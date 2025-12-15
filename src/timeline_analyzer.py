#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timeline Analyzer Module
Ενότητα Ανάλυσης Χρονοδιαγράμματος

Analyzes temporal requirements and deadlines across articles. 
Key tension: 6-month dividend deadline vs 4-year rehabilitation deadline. 
"""

import re
from typing import Dict, List, Tuple, Optional
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class Deadline:
    """Represents a legal deadline."""
    article: str
    description: str
    duration: str
    duration_days: int
    trigger_event: str
    mandatory: bool
    can_extend: bool
    extension_conditions: Optional[str] = None


class TimelineAnalyzer:
    """Analyzes timelines and deadlines in bankruptcy proceedings."""
    
    def __init__(self, articles: Dict, verbose: bool = False):
        self.articles = articles
        self.verbose = verbose
        self. deadlines: List[Deadline] = []
    
    def analyze_deadlines(self) -> Dict:
        """Main timeline analysis for the interpretation."""
        results = {
            'score': 0,
            'max_score': 20,
            'deadlines': [],
            'conflicts': [],
            'timeline_chart': {},
            'critical_finding': ''
        }
        
        # Extract all deadlines
        self._extract_deadlines()
        results['deadlines'] = [self._deadline_to_dict(d) for d in self.deadlines]
        
        # Score based on timeline coherence
        score_breakdown = {
            'deadline_clarity': 0,  # Max 5
            'consistency': 0,  # Max 8
            'implication_strength': 0  # Max 7
        }
        
        # Check 1: Are deadlines clearly stated?
        score_breakdown['deadline_clarity'] = self._score_deadline_clarity()
        
        # Check 2: Are timelines consistent?
        score_breakdown['consistency'], conflicts = self._check_timeline_consistency()
        results['conflicts'] = conflicts
        
        # Check 3: Does 6-month deadline imply rehabilitation obligation?
        score_breakdown['implication_strength'] = self._score_implication_strength()
        
        results['score'] = sum(score_breakdown.values())
        results['score_breakdown'] = score_breakdown
        
        # Generate critical finding
        results['critical_finding'] = self._generate_critical_finding()
        
        # Build timeline chart
        results['timeline_chart'] = self._build_timeline_chart()
        
        if self.verbose:
            print(f"   ✓ Χρονοδιάγραμμα: {results['score']}/{results['max_score']}")
        
        return results
    
    def _extract_deadlines(self):
        """Extract all deadlines from articles."""
        
        # Article 58(2): 4 months for first dividend
        if '58' in self.articles:
            art58 = self. articles['58']
            if 'τέσσερις μήνες' in art58.text:
                self.deadlines.append(Deadline(
                    article='58(2)',
                    description='Πρώτο μέρισμα',
                    duration='4 μήνες',
                    duration_days=120,
                    trigger_event='Πέρας πρώτης συνέλευσης πιστωτών',
                    mandatory=True,
                    can_extend=True,
                    extension_conditions='Επαρκής λόγος προς εποπτική επιτροπή'
                ))
        
        # Regulation 143(i): Extension to 6 months
        if '143' in self.articles:
            art143 = self.articles['143']
            if 'έξι μήνες' in art143.text:
                self.deadlines.append(Deadline(
                    article='143(i)',
                    description='Πρώτο μέρισμα (συνοπτική διαχείριση)',
                    duration='6 μήνες',
                    duration_days=180,
                    trigger_event='Πέρας πρώτης συνέλευσης πιστωτών',
                    mandatory=False,
                    can_extend=False,
                    extension_conditions='Κατά την κρίση Επίσημου Παραλήπτη'
                ))
        
        # Article 28: 4 years for rehabilitation
        if '28' in self. articles:
            art28 = self.articles['28']
            if 'τέσσερα χρόνια' in art28.text or 'τέσσερις ετών' in art28.text:
                self.deadlines.append(Deadline(
                    article='28',
                    description='Αίτηση αποκατάστασης από Επίσημο Παραλήπτη',
                    duration='4 έτη',
                    duration_days=1460,
                    trigger_event='Συμπλήρωση δημόσιας εξέτασης',
                    mandatory=True,
                    can_extend=False,
                    extension_conditions=None
                ))
        
        if self.verbose:
            print(f"   ⏱️  Εντοπίστηκαν {len(self.deadlines)} προθεσμίες")
    
    def _score_deadline_clarity(self) -> int:
        """Score how clearly deadlines are stated (0-5)."""
        score = 0
        
        # Check if we found the key deadlines
        articles_with_deadlines = [d.article for d in self.deadlines]
        
        if '58(2)' in articles_with_deadlines:
            score += 2
        if '143(i)' in articles_with_deadlines:
            score += 2
        if '28' in articles_with_deadlines:
            score += 1
        
        return min(score, 5)
    
    def _check_timeline_consistency(self) -> Tuple[int, List[Dict]]:
        """Check if timelines are consistent.  Returns (score, conflicts)."""
        conflicts = []
        score = 8  # Start with full points, deduct for conflicts
        
        # Major conflict: 6 months vs 4 years
        six_month_deadline = next((d for d in self.deadlines if d.article == '143(i)'), None)
        four_year_deadline = next((d for d in self.deadlines if d.article == '28'), None)
        
        if six_month_deadline and four_year_deadline:
            conflicts.append({
                'type': 'timeline_mismatch',
                'severity': 'high',
                'articles': ['143(i)', '28'],
                'description': (
                    f"Κανονισμός 143: {six_month_deadline.duration} για μέρισμα vs "
                    f"Άρθρο 28: {four_year_deadline.duration} για αποκατάσταση"
                ),
                'analysis': (
                    "Η ερμηνεία προϋποθέτει ότι η 6μηνη προθεσμία μερίσματος "
                    "δημιουργεί υποχρέωση αποκατάστασης, αλλά το Άρθρο 28 δίνει "
                    "4 έτη στον Επίσημο Παραλήπτη. Αυτό υποδηλώνει ότι τα δύο "
                    "χρονοδιαγράμματα μπορεί να είναι ανεξάρτητα."
                )
            })
            score -= 5  # Major deduction
        
        # Check if single dividend timeline aligns with examination
        if six_month_deadline: 
            conflicts.append({
                'type':  'implicit_connection',
                'severity': 'medium',
                'articles': ['143(i)', '27'],
                'description': (
                    "Δεν υπάρχει ρητή σύνδεση μεταξύ της 6μηνης προθεσμίας "
                    "μερίσματος και της υποχρέωσης αποκατάστασης"
                ),
                'analysis':  (
                    "Η ερμηνεία βασίζεται σε σιωπηρή λογική:  6 μήνες → ένα μέρισμα → "
                    "ολοκλήρωση → αποκατάσταση. Αυτή η αλυσίδα δεν είναι νομικά "
                    "καθορισμένη."
                )
            })
            score -= 2
        
        return max(score, 0), conflicts
    
    def _score_implication_strength(self) -> int:
        """
        Score:  Does the 6-month deadline imply rehabilitation obligation?
        This is the core of the interpretation.
        """
        score = 0  # Out of 7
        
        # Check if we have the 6-month deadline
        six_month = next((d for d in self. deadlines if d.article == '143(i)'), None)
        
        if not six_month:
            return 0
        
        # Factor 1: Is it mandatory?  (No - discretionary)
        if not six_month.mandatory:
            score += 0  # Discretionary weakens the argument
        else:
            score += 3
        
        # Factor 2: Single dividend provision
        if '143' in self.articles and 'ένα μόνο μέρισμα' in self.articles['143']. text:
            score += 2  # Single dividend suggests finality
        
        # Factor 3: Connection to rehabilitation articles
        if '27' in self.articles:
            art27 = self.articles['27']
            # Article 27 requires examination completion, not timeline
            if 'ολοκληρωθεί η δημόσια εξέταση' in art27.text:
                score += 1  # Weak connection
        
        # Factor 4: Article 28's 4-year window contradicts
        if '28' in self. articles:
            score -= 1  # Contradiction weakens implication
        
        return max(score, 0)
    
    def _generate_critical_finding(self) -> str:
        """Generate the critical finding about timelines."""
        finding = (
            "ΚΡΙΣΙΜΟ ΕΥΡΗΜΑ ΧΡΟΝΟΔΙΑΓΡΑΜΜΑΤΟΣ:\n\n"
            "Υπάρχει ασυμφωνία μεταξύ δύο χρονικών προθεσμιών:\n\n"
            "1. ΚΑΝΟΝΙΣΜΟΣ 143(i): 6 μήνες για διανομή πρώτου μερίσματος\n"
            "   • Διακριτική ευχέρεια Επίσημου Παραλήπτη\n"
            "   • Αφορά ρευστοποίηση περιουσίας και διανομή\n"
            "   • Συνδυάζεται με 'ένα μόνο μέρισμα'\n\n"
            "2. ΑΡΘΡΟ 28: 4 έτη για αίτηση αποκατάστασης\n"
            "   • Υποχρεωτική προθεσμία για Επίσημο Παραλήπτη\n"
            "   • Αφορά αποκατάσταση πτωχεύσαντα\n"
            "   • Μετράται από συμπλήρωση δημόσιας εξέτασης\n\n"
            "Η ερμηνεία υποστηρίζει ότι η 6μηνη προθεσμία δημιουργεί υποχρέωση\n"
            "άμεσης αποκατάστασης, αλλά το Άρθρο 28 δίνει 4ετή προθεσμία.\n\n"
            "ΕΡΩΤΗΜΑ: Τροποποιεί ο Κανονισμός 143 σιωπηρά το Άρθρο 28, ή είναι\n"
            "τα δύο χρονοδιαγράμματα ανεξάρτητα (μέρισμα vs αποκατάσταση);"
        )
        
        return finding
    
    def _build_timeline_chart(self) -> Dict:
        """Build a timeline chart showing key events."""
        chart = {
            'events': [],
            'critical_path': []
        }
        
        # Event 0: Bankruptcy declared
        chart['events'].append({
            'day': 0,
            'event': 'Κήρυξη σε πτώχευση',
            'article': '103',
            'type': 'start'
        })
        
        # Event 1: First creditors meeting (assume day 30)
        chart['events'].append({
            'day': 30,
            'event': 'Πρώτη συνέλευση πιστωτών',
            'article':  '58',
            'type': 'trigger'
        })
        
        # Event 2: First dividend deadline (normal)
        chart['events'].append({
            'day': 150,  # 30 + 120
            'event': 'Προθεσμία πρώτου μερίσματος (κανονική)',
            'article': '58(2)',
            'type':  'deadline'
        })
        
        # Event 3: First dividend deadline (summary administration)
        chart['events'].append({
            'day': 210,  # 30 + 180
            'event': 'Προθεσμία πρώτου μερίσματος (συνοπτική)',
            'article': '143(i)',
            'type':  'deadline_critical'
        })
        
        # Event 4: Rehabilitation deadline
        chart['events'].append({
            'day': 1490,  # 30 + 1460
            'event': 'Προθεσμία αίτησης αποκατάστασης',
            'article': '28',
            'type': 'deadline'
        })
        
        # Critical path: The interpretation suggests this path
        chart['critical_path'] = [
            {'day': 0, 'event': 'Κήρυξη πτώχευσης'},
            {'day': 30, 'event': 'Συνέλευση πιστωτών'},
            {'day':  210, 'event': 'Διανομή μερίσματος'},
            {'day': 210, 'event': 'ΥΠΟΤΙΘΕΜΕΝΗ αποκατάσταση (σύμφωνα με ερμηνεία)'}
        ]
        
        return chart
    
    def _deadline_to_dict(self, deadline: Deadline) -> Dict:
        """Convert Deadline to dictionary."""
        return {
            'article': deadline.article,
            'description': deadline.description,
            'duration': deadline.duration,
            'duration_days': deadline. duration_days,
            'trigger_event': deadline.trigger_event,
            'mandatory': deadline. mandatory,
            'can_extend': deadline.can_extend,
            'extension_conditions': deadline. extension_conditions
        }


if __name__ == '__main__':
    # Test
    from legal_parser import LegalParser
    
    parser = LegalParser(verbose=True)
    articles = parser.load_all_articles()
    
    analyzer = TimelineAnalyzer(articles, verbose=True)
    results = analyzer.analyze_deadlines()
    
    print(f"\n📊 ΑΝΑΛΥΣΗ ΧΡΟΝΟΔΙΑΓΡΑΜΜΑΤΟΣ")
    print("=" * 60)
    print(f"Βαθμολογία: {results['score']}/{results['max_score']}")
    print(f"\nΠροθεσμίες που εντοπίστηκαν:  {len(results['deadlines'])}")
    
    for deadline in results['deadlines']:
        print(f"\n• {deadline['article']}: {deadline['description']}")
        print(f"  Διάρκεια: {deadline['duration']}")
        print(f"  Υποχρεωτική: {'Ναι' if deadline['mandatory'] else 'Όχι'}")
    
    print(f"\n{results['critical_finding']}")