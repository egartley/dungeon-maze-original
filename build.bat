@echo off
cd src
pyinstaller main.py --onefile --hidden-import=mazelib.generate.MazeGenAlgo
cd dist
move main.exe ..\..\release\
cd ..\..\release
copy ..\src\*.png
