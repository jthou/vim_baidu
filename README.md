# 百度翻译vim插件

## 使用方法
* 光标停留在单词单词处，按ctrl+B，在命令行将显示百度翻译返回结果
* 选中单词，按ctrl+B
* 在命令状态下收入:Bde 单词

## 安装步骤
* 将本项目中的两个文件添加到vim的plugin目录
* 在.vimrc中加入

> " Baidu Fanyi
> let g:baidu_appid='yourid'
> let g:baidu_secretKey='yourkey'
> vnoremap <silent> <C-B> :<C-u>Bdv<CR>
> nnoremap <silent> <C-B> :<C-u>Bdc<CR>
