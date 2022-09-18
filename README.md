# Maze Game Project

# Authors

Brian Hinger Computer Engineering
Tan Tran Computer Science
Evan Gartley Computer Science
Zanieb Radi Computer Science
Cameron Gower Computer Science Information Technology

# Course Information

Professor Robert Despang
Course CS 490-41 CPE 425-41 CPE 525-41
Start Date August 29 2022
End Date December 16 2022

# Purpose 

Software Engineering semester long project. The project is open to what a team decides. As a team the best route we choose was to make a Maze game. The main purpose of the game is to get to the end. As additional features once we get the main game working we choose to possibly add coins, weapons, boosters, and as well as enemies that you may or may not have to kill. Inspiration came from Crossy Road and Temple Run as well as the movie Maze Runner. 

# Software 
Python 3-10
Script for installing dependencies

##  Modules
        https://github.com/john-science/mazelib
        https://www.pygame.org/docs/ref/image.html
        https://www.glfw.org/
        http://pyopengl.sourceforge.net/documentation/
        https://cython.org/
        https://numpy.org/


## Art work

## Defining wthe game world environment 
        Height of walls?
        width of passages?
        

## Developer Installation Tools Before running

https://docs.docker.com/engine/install/
        make sure to make a .wslconfig configuring the docker ram usage to at least 8 gb
https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview


## Docker Automation of Installations
 pip install PyOpenGL PyOpenGL_accelerate 
 sudo apt install freeglut3
 RUN ["pip3", "install", "PyOpenGL"]
 RUN ["pip3", "install", "PyOpenGL_accelerate"]
 RUN ["sudo apt", "install", "freeglut3"]

sudo pip3 install git+https://github.com/mcfletch/pyopengl.git@227f9c66976d9f5dadf62b9a97e6beaec84831ca#subdirectory=accelerate
 Requirement already satisfied: pip in /home/vscode/.local/lib/python3.10/site-packages (22.2.2)
 Requirement already satisfied: pip in /home/vscode/.local/lib/python3.10/site-packages (22.2.2)
### If a npm dependency is needed we can run NPM in python translation mode. 
 sudo apt install nodejs if needed
 sudo apt install npm if needed

The following content in between *** *** is for this scenario of needing nodejs

***
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi
***



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/dungeonmazese/game.git
git branch -M main
git push -uf origin main
```



## License
The main project module used comes from a open source GNU Licensed project. The project modified is and will be free for anyone who may find it but the use is a class assignment and any modifications and broken use of the module on our copy is to be blamed by the Developers who Modified for the class assignment. 

## Project status
Open

## Game Development concepts and ideas

##      Character Development
                - At max <>= 10ft
                - Some features that could exist is apart of further development would be designability for certain clothing colors

                - What is the main character? Person? Minotaur? what?
                - Enemies Zombies? People? Mini-Minotaurs? Feature one after basic game is made
                - Character Weapons Feature 1 child
##      Character Weapons 
                - One or many weapons? 
                - What weapon(s) main character have 
                - Weapon(s) enemies have
                - Weapon type ie basic rare legendary
##      Character Findable Boosters 
                - Health
                - Shield

##      Main game feature
                difficulty selector how many diffiulties?
                day and night feature
                                         

## TimeCard and Card Format

Timecards are to be recorded by the individual please write in the specified format below 

Code or Documentation or Testing some verbage action  as many categories as needed be broad in verbage choice. Convention can be talked about
0...N  entries [Date and time information]

##      Brian Hinger  Team Leader

##      Cam Gower

Docker Environment Configuring
9/10 3 hours
9/11 4 hours
9/12 2 hours

Documentation 

9/11 20 mins

##      Evan Gartley 

##      Tan Tran
 
##      Zanieb Radi

