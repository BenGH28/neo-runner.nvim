"""
A plugin to run a single c/c++ or python file
"""
import os
import re
import typing
from enum import Enum

import vim

# regex
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


# def __run_commmand_in_term(cmd: str) -> None:
#     """will send cmd to be run in the terminal"""
#     if vim.eval("has('vim')"):
#         # call vim specific terminal stuff
#         pass
#     else:
#         # call nvim specific terminal commands
#         # TODO get the terminal buffer and then do this stuff
#         vim.command("normal! echo 'trying to print to the terminal'")
#         vim.command(f'noraml! let @z = "{cmd}\n" | normal! "zp ')


def __open_new_display_win(binaryname: str) -> None:
    """ open a new terminal window 1/3 the height of the original"""
    win_height = vim.current.window.height
    new_win_height = win_height / 3
    vim.command(str(new_win_height) + "sp | term " + binaryname)


def __make_binary_name(filepath: str):
    return filepath.split('.')[0]


def __runner_cmd(navigate: str, build: str, run: str):
    cmd = f"{navigate} && {build} && {run}"
    return cmd


def __compile_c_file(filepath: str) -> None:
    """
    compile a C file and run it non-interactively
    :params
        filepath: the full path to the C file
    """
    gcc = "gcc"
    binaryname = __make_binary_name(filepath)
    directory = os.path.dirname(filepath)

    navigate = f"cd {directory}"
    build = f"{gcc} {filepath} -o {binaryname}"
    run = f"./{binaryname}"

    cmd = __runner_cmd(navigate, build, run)
    result = os.system(cmd)
    __open_new_display_win(binaryname)


def __compile_cpp_file(filepath: str) -> None:
    """
    compile a c++ file and run it non-interactively
    :params
        filepath: the full path to the C++ file
    """
    gpp = "g++"
    binaryname = __make_binary_name(filepath)
    directory = os.path.dirname(filepath)

    navigate = f"cd {directory}"
    build = f"{gpp} {filepath} -o {binaryname}"
    run = f"./{binaryname}"

    cmd = __runner_cmd(navigate, build, run)
    os.system(cmd)
    __open_new_display_win(binaryname)


def __run_python_script(filepath: str) -> None:
    """
    run a python file non-interactively
    :params
        filepath: the full path to the python file
    """
    python = "python3"
    cmd = f"{python} {filepath}"
    __open_new_display_win(cmd)


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
