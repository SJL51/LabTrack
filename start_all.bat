@echo off
REM Start server
cd /d D:\LabTrack_prototype\server
echo Starting Flask server...
start cmd /k "python server.py"

REM Start client(s)
cd /d D:\LabTrack_prototype\client
echo Starting client reporting script...
start cmd /k "python client.py"

REM Add more clients if needed:
REM start cmd /k "python client2.py"
