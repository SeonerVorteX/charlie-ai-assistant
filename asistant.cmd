echo off
cls
color b
echo Activating Dev Environments...
call activate tensorflow
echo Starting Charlie...
call python main.py