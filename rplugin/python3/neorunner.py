""" A plugin to run the current file

Inspired by VSCode's Code Runner this aims to emulate accomplish similar things
but at a far smaller scale.
"""
import os
from typing import Tuple

import pynvim


@pynvim.plugin
class NeoRunner():
    """The NeoVim Plugin"""

    def __init__(self, vim) -> None:
        self.vim = vim

    def __get_var_or_default(self, var: str, default: str) -> str:
        """
        Get global variable or a default
        :params
            var: the user defined variable like `runner_c_compiler`
            default: the defualt to use if there is no user defined global variable

        :return either the global variable specified by `var` or `default`
        """
        try:
            return self.vim.api.get_var(var)
        except:
            return default

    @property
    def filepath(self) -> str:
        """the filepath of the current file"""
        return self.vim.current.buffer.name

    @property
    def filetype(self) -> str:
        """the current filetype"""
        return self.vim.eval('&filetype')

    @property
    def c_compiler(self) -> str:
        """return the user defined C compiler or the default if none exist"""
        return self.__get_var_or_default('runner_c_compiler', 'gcc')

    @property
    def c_options(self) -> str:
        """
        Get the user defined options for the compiler or return empty string if not defined
        :return compiler options as str
        """
        return self.__get_var_or_default('runner_c_options', '')

    @property
    def cpp_compiler(self) -> str:
        """return the user defined C++ compiler or the default if none exist"""
        return self.__get_var_or_default('runner_cpp_compiler', 'g++')

    @property
    def cpp_options(self) -> str:
        """
        Get the user defined options for the compiler or return empty string if not defined
        :return compiler options as str
        """
        return self.__get_var_or_default('runner_cpp_options', '')

    @property
    def python_interpreter(self) -> str:
        """get the version of python the user wants"""
        return self.__get_var_or_default('runner_python_ex', 'python3')

    @property
    def python_options(self) -> str:
        return self.__get_var_or_default('runner_python_options', '')

    def __make_binary_name(self) -> str:
        """
        creates the binary name by removing the file extension
        if the file is found /home/jondo/program.cc then it returns /home/jondo/program
        """
        return self.filepath.split('.')[0]

    def __runner_cmd(self, navigate: str, build: str, run: str) -> str:
        """
        creates a run command for the current buffer
        :params
            navigate: the command to go to the directory that has the file
            build: the specific build command for the file
            run: the command to execute binary
        """
        cmd = f"{navigate} && {build} && {run}"
        # with open('/home/ben/repos/vim-runner/logfile.txt', 'w+') as f:
        #     f.write(cmd)
        return cmd

    def __run_command_in_terminal(self, command: str) -> None:
        """
        open a new terminal window 1/3 the height of the original
        :params
            command: the command to run in the terminal
        """
        win_height = self.vim.current.window.height
        new_win_height = win_height / 3
        self.vim.command(str(new_win_height) + "sp | term " + command)

    def __get_c_or_cpp_properties(self) -> Tuple:
        dictionary = {
            'c': (self.c_compiler, self.c_options),
            'cpp': (self.cpp_compiler, self.cpp_options),
        }
        return dictionary[self.filetype]

    def __compile_c_cpp_file(self) -> None:
        """
        compile a C/C++ file and run it non-interactively
        """
        compiler, options = self.__get_c_or_cpp_properties()
        binaryname = self.__make_binary_name()
        directory = os.path.dirname(self.filepath)

        navigate = f"cd {directory}"
        build = f"{compiler} {options} {self.filepath} -o {binaryname}"
        run = binaryname

        cmd = self.__runner_cmd(navigate, build, run)
        self.__run_command_in_terminal(cmd)

    def __run_python_script(self) -> None:
        """
        Run a python file
        """
        cmd = f"{self.python_interpreter} {self.python_options} {self.filepath}"
        self.__run_command_in_terminal(cmd)

    @property
    def filetypes_to_functions(self) -> dict:
        """
        A dictionary of filetypes mapped to their appropriate execution functions.
        """
        dictionary = {
            'cpp': self.__compile_c_cpp_file,
            'c': self.__compile_c_cpp_file,
            'python': self.__run_python_script
        }
        return dictionary

    def __compile_and_run(self) -> None:
        """determine file type based on file extension
        :params
            filepath: the file to check
        """
        if self.filetype in self.filetypes_to_functions:
            compile_func = self.filetypes_to_functions[self.filetype]
            compile_func()
        else:
            self.vim.api.err_writeln(
                f"NeoRunner doesn't support `{self.filetype}` file type")

    @pynvim.function('compile_current_file')
    def compile_current_file(self) -> None:
        """compile/run the current vim buffer if possible"""
        self.__compile_and_run()

    @pynvim.command('NeoRunner')
    def NeoRunner(self) -> None:
        """the NeoVim command to runner"""
        self.compile_current_file()
