"""
Operating system functions.
"""
__all__ = [
    'abspath',
    'pushd_popd',
    'unzip_file_to_dir',
    'atomic_write',
]

from atomicwrites import atomic_write as atomic_write_
from tempfile import TemporaryDirectory
import contextlib
from os import getcwd, chdir, stat, chmod
from os.path import exists, abspath as abspath_

from zipfile import ZipFile

def abspath(url):
    """
    Get a full path to a file or file URL

    See os.abspath
    """
    if url.startswith('file://'):
        url = url[len('file://'):]
    return abspath_(url)

@contextlib.contextmanager
def pushd_popd(newcwd=None, tempdir=False):
    if newcwd and tempdir:
        raise Exception("pushd_popd can accept either newcwd or tempdir, not both")
    try:
        oldcwd = getcwd()
    except FileNotFoundError as e:  # pylint: disable=unused-variable
        # This happens when a directory is deleted before the context is exited
        oldcwd = '/tmp'
    try:
        if tempdir:
            with TemporaryDirectory() as tempcwd:
                chdir(tempcwd)
                yield tempcwd
        else:
            if newcwd:
                chdir(newcwd)
            yield newcwd
    finally:
        chdir(oldcwd)

def unzip_file_to_dir(path_to_zip, output_directory):
    """
    Extract a ZIP archive to a directory
    """
    z = ZipFile(path_to_zip, 'r')
    z.extractall(output_directory)
    z.close()

@contextlib.contextmanager
def atomic_write(fpath, overwrite=False):
    if exists(fpath):
        mode = stat(fpath).st_mode
    else:
        mode =  0o664
    with atomic_write_(fpath, overwrite=True) as f:
        yield f
    chmod(fpath, mode)
