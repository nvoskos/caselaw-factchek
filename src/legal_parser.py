#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legal Parser Module
Ενότητα Ανάλυσης Νομοθετικών Κειμένων

Parses legal articles from cylaw.org JSON format and extracts
key provisions, constraints, and cross-references. 
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class LegalArticle:
    """Represents a legal article with metadata and analysis."""
    
    def __init__(self, article_data: Dict):
        self.article_no = article_data. get('articleNo', '')
        self.title = article_data.get('articleTitle', '')
        self.text = article_data.get('articleText', '')
        self.url = article_data.get('articleUrl', '')
        self.law = article_data.get('lawTitle', '')
        
        # Extracted metadata
        self.key_terms = []
        self.constraints = []
        self.references_to = []
        self.referenced_by = []
        self. critical_phrases = []
        
        # Parse the article
        self._parse()
    
    def _parse(self):
        """Extract key information from article text."""
        # Identify critical constraint phrases
        if 'δεν επιτρέπει' in self.text or 'δεν επιτρέπεται' in self.text:
            self.constraints.append('prohibition')
            self.critical_phrases.append(self._extract_constraint_phrase())
        
        if 'τροποποίηση' in self.text:
            self.key_terms.append('modification')
            
        if 'εξέταση' in self.text or 'εξέτασης' in self.text:
            self.key_terms.append('examination')
            
        if 'απαλλαγή' in self.text:
            self.key_terms. append('discharge')
            
        if 'μέρισμα' in self.text:
            self.key_terms. append('dividend')
            
        if 'προθεσμία' in self. text:
            self.key_terms.append('deadline')
            
        if 'αποκατάσταση' in self.text:
            self.key_terms.append('rehabilitation')
        
        # Extract article references
        self._extract_references()
    
    def _extract_constraint_phrase(self) -> str:
        """Extract the full constraint phrase from text."""
        # Find sentences containing prohibition
        sentences = self.text.split('.')
        for sentence in sentences:
            if 'δεν επιτρέπει' in sentence or 'δεν επιτρέπεται' in sentence:
                return sentence. strip()
        return ""
    
    def _extract_references(self):
        """Extract references to other articles."""
        # Pattern:  άρθρο XX or άρθρου XX
        pattern = r'άρθρ[οου]\s+(\d+)'
        matches = re.findall(pattern, self.text, re.IGNORECASE)
        self.references_to = list(set(matches))
        
        # Pattern for subsections:  (1), (2), etc.
        subsection_pattern = r'\((\d+)\)'
        subsections = re.findall(subsection_pattern, self.text)
        
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'article_no': self.article_no,
            'title': self.title,
            'text':  self.text,
            'url': self.url,
            'law': self.law,
            'key_terms': self.key_terms,
            'constraints':  self.constraints,
            'references_to': self.references_to,
            'referenced_by':  self.referenced_by,
            'critical_phrases': self.critical_phrases
        }
    
    def __repr__(self):
        return f"<LegalArticle {self.article_no}:  {self.title}>"


class LegalParser:
    """Main parser for loading and analyzing legal articles."""
    
    def __init__(self, data_dir: str = 'data', verbose: bool = False):
        self.data_dir = Path(data_dir)
        self.verbose = verbose
        self.articles: Dict[str, LegalArticle] = {}
    
    def load_article(self, filename: str) -> Optional[LegalArticle]:
        """Load a single article from JSON file."""
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            if self.verbose:
                print(f"⚠️  Αρχείο δεν βρέθηκε: {filepath}")
            return None
        
        try: 
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle cylaw.org format
            if 'data' in data and 'articles' in data['data']:
                article_data = data['data']['articles'][0]
                article_data['lawTitle'] = data['metadata'].get('lawTitle', '')
                article_data['articleUrl'] = data['metadata'].get('sourceUrl', '')
            else:
                article_data = data
            
            article = LegalArticle(article_data)
            
            if self.verbose:
                print(f"   ✓ Φορτώθηκε:  Άρθρο {article.article_no}")
            
            return article
            
        except Exception as e:
            if self.verbose:
                print(f"✗ Σφάλμα κατά τη φόρτωση {filename}: {e}")
            return None
    
    def load_all_articles(self) -> Dict[str, LegalArticle]: 
        """Load all articles from data directory."""
        article_files = [
            'article_16.json',
            'article_27.json',
            'article_28.json',
            'article_58.json',
            'article_103.json',
            'regulation_143.json'
        ]
        
        for filename in article_files:
            article = self.load_article(filename)
            if article: 
                self.articles[article.article_no] = article
        
        # Build cross-reference relationships
        self._build_cross_references()
        
        return self.articles
    
    def _build_cross_references(self):
        """Build bidirectional cross-reference relationships."""
        for article_no, article in self.articles. items():
            for ref in article.references_to:
                if ref in self.articles:
                    self.articles[ref].referenced_by.append(article_no)
    
    def get_article(self, article_no: str) -> Optional[LegalArticle]: 
        """Get article by number."""
        return self. articles.get(article_no)
    
    def search_by_term(self, term: str) -> List[LegalArticle]: 
        """Search articles containing specific term."""
        results = []
        for article in self.articles.values():
            if term.lower() in article.text.lower() or term in article.key_terms:
                results.append(article)
        return results
    
    def get_critical_articles(self) -> List[LegalArticle]:
        """Get articles with critical constraints."""
        return [a for a in self.articles.values() if a.constraints]


if __name__ == '__main__': 
    # Test the parser
    parser = LegalParser(verbose=True)
    articles = parser.load_all_articles()
    
    print(f"\n📊 Φορτώθηκαν {len(articles)} άρθρα")
    
    # Show Article 103 analysis
    if '103' in articles:
        art103 = articles['103']
        print(f"\n🔍 Άρθρο 103 Ανάλυση:")
        print(f"   Όροι-Κλειδιά: {art103.key_terms}")
        print(f"   Περιορισμοί: {art103.constraints}")
        print(f"   Αναφέρεται σε: {art103.references_to}")
        print(f"   Κρίσιμες Φράσεις: {art103.critical_phrases}")