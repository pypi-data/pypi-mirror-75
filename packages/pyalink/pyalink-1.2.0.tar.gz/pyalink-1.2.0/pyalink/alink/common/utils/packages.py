import os


def has_package(name: str):
    import pkg_resources
    try:
        pkg_resources.get_distribution(name)
    except pkg_resources.DistributionNotFound:
        return False
    return True


def has_pyflink() -> bool:
    """
    Test if pyflink is found, i.e. pyalink 1.10+
    :return: pyflink if found or not
    :rtype bool
    """
    if (not has_package("pyalink-flink-1.9")) and has_package("apache-flink"):
        return True
    else:
        return False


def get_alink_lib_path() -> str:
    import pyalink
    import os
    for path in pyalink.__path__:
        lib_path = os.path.join(path, "lib")
        if os.path.isdir(lib_path):
            return lib_path
    raise Exception("Cannot find pyalink Java libraries, please check your installation.")


def get_pyflink_path() -> str:
    if has_pyflink():
        import pyflink
        for path in pyflink.__path__:
            if os.path.isdir(path):
                return path
    else:
        alink_lib_path = get_alink_lib_path()
        for f in os.listdir(alink_lib_path):
            path = os.path.join(alink_lib_path, f)
            if f.startswith("flink-") and os.path.isdir(path):
                return path
    print("Warning: cannot find pyflink path. "
          "If not running using 'flink run', please check if PyFlink is installed correctly.")


def in_ipython() -> bool:
    """
    Test if in ipython
    :return: in ipython or not
    :rtype bool
    """
    from IPython import get_ipython
    return get_ipython() is not None
