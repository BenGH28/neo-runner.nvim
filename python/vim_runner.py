"""
A plugin to run a single c/c++ or python file
"""
import os
import re
import typing
from enum import Enum

import vim

CPP_EXT1 = "\.cpp$"
CPP_EXT2 = "\.cc$"
C_EXT = "\.c$"
PY_EXT = "\.py$"

LOG_FILE = "/home/ben/repos/vim-runner/logfile.txt"


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
    match_cpp0 = re.search(CPP_EXT1, file)
    match_cpp1 = re.search(CPP_EXT2, file)
    match_c = re.search(C_EXT, file)
    match_py = re.search(PY_EXT, file)

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
    # filename = os.path.basename(file)
    binaryname = file.split('.')[0]
    build = f"{gcc} {file} -o {binaryname}"
    #TODO navigate to file directory not the file itself
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
    python = "python3"
    cmd = f"{python} {file}"
    os.system(cmd)


def compile_current_file() -> None:
    """compile/run the current vim buffer if possible"""
    filepath = vim.current.buffer.name
    if filepath is None or filepath == "":
        raise Exception(f"{filepath} is None")

    filetype: FileType = __determine_file_type(filepath)

    with open(LOG_FILE, 'w') as f:
        f.write(f"{filepath}\n")
        f.write(f"{filetype}\n")

        if filetype == FileType.c:
            __compile_c_file(filepath)
            f.write("compiled C file\n")
        elif filetype == FileType.cpp:
            __compile_cpp_file(filepath)
            f.write("compiled C++ file\n")
        elif filetype == FileType.py:
            __run_python_script(filepath)
            f.write("compiled python file\n")
        else:
            f.write(f"not a valid file: {filepath}")
