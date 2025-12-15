#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caselaw Fact-Checker Package
Πακέτο Επαλήθευσης Νομικής Ερμηνείας

A comprehensive system for fact-checking legal interpretations
in Cyprus Bankruptcy Law.
"""

__version__ = "1.0.0"
__author__ = "Caselaw Fact-Checker Team"
__description__ = "Legal Fact-Checking System for Cyprus Bankruptcy Law"

from .legal_parser import LegalParser, LegalArticle
from .cross_reference_analyzer import CrossReferenceAnalyzer
from .logic_validator import LogicValidator
from .timeline_analyzer import TimelineAnalyzer, Deadline
from .reasoning_engine import ReasoningEngine
from .fact_checker import FactChecker
from . report_generator import ReportGenerator

__all__ = [
    'LegalParser',
    'LegalArticle',
    'CrossReferenceAnalyzer',
    'LogicValidator',
    'TimelineAnalyzer',
    'Deadline',
    'ReasoningEngine',
    'FactChecker',
    'ReportGenerator',
]