""" A plugin to run the current file

Inspired by VSCode's Code Runner this aims to emulate accomplish similar things
but at a far smaller scale.
"""
import os

import pynvim


@pynvim.plugin
class NeoRunner():
    """The NeoVim Plugin"""

    def __init__(self, vim) -> None:
        self.vim = vim

    @property
    def c_compiler(self) -> str:
        """return the user defined C compiler or the default if none exist"""
        try:
            return self.vim.api.get_var('runner_c_compiler')
        except:
            return 'gcc'

    @property
    def c_options(self) -> str:
        """
        Get the user defined options for the compiler or return empty string if not defined
        :return compiler options as str
        """
        try:
            return self.vim.api.get_var('runner_c_options')
        except:
            return ''

    @property
    def cpp_compiler(self) -> str:
        """return the user defined C++ compiler or the default if none exist"""
        try:
            return self.vim.api.get_var('runner_cpp_compiler')
        except:
            return 'g++'

    @property
    def cpp_options(self) -> str:
        """
        Get the user defined options for the compiler or return empty string if not defined
        :return compiler options as str
        """
        try:
            return self.vim.api.get_var('runner_cpp_options')
        except:
            return ''

    def __compile_and_run(self, filepath: str) -> None:
        """determine file type based on file extension
        :params
            filepath: the file to check
        """
        filetype: str = self.vim.eval('&filetype')

        if filetype == 'python':
            self.__run_python_script(filepath)
        elif filetype == 'cpp':
            self.__compile_c_cpp_file(self.cpp_compiler, filepath)
        elif filetype == 'c':
            self.__compile_c_cpp_file(self.c_compiler, filepath)
        else:
            self.vim.api.err_writeln(
                f"NeoRunner doesn't support `{filetype}` file type")

    def __run_command_in_terminal(self, command: str) -> None:
        """
        open a new terminal window 1/3 the height of the original
        :params
            command: the command to run in the terminal
        """
        win_height = self.vim.current.window.height
        new_win_height = win_height / 3
        self.vim.command(str(new_win_height) + "sp | term " + command)

    def __make_binary_name(self, filepath: str):
        """
        creates the binary name by removing the file extension
        if the file is found /home/jondo/program.cc then it returns /home/jondo/program
        :params
            filepath: the full path to the file
        """
        return filepath.split('.')[0]

    def __runner_cmd(self, navigate: str, build: str, run: str):
        """
        creates a run command for the current buffer
        :params
            navigate: the command to go to the directory that has the file
            build: the specific build command for the file
            run: the command to execute binary
        """
        cmd = f"{navigate} && {build} && {run}"
        with open('/home/ben/repos/vim-runner/logfile.txt', 'w+') as f:
            f.write(cmd)
        return cmd

    def __compile_c_cpp_file(self, compiler_to_use: str,  filepath: str, options: str = "") -> None:
        """
        compile a C/C++ file and run it non-interactively
        :params
            compiler_to_use: the compiler you wish to use (should be one of gcc, g++ or clang)
            filepath: the full path to the C/C++ file
        """
        compiler = compiler_to_use
        binaryname = self.__make_binary_name(filepath)
        directory = os.path.dirname(filepath)

        navigate = f"cd {directory}"
        build = f"{compiler} {options} {filepath} -o {binaryname}"
        run = binaryname

        cmd = self.__runner_cmd(navigate, build, run)
        self.__run_command_in_terminal(cmd)

    def __run_python_script(self, filepath: str) -> None:
        """
        Run a python file
        :params
            filepath: the full path to the python file
        """
        python = "python3"
        cmd = f"{python} {filepath}"
        self.__run_command_in_terminal(cmd)

    @pynvim.function('compile_current_file')
    def compile_current_file(self) -> None:
        """compile/run the current vim buffer if possible"""
        filepath = self.vim.current.buffer.name

        if filepath is None or filepath == "":
            raise Exception(f"{filepath} is None")
        self.__compile_and_run(filepath)

    @pynvim.command('NeoRunner')
    def NeoRunner(self) -> None:
        """the NeoVim command to runner"""
        self.compile_current_file()
