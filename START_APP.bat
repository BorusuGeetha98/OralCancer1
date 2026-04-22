@echo off
taskkill /f /im node.exe
set EXPO_PACKAGER_GENERAL_HOST_ADDR=10.81.212.8
cd c:\Users\geeth\Desktop\project\ReactApp
npx expo start -c
