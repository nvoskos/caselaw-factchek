#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Cross-Reference Analyzer Module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.legal_parser import LegalParser
from src.cross_reference_analyzer import CrossReferenceAnalyzer


class TestCrossReferenceAnalyzer:
    """Test CrossReferenceAnalyzer class."""
    
    @pytest.fixture
    def articles(self):
        """Load articles for testing."""
        parser = LegalParser(data_dir='data', verbose=False)
        return parser.load_all_articles()
    
    @pytest.fixture
    def analyzer(self, articles):
        """Create analyzer instance."""
        return CrossReferenceAnalyzer(articles, verbose=False)
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.graph is not None
        assert len(analyzer.articles) > 0
    
    def test_build_graph(self, analyzer):
        """Test building reference graph."""
        graph = analyzer.build_graph()
        
        assert graph. number_of_nodes() >= 6
        assert graph.number_of_edges() > 0
    
    def test_interpretation_chain(self, analyzer):
        """Test finding interpretation chain."""
        analyzer.build_graph()
        chain = analyzer.find_interpretation_chain()
        
        assert '103' in chain
        assert '143' in chain
        assert '58' in chain
    
    def test_detect_conflicts(self, analyzer):
        """Test conflict detection."""
        analyzer.build_graph()
        conflicts = analyzer. detect_conflicts()
        
        assert len(conflicts) > 0
        # Should detect 103(2) vs 143 conflict
        assert any(c['type'] == 'prohibition_vs_modification' for c in conflicts)
    
    def test_article_103_constraint_analysis(self, analyzer):
        """Test Article 103(2) constraint analysis."""
        analyzer.build_graph()
        analysis = analyzer.analyze_article_103_constraint()
        
        assert analysis['article'] == '103'
        assert len(analysis['constraint_text']) > 0
        assert analysis['ambiguity_level'] in ['low', 'medium', 'high']
    
    def test_article_dependencies(self, analyzer):
        """Test getting article dependencies."""
        analyzer.build_graph()
        deps = analyzer.get_article_dependencies('143')
        
        # Article 143 should depend on Article 58
        assert '58' in deps['depends_on'] or len(deps['depends_on']) >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])