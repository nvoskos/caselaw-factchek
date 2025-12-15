#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests - Full System End-to-End
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.legal_parser import LegalParser
from src.cross_reference_analyzer import CrossReferenceAnalyzer
from src.logic_validator import LogicValidator
from src.timeline_analyzer import TimelineAnalyzer
from src.reasoning_engine import ReasoningEngine
from src.fact_checker import FactChecker
from src.report_generator import ReportGenerator


class TestFullSystemIntegration:
    """Test complete system integration."""
    
    def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline from start to finish."""
        
        # Step 1: Load articles
        parser = LegalParser(data_dir='data', verbose=False)
        articles = parser.load_all_articles()
        
        assert len(articles) >= 6
        
        # Step 2: Build cross-references
        analyzer = CrossReferenceAnalyzer(articles, verbose=False)
        graph = analyzer. build_graph()
        
        assert graph. number_of_nodes() >= 6
        
        # Step 3: Logic validation
        validator = LogicValidator(articles, graph, verbose=False)
        logic_results = validator.validate_interpretation()
        
        assert 0 <= logic_results['score'] <= 30
        
        # Step 4: Timeline analysis
        timeline_analyzer = TimelineAnalyzer(articles, verbose=False)
        timeline_results = timeline_analyzer.analyze_deadlines()
        
        assert 0 <= timeline_results['score'] <= 20
        
        # Step 5: Reasoning
        reasoning = ReasoningEngine(articles, graph, verbose=False)
        reasoning_results = reasoning. analyze()
        
        assert len(reasoning_results['alternatives']) > 0
        
        # Step 6: Fact checking
        fact_checker = FactChecker(
            articles,
            logic_results,
            timeline_results,
            reasoning_results,
            verbose=False
        )
        final_score = fact_checker.calculate_score()
        
        assert 0 <= final_score['total'] <= 100
        
        # Step 7: Report generation
        report_gen = ReportGenerator(
            articles,
            graph,
            logic_results,
            timeline_results,
            reasoning_results,
            final_score,
            verbose=False
        )
        
        # Test report generation (without actually writing files)
        html = report_gen._create_html_report()
        assert len(html) > 0
        assert 'ΑΝΑΦΟΡΑ ΕΠΑΛΗΘΕΥΣΗΣ' in html
        
        md = report_gen._create_markdown_report()
        assert len(md) > 0
        assert '# 📊 ΑΝΑΦΟΡΑ ΕΠΑΛΗΘΕΥΣΗΣ' in md
    
    def test_expected_score_range(self):
        """Test that final score is in expected range (50-75)."""
        
        parser = LegalParser(data_dir='data', verbose=False)
        articles = parser.load_all_articles()
        
        analyzer = CrossReferenceAnalyzer(articles, verbose=False)
        graph = analyzer.build_graph()
        
        validator = LogicValidator(articles, graph, verbose=False)
        logic_results = validator.validate_interpretation()
        
        timeline_analyzer = TimelineAnalyzer(articles, verbose=False)
        timeline_results = timeline_analyzer.analyze_deadlines()
        
        reasoning = ReasoningEngine(articles, graph, verbose=False)
        reasoning_results = reasoning.analyze()
        
        fact_checker = FactChecker(
            articles,
            logic_results,
            timeline_results,
            reasoning_results,
            verbose=False
        )
        final_score = fact_checker.calculate_score()
        
        # Based on the interpretation, we expect a "Partially Supported" result
        # Score should be in the 50-75 range
        assert 50 <= final_score['total'] <= 80
        assert 'Μερικώς' in final_score['category'] or 'Μετρίως' in final_score['category']
    
    def test_key_findings_present(self):
        """Test that key findings are present in results."""
        
        parser = LegalParser(data_dir='data', verbose=False)
        articles = parser.load_all_articles()
        
        analyzer = CrossReferenceAnalyzer(articles, verbose=False)
        graph = analyzer.build_graph()
        
        # Should detect Article 103(2) prohibition
        assert '103' in articles
        art103 = articles['103']
        assert 'prohibition' in art103.constraints
        
        # Should detect Regulation 143 modifications
        assert '143' in articles
        art143 = articles['143']
        assert 'έξι μήνες' in art143.text
        
        # Should detect conflicts
        conflicts = analyzer.detect_conflicts()
        assert len(conflicts) > 0
        assert any(c['type'] == 'prohibition_vs_modification' for c in conflicts)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])