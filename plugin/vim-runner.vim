let s:save_cpo = &cpo
set cpo&vim

if exists("g:loaded_vim_runner")
	finish
endif
let g:loaded_vim_runner = 1

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import vim_runner
EOF

function! VimRunner()
	python3 vim_runner.compile_current_file()
endfunction

command! -narg=0 VimRunner call VimRunner()

let &cpo = s:save_cpo
unlet s:save_cpo
