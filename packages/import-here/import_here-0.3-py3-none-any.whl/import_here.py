import os
import imp
from typing import Optional

version = "0.3"


def import_module_here(path, module_name, file=None):
    if not os.path.isfile(path):
        if file is None:
            raise ValueError(
                "when `path` is not a file, must pass `__file__` varaible as argument `file`"
            )
        path = os.path.join(get_root_dir(file), path)
    with open(path, "rb") as fp:
        return imp.load_module(module_name, fp, path, (".py", "rb", imp.PY_SOURCE))


def get_root_dir(__file__):
    return os.path.dirname(os.path.abspath(__file__))


def export_all(lib, locals: Optional[dict] = None):
    __all__ = getattr(lib, '__all__', None)
    if __all__:
        export = {k: getattr(lib, k) for k in __all__}
    else:
        export = {k: v for k, v in lib.__dict__.items() if not k.startswith('_')}
    if locals:
        locals.update(export)
    return export
