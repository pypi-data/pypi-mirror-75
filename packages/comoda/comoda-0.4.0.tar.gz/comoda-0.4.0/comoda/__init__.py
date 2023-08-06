import logging
import os
import shutil
import subprocess
import sys

from logstash_async.handler import AsynchronousLogstashHandler

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def a_formatter():
    log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)
    return formatter


def a_handler(filename=None, mode="a", formatter=None):
    if filename:
        handler = logging.FileHandler(filename, mode=mode)
    else:
        handler = logging.StreamHandler()

    formatter = formatter if formatter else a_formatter()
    handler.setFormatter(formatter)

    return handler


def a_async_handler(host='0.0.0.0', port=5000, formatter=None):
    async_handler = AsynchronousLogstashHandler(host, port, database_path=None)

    formatter = formatter if formatter else a_formatter()
    async_handler.setFormatter(formatter)

    return async_handler


def a_logger(name, level="WARNING", filename=None, mode="a", host=None, port=5000):
    formatter = a_formatter()
    logger = logging.getLogger(name)

    if not isinstance(level, int):
        try:
            level = getattr(logging, level)
        except AttributeError:
            raise ValueError("unsupported literal log level: %s" % level)
        logger.setLevel(level)

    if host and isinstance(port, int):
        async_handler = a_async_handler(host, port, formatter)
        logger.addHandler(async_handler)

    handler = a_handler(filename, mode, formatter)
    logger.addHandler(handler)
    return logger


# from http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-
# exists-and-create-it-if-necessary/5032238#5032238
def ensure_dir(path, force=False):
    try:
        if force and os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


# from http://stackoverflow.com/questions/19044096/how-to-import-a-submodule-in-
# python-without-exec
def import_from(mod_name, var_name, error_msg=None):
    import importlib
    var = None
    try:
        mod = importlib.import_module(mod_name)
        var = getattr(mod, var_name)
    except ImportError:
        if not error_msg:
            error_msg = 'Module {} missing'.format(mod_name)

    assert var is not None, error_msg
    return var


# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script/11210902#11210902
def is_tool_available(name):
    """
    Check if a program exists
    :param name: label of the tool to search
    :return: boolean
    """
    try:
        devnull = open(os.devnull, 'w')
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def path_is_empty(path):
    """
    Return true if path exists and is empty. False if doesn't exists or
    exists but is not empty
    :param path: path
    :return: boolean
    """
    return not os.listdir(path) if os.path.exists(os.path.expanduser(
        path)) else False


def path_exists(path, logger=None, force=False):
    def missing(p, l, f):
        if f:
            msg = "path - {} - doesn't exists".format(p)
            if l:
                logger.error(msg)
            else:
                print(msg)
            sys.exit()
        return False

    return True if os.path.exists(os.path.expanduser(path)) else missing(path,
                                                                         logger,
                                                                         force)


def search_binary_path(name, path=None, exts=('',)):
    """ http://code.activestate.com/recipes/52224/
    Search PATH for a binary.
    Args:
    name: the filename to search for
    path: the optional path string (default: os.environ['PATH')
    exts: optional list/tuple of extensions to try (default: ('',))

    Returns:
    The abspath to the binary or None if not found.
    """
    path = path or os.getenv('PATH')
    for folder in path.split(os.path.pathsep):
        for ext in exts:
            binpath = os.path.join(folder, name) + ext
            if os.path.exists(binpath):
                return os.path.abspath(binpath)
    return None
