from importlib import import_module


def import_class(name):
    mod_path, cls_name = name.rsplit(':', 1)
    mod = import_module(mod_path)
    return getattr(mod, cls_name)
