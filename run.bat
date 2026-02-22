@echo off
REM SWIN - Startup Script for Windows

cls
color 0B
title SWIN - Sentiment-driven Workflow Intelligence Network

echo.
echo ============================================================
echo   SWIN - Sentiment-driven Workflow Intelligence Network
echo ============================================================
echo.
echo Select what to run:
echo   1. Web Interface (Streamlit)
echo   2. Demo Workflow
echo   3. Run Tests
echo   4. Run Master Test
echo   5. Install Dependencies
echo   6. Check Configuration
echo   0. Exit
echo.
echo ============================================================
echo.

set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" goto streamlit
if "%choice%"=="2" goto demo
if "%choice%"=="3" goto tests
if "%choice%"=="4" goto master_tests
if "%choice%"=="5" goto install
if "%choice%"=="6" goto config
if "%choice%"=="0" goto exit
goto invalid

:streamlit
echo.
echo Starting Streamlit Web Interface...
echo Opening http://localhost:8501
echo.
python -m streamlit run streamlit_app.py
goto end

:demo
echo.
echo Running Demo Workflow...
echo.
python demo_langgraph_workflow.py
goto end

:tests
echo.
echo Running Pytest Tests...
echo.
python -m pytest tests/ -v --tb=short
goto end

:master_tests
echo.
echo Running Master Test Script...
echo.
python test_everything.py
goto end

:install
echo.
echo Installing Dependencies...
echo.
python -m pip install -r requirements.txt -U
echo.
echo Finished!
goto end

:config
echo.
echo Checking Configuration...
echo.
python check_dependencies.py
goto end

:invalid
echo.
echo Invalid choice. Please try again.
echo.
goto end

:exit
echo.
echo Goodbye!
echo.
exit /b

:end
echo.
pause
goto:eof
