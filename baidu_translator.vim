"Check if py3 is supported
"function! s:UsingPython3()
"  if has('python3')
"    return 1
"  endif
"  if has('python')
"    return 0
"  endif
"  echo "Error: Required vim compiled with +python/+python3"
"  finish
"endfunction
"
"let s:using_python3 = s:UsingPython3()
"let s:python_until_eof = s:using_python3 ? "python3 << EOF" : "python << EOF"
"let s:pcommand = "py " 

let s:initialized_python = 0
let s:script_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:InitializeClient()
    if has('python')
        let s:pcommand = 'python'
        let s:pfile = 'pyfile'
    elseif has('python3')
        let s:pcommand = 'python3'
        let s:pfile = 'py3file'
    else
    echo 'Error: this plugin requires vim compiled with python support.'
    finish
  endif

  if !s:initialized_python
    let s:initialized_python = 1
        execute s:pfile . ' ' . s:script_path . '/baidu_translator.py'
  endif
endfunction


" This function taken from the lh-vim repository
function! s:GetVisualSelection()
    try
        let a_save = @a
        normal! gv"ay
        return @a
    finally
        let @a = a_save
    endtry
endfunction

function! s:GetCursorWord()
    return expand("<cword>")
endfunction

if !exists("g:baidu_appid")
    let g:baidu_appid=''
endif

if !exists("g:baidu_secretKey")
    let g:baidu_secretKey=''
endif

"exec s:python_until_eof
"EOF

function! s:BaiduVisualTranslate()
  call <SID>InitializeClient()
    exec s:pcommand ' baidu_translate_visual_selection(vim.eval("<SID>GetVisualSelection()"))'
endfunction

function! s:BaiduCursorTranslate()
  call <SID>InitializeClient()
    exec s:pcommand ' baidu_translate_visual_selection(vim.eval("<SID>GetCursorWord()"))'
endfunction

function! s:BaiduEnterTranslate()
  call <SID>InitializeClient()
    let word = input("Please enter the word: ")
    redraw!
    exec s:pcommand ' baidu_translate_visual_selection(vim.eval("word"))'
endfunction

command! Bdv call <SID>BaiduVisualTranslate()
command! Bdc call <SID>BaiduCursorTranslate()
command! Bde call <SID>BaiduEnterTranslate()


