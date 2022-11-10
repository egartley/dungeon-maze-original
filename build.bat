cd src
pyinstaller main.py --noconsole --onefile --hidden-import=mazelib.generate.MazeGenAlgo --icon=pepe.ico
cd dist
move main.exe ..\..\release\
cd ..\..\release
copy ..\src\*.png
