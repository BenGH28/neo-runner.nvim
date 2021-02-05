"""
A plugin to run a single c/c++ or python file.

Inspired by VSCode's Code Runner this aims to emulate accomplish similar things
but at a far smaller scale.  Currently it only supports C/C++ and python but it can
be extended further if need be.
"""
import os
from typing import Tuple
from enum import Enum

import vim

C_COMPILER = vim.eval("get(g:, 'runner_c_compiler', 'gcc')")
CPP_COMPILER = vim.eval("get(g:, 'runner_cpp_compiler', 'g++')")


class FileType(Enum):
    """different filetypes that I can handle"""
    other = 0
    cpp = 1
    c = 2
    py = 3


def __determine_file_type() -> Tuple[FileType, str]:
    """determine file type based on file extension
    :params
        file (str): the file to check
    :returns
        filetype(FileType): the type of file
    """
    filetype: str = vim.eval('&filetype')

    if filetype == 'python':
        return FileType.py, filetype
    if filetype == 'cpp':
        return FileType.cpp, filetype
    if filetype == 'c':
        return FileType.c, filetype
    return FileType.other, filetype


def __open_new_display_win(command: str) -> None:
    """
    open a new terminal window 1/3 the height of the original
    :params
        command: the command to run in the terminal
    """
    win_height = vim.current.window.height
    new_win_height = win_height / 3
    if vim.eval("exists('v:versionlong')"):
        pass
    else:
        vim.command(str(new_win_height) + "sp | term " + command)


def __make_binary_name(filepath: str):
    """
    creates the binary name by removing the file extension
    if the file is found /home/jondo/program.cc then it returns /home/jondo/program
    :params
        filepath: the full path to the file
    """
    return filepath.split('.')[0]


def __runner_cmd(navigate: str, build: str, run: str):
    """
    creates a run command for the current buffer
    :params
        navigate: the command to go to the directory that has the file
        build: the specific build command for the file
        run: the command to execute binary
    """
    cmd = f"{navigate} && {build} && {run}"
    return cmd


def __compile_c_cpp_file(compiler_to_use: str,  filepath: str, options: str = "") -> None:
    """
    compile a c++ file and run it non-interactively
    :params
        compiler_to_use: the compiler you wish to use (should be one of gcc, g++ or clang)
        filepath: the full path to the C/C++ file
    """
    compiler = compiler_to_use
    binaryname = __make_binary_name(filepath)
    directory = os.path.dirname(filepath)

    navigate = f"cd {directory}"
    build = f"{compiler} {options} {filepath} -o {binaryname}"
    run = binaryname

    cmd = __runner_cmd(navigate, build, run)
    print(cmd)
    __open_new_display_win(cmd)


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

    filetype, ft_str = __determine_file_type()

    if filetype is FileType.c:
        __compile_c_cpp_file(C_COMPILER, filepath)
    elif filetype is FileType.cpp:
        __compile_c_cpp_file(CPP_COMPILER, filepath)
    elif filetype is FileType.py:
        __run_python_script(filepath)
    else:
        print(f"VimRunner doesn't support `{ft_str}` file type")
