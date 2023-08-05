# _*_ coding: utf-8 _*_
import hashlib
import os
import platform
import shutil
import sys
import time

from .ae_logger import ae_log
from .ae_util import ae_isWindow


def copy_file(src, dst, check_hash=True, progress=True):
    buf_size = 64 * 1024
    name = os.path.basename(src)
    if os.path.isdir(dst):
        dst = os.path.join(dst, name)
    if os.path.exists(dst):
        os.remove(dst)

    try:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                length = 0
                total = get_file_size(src)
                while length < total:
                    buf = fsrc.read(buf_size)
                    fdst.write(buf)
                    length += len(buf)
                    if progress:
                        ae_log.debug(f'{src} | {length} / {total}')
                    time.sleep(0.01)
        os.system("sync")
    except Exception as e:
        ae_log.exception(e)
    finally:
        if check_hash and get_hash(src) != get_hash(dst):
            ae_log.debug("The hash value different between the source file and the destination file.")
            if os.path.exists(dst):
                os.remove(dst)
            return False
        ae_log.debug("file copied.. size:%s, path:%s" % (sizeof_fmt(get_file_size(dst)), dst))
    return True


def move_file(src, dst):
    try:
        shutil.move(src, dst)
        os.system("sync")
    except Exception as e:
        ae_log.exception(e)


def get_path_increment(path, file):
    if not os.path.exists(os.path.join(path, file)):
        return os.path.join(path, file)

    i = 0
    name = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1]
    while os.path.exists(os.path.join(path, "{}({}){}".format(name, i, ext))):
        i += 1
    return os.path.join(path, "{}({}){}".format(name, i, ext))


def sizeof_fmt(num):
    for unit in ['', 'KB', 'MB', 'GB', 'TB']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, 'Bytes')


def get_hash(path, block=64 * 1024):
    if not os.path.exists(path):
        return
    md5 = hashlib.md5()
    with open(path, 'rb') as file:
        while True:
            buf = file.read(block)
            if not buf:
                break
            md5.update(buf)
    return md5.hexdigest()


def get_hash2(path, block=64 * 1024):
    if not os.path.exists(path):
        return
    md5 = hashlib.md5()
    md5.update(open(path, 'rb').read())
    return md5.hexdigest()


def delete_file(file):
    try:
        os.remove(file)
    except Exception as e:
        ae_log.exception(e)


def get_file_size(file):
    stat = os.stat(file)
    return stat.st_size


def split_path(file):
    path, file = file.split(os.path.basename(file))
    return path


def available_size(path):
    size = 0
    if platform.system() == "Windows":
        size = sys.maxsize
    else:
        st = os.statvfs(path)
        if st:
            size = st.f_bavail * st.f_frsize
    return size


def is_available_size(src, dst):
    src_size = get_file_size(src)
    dst_size = available_size(split_path(dst))
    ae_log.debug("is_available_space:{0}, file_size:{1}".format(sizeof_fmt(dst_size), sizeof_fmt(src_size)))
    return dst_size > src_size


def delete_files(root: str):
    files = os.listdir(root)
    for file in files:
        path = os.path.join(root, file)
        if not os.path.isdir(path):
            os.remove(path)


def delete_recursive(root: str):
    files = os.listdir(root)
    for file in files:
        path = os.path.join(root, file)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def is_hidden(path):
    name = os.path.basename(path)
    return name.startswith(".") or has_hidden_attribute(path)


def get_folder_list(path):
    if not os.path.isdir(path) or not os.path.exists(path):
        return ""
    folder_list = sorted([file for file in os.listdir(path)
                          if os.path.isdir(os.path.join(path, file)) and not is_hidden(os.path.join(path, file))], key=lambda file: file.upper())
    return folder_list


def read_file(path, length):
    if not os.path.exists(path):
        return bytearray()
    with open(path, "rb") as file:
        return file.read(length)


def has_hidden_attribute(path):
    FILE_ATTRIBUTE_HIDDEN = 0x2
    FILE_ATTRIBUTE_DIRECTORY = 0x10
    FILE_ATTRIBUTE_ARCHIVE = 0x20
    FILE_ATTRIBUTE_NORMAL = 0x80
    if ae_isWindow():
        return bool(os.stat(path).st_file_attributes & FILE_ATTRIBUTE_HIDDEN)
