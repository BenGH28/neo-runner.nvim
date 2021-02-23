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

## Requirements

Use `:checkhealth` to see if you meet the requirements below.
- neovim
- python3
- [pynvim](https://github.com/neovim/pynvim)

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug)

```vim
Plug 'BenGH28/neo-runner.nvim', {'do': ':UpdateRemotePlugins'}
```

Once you `:PlugInstall` run `:UpdateRemotePlugins`

## Usage

<img src=https://i.imgur.com/QSmS2Ld.gif width=600>

```vim
:NeoRunner
```

The lone command that will compile and execute your code.

## Config

***neo-runner*** uses `gcc`, `g++` and `python3` by default for
execution.

Example config

```vim
"C/C++
let g:runner_c_compiler = 'gcc'
let g:runner_cpp_compiler = 'g++'
let g:runner_c_options = '-std=c99 -Wall'
let g:runner_cpp_options = '-std=c++11 -Wall'

"Python
let g:runner_python_ex = 'python3'
let g:runner_python_options = ''
```

## Credits

Header icon made by [Freepik](https://www.flaticon.com/authors/freepik) from www.flaticon.com

