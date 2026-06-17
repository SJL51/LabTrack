@echo off
REM Navigate to the server folder
cd /d D:\LabTrack_prototype\server

echo Starting Flask server...
start cmd /k "python server.py"
