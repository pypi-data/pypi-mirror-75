use libsystemd::activation::{receive_descriptors, IsType};
use mio::event::Source;
use mio::net::{TcpListener, TcpStream, UnixListener, UnixStream};
use nix::fcntl::{fcntl, FcntlArg, OFlag};
use std::error;
use std::fmt::Debug;
use std::io;
use std::net;
use std::os::unix::io::{AsRawFd, FromRawFd, IntoRawFd, RawFd};

pub type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

// we need AsRawFd for sendfile
pub trait Write: io::Write + AsRawFd {}
impl<T: io::Write + AsRawFd> Write for T {}

pub trait NonBlockingWrite: Write + Send + Source {}
impl<T: Write + Send + Source> NonBlockingWrite for T {}

pub trait BlockingWrite: Socket + SetBlocking {}
impl<T: Socket + SetBlocking> BlockingWrite for T {}

pub trait Read: io::Read {
    fn peer_addr(&self) -> String;
}

impl Read for TcpStream {
    fn peer_addr(&self) -> String {
        match TcpStream::peer_addr(&self) {
            Ok(addr) => format!("{}", addr.ip()),
            Err(_) => String::new(),
        }
    }
}

impl Read for UnixStream {
    fn peer_addr(&self) -> String {
        match UnixStream::peer_addr(&self) {
            Ok(addr) => format!("{:?}", addr.as_pathname()),
            Err(_) => String::new(),
        }
    }
}

pub fn would_block(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::WouldBlock
}

/// set a file descriptor into blocking mode
pub trait SetBlocking: AsRawFd {
    fn set_blocking(&mut self) -> Result<()>;
}
impl<T: AsRawFd> SetBlocking for T {
    #[inline]
    fn set_blocking(&mut self) -> Result<()> {
        let flags = fcntl(self.as_raw_fd(), FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.remove(OFlag::O_NONBLOCK);
        fcntl(self.as_raw_fd(), FcntlArg::F_SETFL(new_flags))?;
        Ok(())
    }
}

/// set a file descriptor into non-blocking mode
pub trait SetNonBlocking {
    type Fd;
    fn set_nonblocking(self) -> Result<Self::Fd>;
}

impl SetNonBlocking for RawFd {
    type Fd = RawFd;
    #[inline]
    fn set_nonblocking(self) -> Result<Self::Fd> {
        let flags = fcntl(self, FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.insert(OFlag::O_NONBLOCK);
        fcntl(self, FcntlArg::F_SETFL(new_flags))?;
        Ok(self)
    }
}

pub trait Socket: AsRawFd + io::Write + Read + Send + Source {}

impl<S: AsRawFd + io::Write + Read + Send + Source> Socket for S {}

/// commonalities of TCPListener + UnixListener
pub trait Listening {
    type Connected: Socket + Debug + SetBlocking;
    fn accept(&self) -> io::Result<Self::Connected>;
}

// s. https://stackoverflow.com/questions/53713354/implementing-traits-without-repeating-methods-already-defined-on-the-struct
impl Listening for TcpListener {
    type Connected = TcpStream;
    fn accept(&self) -> io::Result<Self::Connected> {
        match TcpListener::accept(&self) {
            Ok((conn, _)) => Ok(conn),
            Err(e) => Err(e),
        }
    }
}

impl Listening for UnixListener {
    type Connected = UnixStream;
    fn accept(&self) -> io::Result<Self::Connected> {
        match UnixListener::accept(&self) {
            Ok((conn, _)) => Ok(conn),
            Err(e) => Err(e),
        }
    }
}

pub trait Listener: Listening + Source + FromRawFd {}
impl<L: Listening + Source + FromRawFd> Listener for L {}

/// get a socket activated by systemd
pub fn get_active_socket<L: Listener>() -> Result<L> {
    match receive_descriptors(false) {
        Ok(mut possible_fds) => {
            // check whether systemd has passed a valid file descriptor
            if !possible_fds.is_empty() {
                let fd = possible_fds.remove(0);
                if fd.is_inet() | fd.is_unix() {
                    let rawfd = fd.into_raw_fd().set_nonblocking()?;
                    Ok(unsafe { L::from_raw_fd(rawfd) })
                } else {
                    Err(Box::new(io::Error::new(
                        io::ErrorKind::Other,
                        "File descriptor must be a TCP or Unix Domain socket",
                    )))
                }
            } else {
                Err(Box::new(io::Error::new(
                    io::ErrorKind::Other,
                    "Could not get file descriptors",
                )))
            }
        }
        Err(e) => Err(Box::new(e)),
    }
}

pub fn parse_server_info(addr: &str) -> (String, String) {
    match addr.parse::<net::SocketAddr>() {
        Ok(ipaddr) => (format!("{}", ipaddr.ip()), format!("{}", ipaddr.port())),
        Err(_) => (String::from(addr), String::new()),
    }
}

#[cfg(test)]
mod tests {

    use log::debug;
    use mio::net::{self, TcpListener, UnixListener};
    use nix::fcntl::{fcntl, FcntlArg, OFlag};
    use nix::unistd::dup2;
    use std::env::set_var;
    use std::fs::remove_file;
    use std::io;
    use std::net::SocketAddr;
    use std::os::unix::io::AsRawFd;
    use std::process::id;
    use tempfile::tempfile;

    use crate::transport::{get_active_socket, parse_server_info, would_block, SetNonBlocking};

    #[test]
    fn test_would_block() {
        let wbe = io::Error::new(io::ErrorKind::WouldBlock, "foo");
        assert!(would_block(&wbe));
        let nwbe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!would_block(&nwbe));
    }

    #[test]
    fn test_set_nonblocking() {
        let addr: SocketAddr = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(addr).unwrap();
        let before = net::TcpStream::connect(listener.local_addr().unwrap()).unwrap();
        let o_before =
            OFlag::from_bits(fcntl(before.as_raw_fd(), FcntlArg::F_GETFL).unwrap()).unwrap();
        assert!(o_before.contains(OFlag::O_NONBLOCK));
        match before.as_raw_fd().set_nonblocking() {
            Ok(after) => {
                let o_after = OFlag::from_bits(fcntl(after, FcntlArg::F_GETFL).unwrap()).unwrap();
                assert!(o_after.contains(OFlag::O_NONBLOCK));
            }
            Err(e) => {
                debug!("Unexpected error: {:?}", e);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_get_active_socket() {
        // no systemd environment
        match get_active_socket::<TcpListener>() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // no file descriptors
        set_var("LISTEN_FDS", "");
        set_var("LISTEN_PID", format!("{}", id()));
        match get_active_socket::<TcpListener>() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // file descriptor is not a socket
        let tmp = tempfile().unwrap();
        dup2(tmp.as_raw_fd(), 3).unwrap();
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match get_active_socket::<TcpListener>() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // Success
        let si = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(si).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match get_active_socket::<TcpListener>() {
            Ok(sock) => {
                debug!("{:?}", sock);
                assert!(sock.as_raw_fd() == 3);
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false)
            }
        }
        // UnixListener
        let si = "/tmp/test.socket";
        let listener = UnixListener::bind(si).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match get_active_socket::<UnixListener>() {
            Ok(sock) => {
                debug!("{:?}", sock);
                assert!(sock.as_raw_fd() == 3);
            }
            Err(e) => {
                println!("Error: {:?}", e);
                assert!(false)
            }
        }
        remove_file("/tmp/test.socket").unwrap();
    }

    #[test]
    fn test_parse_server_info() {
        assert!(
            parse_server_info("127.0.0.1:7878") == ("127.0.0.1".to_string(), "7878".to_string())
        );
        assert!(
            parse_server_info("/tmp/pyruvate.sock")
                == ("/tmp/pyruvate.sock".to_string(), String::new())
        );
    }
}
