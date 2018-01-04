@echo off
cd /d %~dp0
mklink /D x64\Release\python ..\..\wxFEFactory\python
pause