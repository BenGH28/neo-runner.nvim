<h1 align="center">
  <br>
  <img src="https://www.flaticon.com/svg/3893/3893735.svg" alt="Markdownify" width="250">
  <br>
	<em>neo-runner.nvim</em>
  <br>
</h1>

Inspired by VS Code's [Code Runner](https://github.com/formulahendry/vscode-code-runner) but nowhere near as broad.
***neo-runner*** allows you to run your file without ever leaving Neovim.

## Language Support

- C/C++
- Python

Should I feel the need or if there is any demand for this plugin
I can add more.

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug)

```vim
Plug 'BenGH28/neo-runner.nvim', {'on': 'UpdateRemotePlugins'}
```

## Usage

![Imgur](https://imgur.com/a/Y4DIVO5)

```vim
:NeoRunner
```

The lone command that will compile and execute your code.

## Customisation

***neo-runner*** uses `gcc`, `g++` and `python3` by default for
execution.

To customise the functionality of ***neo-runner*** you can add
something like the following to your `init.vim`

```vim
"C/C++
let g:runner_c_compiler = 'clang'
let g:runner_cpp_compiler = 'clang++'
let g:runner_c_options = '-std=c99 -Wall'
let g:runner_cpp_options = '-std=c++11 -Wall'

"Python
let g:runner_python_ex = 'python'
let g:runner_python_options = '-I'
```

## Credits

Header icon made by [Freepik](https://www.flaticon.com/authors/freepik) from www.flaticon.com

