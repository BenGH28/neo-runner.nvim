"""
A plugin to run a single c/c++ or python file
"""
import os
import re
import typing
from enum import Enum

import vim

CPP_EXT1 = ".cpp$"
CPP_EXT2 = ".cc$"
C_EXT = ".c$"
PY_EXT = ".py$"


class FileType(Enum):
    """different filetypes that I can handle"""
    other = 0
    cpp = 1
    c = 2
    py = 3


def __determine_file_type(file: str) -> FileType:
    """determine file type based on file extension
    :params
        file (str): the file to check
    :returns
        filetype(FileType): the type of file
    """
    match_cpp0 = re.match(CPP_EXT1, file, flags=0)
    match_cpp1 = re.match(CPP_EXT2, file, flags=0)
    match_c = re.match(C_EXT, file, flags=0)
    match_py = re.match(PY_EXT, file, flags=0)

    if match_cpp0 or match_cpp1:
        return FileType.cpp
    if match_c:
        return FileType.c
    if match_py:
        return FileType.py
    return FileType.other


def __compile_c_file(file: str) -> None:
    """compile a C file"""
    gcc = "gcc"
    filename = os.path.basename(file)
    binaryname = filename.split('.')[0]
    build = f"{gcc} {file} -o {binaryname}"
    navigate = f"cd {file}"
    cmd = f"{navigate} && {build}"
    os.system(cmd)


def __compile_cpp_file(file) -> None:
    gpp = "g++"
    filename = os.path.basename(file)
    binaryname = filename.split('.')[0]
    build = f"{gpp} {file} -o {binaryname}"
    navigate = f"cd {file}"
    cmd = f"{navigate} && {build}"
    os.system(cmd)


def __run_python_script(file) -> None:
    py = "python3"
    cmd = f"{py} {file}"
    os.system(cmd)



def compile_current_file() -> None:
    """compile/run the current vim buffer if possible"""
    filepath: str = vim.current.buffer.name
    filetype = __determine_file_type(filepath)

    if filetype == FileType.c:
        __compile_c_file(filepath)
    elif filetype == FileType.cpp:
        __compile_cpp_file(filepath)
    else:
        __run_python_script(filepath)
