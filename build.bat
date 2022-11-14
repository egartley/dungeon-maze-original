cd repo
pyinstaller main.py --noconsole --onefile --hidden-import=mazelib.generate.MazeGenAlgo --icon=pepe.ico
cd dist
move main.exe ..\..\release\
cd ..\..\
xcopy /E "repo\src\sprites\" "release\src\sprites\"