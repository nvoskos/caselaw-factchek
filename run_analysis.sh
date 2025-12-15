#!/bin/bash
# Quick start script for Caselaw Fact-Checker

echo "═══════════════════════════════════════════════════════════"
echo "  Caselaw Fact-Checker - Quick Start"
echo "  Σύστημα Επαλήθευσης Νομικής Ερμηνείας"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create outputs directory
mkdir -p outputs

# Run the analysis
echo ""
echo "🚀 Running bankruptcy law fact-check analysis..."
echo ""
python bankruptcy_factcheck.py --verbose

echo ""
echo "✅ Analysis complete!"
echo "📄 Check the outputs/ directory for reports"
echo ""