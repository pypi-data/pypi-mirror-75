use cpython::{NoArgs, ObjectProtocol, PyObject, PyResult, Python};
pub use python3_sys::{PyGILState_Ensure, PyGILState_Release, PyGILState_STATE, Py_None};

pub fn with_gil<'a, F, R>(mut code: F) -> R
where
    F: FnMut(Python<'a>, PyGILState_STATE) -> R,
{
    let (gilstate, py) = unsafe { (PyGILState_Ensure(), Python::assume_gil_acquired()) };
    let result = code(py, gilstate);
    unsafe { PyGILState_Release(gilstate) };
    result
}

pub fn with_released_gil<F, R>(gilstate: PyGILState_STATE, mut code: F) -> R
where
    F: FnMut() -> R,
{
    unsafe { PyGILState_Release(gilstate) };
    let result = code();
    unsafe { PyGILState_Ensure() };
    result
}

pub fn close_pyobject(ob: &mut PyObject, py: Python) -> PyResult<()> {
    if ob.getattr(py, "close").is_ok() {
        ob.call_method(py, "close", NoArgs, None)?;
    }
    Ok(())
}
