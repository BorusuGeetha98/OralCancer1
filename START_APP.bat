@echo off
taskkill /f /im node.exe
cd OralCancerApp
npx expo start -c
