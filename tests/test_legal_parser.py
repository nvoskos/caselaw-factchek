#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Legal Parser Module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys. path.insert(0, str(Path(__file__).parent.parent))

from src.legal_parser import LegalParser, LegalArticle


class TestLegalArticle:
    """Test LegalArticle class."""
    
    def test_article_creation(self):
        """Test creating a legal article."""
        article_data = {
            'articleNo': '103',
            'articleTitle': 'Test Article',
            'articleText': 'This article contains the word εξέταση and τροποποίηση.',
            'articleUrl': 'https://example.com',
            'lawTitle': 'Test Law'
        }
        
        article = LegalArticle(article_data)
        
        assert article.article_no == '103'
        assert article.title == 'Test Article'
        assert 'examination' in article.key_terms
        assert 'modification' in article.key_terms
    
    def test_constraint_detection(self):
        """Test detection of constraint phrases."""
        article_data = {
            'articleNo': '103',
            'articleTitle': 'Test',
            'articleText': 'αλλά καμιά διάταξη δεν επιτρέπει την τροποποίηση των διατάξεων που αφορούν την εξέταση',
            'articleUrl': 'https://example.com',
            'lawTitle': 'Test Law'
        }
        
        article = LegalArticle(article_data)
        
        assert 'prohibition' in article.constraints
        assert len(article.critical_phrases) > 0
    
    def test_reference_extraction(self):
        """Test extraction of article references."""
        article_data = {
            'articleNo': '143',
            'articleTitle': 'Test',
            'articleText': 'Αναφέρεται στο άρθρο 58 και στο άρθρου 103 του Νόμου.',
            'articleUrl': 'https://example.com',
            'lawTitle': 'Test Law'
        }
        
        article = LegalArticle(article_data)
        
        assert '58' in article.references_to
        assert '103' in article.references_to


class TestLegalParser:
    """Test LegalParser class."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return LegalParser(data_dir='data', verbose=False)
    
    def test_parser_initialization(self, parser):
        """Test parser initialization."""
        assert parser.data_dir. exists()
        assert isinstance(parser.articles, dict)
    
    def test_load_article_103(self, parser):
        """Test loading Article 103."""
        article = parser.load_article('article_103.json')
        
        assert article is not None
        assert article.article_no == '103'
        assert 'Συνοπτική διαχείριση' in article.title
        assert 'prohibition' in article.constraints
    
    def test_load_regulation_143(self, parser):
        """Test loading Regulation 143."""
        article = parser.load_article('regulation_143.json')
        
        assert article is not None
        assert article.article_no == '143'
        assert 'modification' in article.key_terms
    
    def test_load_all_articles(self, parser):
        """Test loading all articles."""
        articles = parser.load_all_articles()
        
        assert len(articles) >= 6
        assert '103' in articles
        assert '143' in articles
        assert '58' in articles
        assert '27' in articles
        assert '28' in articles
        assert '16' in articles
    
    def test_search_by_term(self, parser):
        """Test searching articles by term."""
        parser.load_all_articles()
        results = parser.search_by_term('εξέταση')
        
        assert len(results) > 0
        assert any(a.article_no == '103' for a in results)
    
    def test_get_critical_articles(self, parser):
        """Test getting critical articles."""
        parser.load_all_articles()
        critical = parser.get_critical_articles()
        
        assert len(critical) > 0
        assert any(a.article_no == '103' for a in critical)


class TestCrossReferences:
    """Test cross-reference building."""
    
    def test_cross_reference_building(self):
        """Test that cross-references are built correctly."""
        parser = LegalParser(data_dir='data', verbose=False)
        articles = parser.load_all_articles()
        
        # Article 143 should reference Article 103
        if '143' in articles:
            art143 = articles['143']
            assert '103' in art143.references_to or '58' in art143.references_to


if __name__ == '__main__': 
    pytest.main([__file__, '-v'])