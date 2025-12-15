#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fact Checker Module
Ενότητα Επαλήθευσης Γεγονότων

Calculates final score and determines validity of interpretation. 
"""

from typing import Dict, List


class FactChecker:
    """Main fact-checking scorer."""
    
    def __init__(self, articles: Dict, logic_results: Dict, 
                 timeline_results: Dict, reasoning_results: Dict, verbose: bool = False):
        self.articles = articles
        self. logic_results = logic_results
        self.timeline_results = timeline_results
        self.reasoning_results = reasoning_results
        self.verbose = verbose
    
    def calculate_score(self) -> Dict:
        """Calculate final fact-check score."""
        score = {
            'total':  0,
            'max_total': 100,
            'text_support': 0,
            'logic_score': 0,
            'timeline_score': 0,
            'precedent':  0,
            'category': '',
            'confidence': '',
            'breakdown': {},
            'interpretation': '',
            'recommendation': ''
        }
        
        # Component 1: Legal text support (40 points)
        score['text_support'] = self._score_text_support()
        
        # Component 2: Logic (30 points) - from LogicValidator
        score['logic_score'] = self. logic_results. get('score', 0)
        
        # Component 3: Timeline (20 points) - from TimelineAnalyzer
        score['timeline_score'] = self.timeline_results.get('score', 0)
        
        # Component 4: Precedent (10 points)
        score['precedent'] = self._score_precedent()
        
        # Calculate total
        score['total'] = (
            score['text_support'] + 
            score['logic_score'] + 
            score['timeline_score'] + 
            score['precedent']
        )
        
        # Determine category
        score['category'] = self._determine_category(score['total'])
        score['confidence'] = self._determine_confidence(score)
        
        # Detailed breakdown
        score['breakdown'] = self._create_breakdown(score)
        
        # Generate interpretation
        score['interpretation'] = self._generate_interpretation(score)
        score['recommendation'] = self._generate_recommendation(score)
        
        if self.verbose:
            print(f"   ✓ Τελική βαθμολογία: {score['total']}/100 ({score['category']})")
        
        return score
    
    def _score_text_support(self) -> int:
        """Score direct support from legal text (0-40)."""
        score = 0
        
        # Factor 1: Article 103(2) prohibition (15 points)
        if '103' in self.articles:
            art103 = self.articles['103']
            if 'δεν επιτρέπει την τροποποίηση' in art103.text and 'εξέταση' in art103.text:
                score += 15
        
        # Factor 2: Regulation 143 modifications (12 points)
        if '143' in self.articles:
            art143 = self.articles['143']
            points = 0
            if 'έξι μήνες' in art143.text: 
                points += 6
            if 'ένα μόνο μέρισμα' in art143.text:
                points += 6
            score += points
        
        # Factor 3: Article 27 examination requirement (8 points)
        if '27' in self.articles:
            art27 = self.articles['27']
            if 'ολοκληρωθεί η δημόσια εξέταση' in art27.text:
                score += 8
        
        # Factor 4: Article 58 reference (5 points)
        if '58' in self.articles and '143' in self.articles:
            art143 = self.articles['143']
            if '58' in art143.text:
                score += 5
        
        return min(score, 40)
    
    def _score_precedent(self) -> int:
        """Score based on case law precedent (0-10)."""
        # Since we don't have access to case law, we score conservatively
        score = 5  # Neutral - no precedent found either way
        
        # In a real system, this would: 
        # - Search case law databases
        # - Find similar interpretations
        # - Score based on judicial support
        
        return score
    
    def _determine_category(self, total: int) -> str:
        """Determine interpretation category based on score."""
        if total >= 80:
            return "Ισχυρά Υποστηριζόμενη / Strongly Supported"
        elif total >= 65:
            return "Μετρίως Υποστηριζόμενη / Moderately Supported"
        elif total >= 50:
            return "Μερικώς Υποστηριζόμενη / Partially Supported"
        elif total >= 35:
            return "Αδύναμα Υποστηριζόμενη / Weakly Supported"
        else:
            return "Μη Υποστηριζόμενη / Not Supported"
    
    def _determine_confidence(self, score: Dict) -> str:
        """Determine confidence level."""
        total = score['total']
        
        # Check for critical ambiguities
        critical_ambiguities = len([
            amb for amb in self.reasoning_results. get('ambiguities', [])
            if amb. get('importance') == 'critical'
        ])
        
        if critical_ambiguities > 0:
            if total >= 70:
                return "Μέτρια Εμπιστοσύνη / Moderate Confidence"
            else:
                return "Χαμηλή Εμπιστοσύνη / Low Confidence"
        else:
            if total >= 70:
                return "Υψηλή Εμπιστοσύνη / High Confidence"
            elif total >= 50:
                return "Μέτρια Εμπιστοσύνη / Moderate Confidence"
            else:
                return "Χαμηλή Εμπιστοσύνη / Low Confidence"
    
    def _create_breakdown(self, score: Dict) -> Dict:
        """Create detailed score breakdown."""
        return {
            'text_support': {
                'score': score['text_support'],
                'max': 40,
                'percentage': (score['text_support'] / 40) * 100,
                'status': self._get_status(score['text_support'], 40)
            },
            'logic':  {
                'score': score['logic_score'],
                'max': 30,
                'percentage': (score['logic_score'] / 30) * 100,
                'status': self._get_status(score['logic_score'], 30)
            },
            'timeline': {
                'score': score['timeline_score'],
                'max': 20,
                'percentage': (score['timeline_score'] / 20) * 100,
                'status': self._get_status(score['timeline_score'], 20)
            },
            'precedent': {
                'score': score['precedent'],
                'max': 10,
                'percentage': (score['precedent'] / 10) * 100,
                'status': self._get_status(score['precedent'], 10)
            }
        }
    
    def _get_status(self, score: int, max_score: int) -> str:
        """Get status indicator for a score component."""
        percentage = (score / max_score) * 100
        if percentage >= 75:
            return "✓ Ισχυρό"
        elif percentage >= 50:
            return "⚠ Μέτριο"
        else:
            return "✗ Αδύναμο"
    
    def _generate_interpretation(self, score: Dict) -> str:
        """Generate interpretation of the score."""
        total = score['total']
        category = score['category']
        
        interpretation = f"ΣΥΝΟΛΙΚΗ ΑΞΙΟΛΟΓΗΣΗ: {total}/100 ({category})\n\n"
        
        if total >= 65:
            interpretation += (
                "Η ερμηνεία έχει ΜΕΤΡΙΑ ΕΩΣ ΙΣΧΥΡΗ νομική βάση.  Υπάρχουν σημαντικά "
                "υποστηρικτικά στοιχεία από το νομοθετικό κείμενο, ιδίως την απαγόρευση "
                "τροποποίησης του Άρθρου 103(2) και τις τροποποιήσεις του Κανονισμού 143. "
                "Ωστόσο, υπάρχουν κρίσιμες ασάφειες που απαιτούν περαιτέρω διευκρίνιση.\n\n"
            )
        elif total >= 50:
            interpretation += (
                "Η ερμηνεία έχει ΜΕΡΙΚΗ νομική βάση. Ενώ ορισμένα στοιχεία υποστηρίζουν "
                "την άποψη (π.χ.  Άρθρο 103(2), 6μηνη προθεσμία), υπάρχουν σημαντικά "
                "αντιφατικά στοιχεία (π.χ. 4ετής προθεσμία Άρθρου 28, διάκριση τομέων). "
                "Η ερμηνεία βασίζεται σε σιωπηρές λογικές συνδέσεις που δεν είναι ρητά "
                "καθορισμένες στο νομοθετικό κείμενο.\n\n"
            )
        else:
            interpretation += (
                "Η ερμηνεία έχει ΑΔΥΝΑΜΗ νομική βάση.  Τα αντιφατικά στοιχεία υπερτερούν "
                "των υποστηρικτικών.  Η σύνδεση μεταξύ της 6μηνης προθεσμίας μερίσματος "
                "και της υποχρέωσης αποκατάστασης δεν υποστηρίζεται επαρκώς από το "
                "νομοθετικό κείμενο.\n\n"
            )
        
        # Add key findings
        interpretation += "ΚΥΡΙΑ ΕΥΡΗΜΑΤΑ:\n\n"
        
        interpretation += "ΥΠΟΣΤΗΡΙΚΤΙΚΑ:\n"
        for factor in self.logic_results.get('supporting_factors', []):
            interpretation += f"  ✓ {factor}\n"
        
        interpretation += "\nΑΝΤΙΦΑΤΙΚΑ:\n"
        for factor in self.logic_results.get('contradicting_factors', []):
            interpretation += f"  ✗ {factor}\n"
        
        return interpretation
    
    def _generate_recommendation(self, score: Dict) -> str:
        """Generate recommendation based on score."""
        total = score['total']
        
        if total >= 70:
            recommendation = (
                "ΣΥΣΤΑΣΗ:  Η ερμηνεία έχει αξιόλογη νομική βάση αλλά απαιτεί "
                "επιβεβαίωση μέσω:\n"
                "  1. Έρευνας νομολογίας σε παρόμοιες υποθέσεις\n"
                "  2. Γνωμοδότησης ειδικού στο πτωχευτικό δίκαιο\n"
                "  3. Εξέτασης της πρακτικής του Επίσημου Παραλήπτη\n\n"
                "Εάν η υπόθεση προχωρήσει, υπάρχει λογική βάση για την επιχειρηματολογία."
            )
        elif total >= 50:
            recommendation = (
                "ΣΥΣΤΑΣΗ: Η ερμηνεία είναι ΑΜΦΙΛΕΓΟΜΕΝΗ.  Προτείνεται:\n"
                "  1. Ενδελεχής έρευνα νομολογίας\n"
                "  2. Ανάλυση νομοθετικής πρόθεσης Κανονισμού 143\n"
                "  3. Εξέταση εναλλακτικών ερμηνειών\n"
                "  4. Προετοιμασία για αντίλογο βάσει Άρθρου 28\n\n"
                "Η επιτυχία θα εξαρτηθεί από την ποιότητα της επιχειρηματολογίας "
                "και την προδιάθεση του Δικαστηρίου."
            )
        else:
            recommendation = (
                "ΣΥΣΤΑΣΗ: Η ερμηνεία έχει ΣΗΜΑΝΤΙΚΕΣ ΑΔΥΝΑΜΙΕΣ. Προτείνεται:\n"
                "  1. Επανεξέταση της νομικής στρατηγικής\n"
                "  2. Εξέταση εναλλακτικών νομικών βάσεων\n"
                "  3. Εστίαση σε ισχυρότερα επιχειρήματα\n\n"
                "Η προώθηση αυτής της ερμηνείας φέρει σημαντικό κίνδυνο απόρριψης."
            )
        
        return recommendation


if __name__ == '__main__':
    # Test
    from legal_parser import LegalParser
    from cross_reference_analyzer import CrossReferenceAnalyzer
    from logic_validator import LogicValidator
    from timeline_analyzer import TimelineAnalyzer
    from reasoning_engine import ReasoningEngine
    
    parser = LegalParser(verbose=True)
    articles = parser.load_all_articles()
    
    analyzer = CrossReferenceAnalyzer(articles, verbose=True)
    graph = analyzer.build_graph()
    
    validator = LogicValidator(articles, graph, verbose=True)
    logic_results = validator.validate_interpretation()
    
    timeline_analyzer = TimelineAnalyzer(articles, verbose=True)
    timeline_results = timeline_analyzer.analyze_deadlines()
    
    reasoning = ReasoningEngine(articles, graph, verbose=True)
    reasoning_results = reasoning.analyze()
    
    fact_checker = FactChecker(articles, logic_results, timeline_results, 
                               reasoning_results, verbose=True)
    final_score = fact_checker.calculate_score()
    
    print(f"\n{'='*70}")
    print("ΤΕΛΙΚΗ ΑΞΙΟΛΟΓΗΣΗ")
    print(f"{'='*70}")
    print(final_score['interpretation'])
    print(f"\n{final_score['recommendation']}")