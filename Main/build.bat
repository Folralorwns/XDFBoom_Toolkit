@echo off
title 打包 XDFBoom Toolkit
echo 正在使用 Nuitka 打包 main.py...

nuitka ^
  --standalone ^
  --enable-plugin=pyside6 ^
  --include-data-dir=resources=resources ^
  --output-dir=build ^
  --windows-icon-from-ico=resources/ico/logo_light_theme.ico ^
  --windows-disable-console ^
  main.py

echo 打包完成！输出目录在 build\main.dist\
pause
