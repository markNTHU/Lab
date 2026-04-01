@echo off
chcp 65001 >nul
echo ┌──────────────────────────────────────────────┐
echo │     Excel 轉 Obsidian 實驗紀錄小工具         │
echo └──────────────────────────────────────────────┘

:: 檢查是否有傳入檔案
if "%~1"=="" (
    echo.
    echo ❌ 錯誤：請直接將想轉換的 Excel 檔案「拖曳」到這個 .bat 檔案上方！
    echo.
    pause
    exit /b
)

echo.
echo 正在讀取並轉換： %~nx1
echo.

:: 執行 Python 腳本，並暫停讓使用者複製
python "c:\Users\markd\Obsidian\Obsidian\excel_to_md.py" "%~1"

echo.
pause
