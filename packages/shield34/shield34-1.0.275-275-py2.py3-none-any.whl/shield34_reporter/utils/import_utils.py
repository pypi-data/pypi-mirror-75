import sys

def is_module_available(module_name):
    if sys.version_info < (3, 0):
        # python 2
        try:
            __import__(module_name)
        except ImportError:
            torch_loader = None
        else:
            torch_loader = True
        #torch_loader = importlib.find_loader(module_name)
    elif sys.version_info <= (3, 3):
        # python 3.0 to 3.3
        import pkgutil
        torch_loader = pkgutil.find_loader(module_name)
    elif sys.version_info >= (3, 4):
        # python 3.4 and above
        from importlib import util
        torch_loader = util.find_spec(module_name)

    return torch_loader is not None