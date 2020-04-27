import ert_logging
from .ert_adapter import ERT

def clear_global_state():
    """Deletes the global ERT instance shared as a global variable in the
    ert_shared module. This is due to an exception that arrises when closing
    the ERT application when modules, Python objects and C-objects are removed.
    Over time the singleton instance of ERT should disappear and this function
    should be removed.
    """
    global ERT
    if ERT is None:
        return

    ERT._implementation = None
    ERT._enkf_facade = None
    ERT = None
