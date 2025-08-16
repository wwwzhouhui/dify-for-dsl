@echo off
echo Starting Markdown to Mindmap Gradio App...
echo.
echo Please make sure you have installed:
echo 1. Python dependencies: pip install -r requirements.txt
echo 2. Node.js and markmap-cli: npm install -g markmap-cli
echo.
echo Starting server on http://localhost:16008
echo Press Ctrl+C to stop the server
echo.
python marp1_gradio.py
pause