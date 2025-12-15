#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Timeline Analyzer Module
"""

import pytest
import sys
from pathlib import Path

sys. path.insert(0, str(Path(__file__).parent.parent))

from src.legal_parser import LegalParser
from src. timeline_analyzer import TimelineAnalyzer, Deadline


class TestDeadline:
    """Test Deadline dataclass."""
    
    def test_deadline_creation(self):
        """Test creating a deadline."""
        deadline = Deadline(
            article='58(2)',
            description='First dividend',
            duration='4 months',
            duration_days=120,
            trigger_event='First creditors meeting',
            mandatory=True,
            can_extend=True,
            extension_conditions='Sufficient reason'
        )
        
        assert deadline.article == '58(2)'
        assert deadline.duration_days == 120
        assert deadline.mandatory is True


class TestTimelineAnalyzer: 
    """Test TimelineAnalyzer class."""
    
    @pytest.fixture
    def articles(self):
        """Load articles."""
        parser = LegalParser(data_dir='data', verbose=False)
        return parser.load_all_articles()
    
    @pytest.fixture
    def analyzer(self, articles):
        """Create analyzer."""
        return TimelineAnalyzer(articles, verbose=False)
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.articles is not None
        assert len(analyzer.deadlines) == 0
    
    def test_analyze_deadlines(self, analyzer):
        """Test deadline analysis."""
        results = analyzer.analyze_deadlines()
        
        assert 'score' in results
        assert results['max_score'] == 20
        assert 0 <= results['score'] <= 20
        assert len(results['deadlines']) >= 3  # Should find 58(2), 143(i), 28
    
    def test_extract_deadlines(self, analyzer):
        """Test deadline extraction."""
        analyzer.analyze_deadlines()
        
        # Should extract key deadlines
        assert len(analyzer.deadlines) >= 3
        
        # Check for specific deadlines
        articles = [d.article for d in analyzer.deadlines]
        assert '58(2)' in articles or '143(i)' in articles
    
    def test_four_month_deadline(self, analyzer):
        """Test 4-month deadline detection."""
        analyzer.analyze_deadlines()
        
        four_month = next((d for d in analyzer.deadlines if d.article == '58(2)'), None)
        
        if four_month:
            assert four_month.duration == '4 μήνες'
            assert four_month.duration_days == 120
            assert four_month. mandatory is True
    
    def test_six_month_deadline(self, analyzer):
        """Test 6-month deadline detection."""
        analyzer. analyze_deadlines()
        
        six_month = next((d for d in analyzer.deadlines if d.article == '143(i)'), None)
        
        if six_month: 
            assert six_month.duration == '6 μήνες'
            assert six_month.duration_days == 180
    
    def test_four_year_deadline(self, analyzer):
        """Test 4-year deadline detection."""
        analyzer.analyze_deadlines()
        
        four_year = next((d for d in analyzer.deadlines if d. article == '28'), None)
        
        if four_year: 
            assert '4' in four_year.duration or 'τέσσερα' in four_year.duration
            assert four_year.duration_days == 1460
    
    def test_timeline_consistency(self, analyzer):
        """Test timeline consistency check."""
        results = analyzer.analyze_deadlines()
        
        assert 'conflicts' in results
        # Should detect 6-month vs 4-year conflict
        assert len(results['conflicts']) > 0
    
    def test_critical_finding(self, analyzer):
        """Test critical finding generation."""
        results = analyzer.analyze_deadlines()
        
        assert 'critical_finding' in results
        assert len(results['critical_finding']) > 0
        assert 'ΚΡΙΣΙΜΟ ΕΥΡΗΜΑ' in results['critical_finding']
    
    def test_timeline_chart(self, analyzer):
        """Test timeline chart generation."""
        results = analyzer.analyze_deadlines()
        
        assert 'timeline_chart' in results
        assert 'events' in results['timeline_chart']
        assert len(results['timeline_chart']['events']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])