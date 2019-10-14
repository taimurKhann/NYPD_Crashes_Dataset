# NYPD_Crashes_Dataset

Below are the instructions to run the code

1) Make sure docker is already installed and running.
2) Download the code from the repository
3) run command "docker build -t creditshelf:1.0 ."
4) Once the image has been build run below command
docker run -it -p 5656:80 creditshelf:1.0 bash

5) Once the command ran and docker image bash opens run below command
./script.py

6) After the execution of the script open the browser and type below uel
http://127.0.0.1:5656/
