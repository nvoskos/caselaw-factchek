@echo off
echo ═══════════════════════════════════════════════════════════
echo   Caselaw Fact-Checker - Quick Start
echo   Σύστημα Επαλήθευσης Νομικής Ερμηνείας
echo ═══════════════════════════════════════════════════════════
echo. 

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements. txt --quiet

REM Create outputs directory
if not exist "outputs" mkdir outputs

REM Run the analysis
echo. 
echo 🚀 Running bankruptcy law fact-check analysis... 
echo.
python bankruptcy_factcheck.py --verbose

echo. 
echo ✅ Analysis complete! 
echo 📄 Check the outputs\ directory for reports
echo.
pause