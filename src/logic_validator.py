#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logic Validator Module
Ενότητα Επαλήθευσης Λογικής

Validates the logical consistency of the legal interpretation. 
Checks if Regulation 143 modifications violate Article 103(2) constraints.
"""

import networkx as nx
from typing import Dict, List, Tuple


class LogicValidator:
    """Validates logical consistency of legal interpretation."""
    
    def __init__(self, articles: Dict, reference_graph: nx.DiGraph, verbose: bool = False):
        self.articles = articles
        self.graph = reference_graph
        self. verbose = verbose
        self.validation_results = {}
    
    def validate_interpretation(self) -> Dict:
        """
        Main validation of the interpretation:
        "Official Receiver must proceed with rehabilitation at 6-month deadline"
        """
        results = {
            'score': 0,
            'max_score': 30,
            'checks': [],
            'summary': '',
            'supporting_factors': [],
            'contradicting_factors': []
        }
        
        # Check 1: Article 103(2) prohibition exists (8 points)
        check1 = self._check_prohibition_exists()
        results['checks'].append(check1)
        results['score'] += check1['points_awarded']
        
        # Check 2: Regulation 143 modifies timelines (7 points)
        check2 = self._check_regulation_143_modifications()
        results['checks'].append(check2)
        results['score'] += check2['points_awarded']
        
        # Check 3: Does timeline modification = examination modification?  (10 points)
        check3 = self._check_modification_equivalence()
        results['checks'].append(check3)
        results['score'] += check3['points_awarded']
        
        # Check 4: Single dividend implies completion?  (5 points)
        check4 = self._check_single_dividend_implication()
        results['checks']. append(check4)
        results['score'] += check4['points_awarded']
        
        # Compile supporting/contradicting factors
        for check in results['checks']:
            if check['supports_interpretation']:
                results['supporting_factors'].append(check['description'])
            else:
                results['contradicting_factors'].append(check['description'])
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        if self.verbose:
            print(f"   ✓ Λογική επαλήθευση: {results['score']}/{results['max_score']}")
        
        return results
    
    def _check_prohibition_exists(self) -> Dict:
        """
        Check if Article 103(2) prohibition clearly exists. 
        """
        check = {
            'name': 'article_103_prohibition',
            'description': 'Άρθρο 103(2): Απαγόρευση τροποποίησης διατάξεων εξέτασης',
            'points_possible': 8,
            'points_awarded': 0,
            'supports_interpretation':  False,
            'evidence': [],
            'analysis': ''
        }
        
        if '103' not in self.articles:
            check['analysis'] = 'Άρθρο 103 δεν βρέθηκε'
            return check
        
        art103 = self.articles['103']
        
        # Check for prohibition language
        prohibition_found = False
        constraint_text = ''
        
        for phrase in art103.critical_phrases:
            if 'δεν επιτρέπει την τροποποίηση' in phrase and 'εξέταση' in phrase:
                prohibition_found = True
                constraint_text = phrase
                break
        
        if prohibition_found: 
            check['points_awarded'] = 8
            check['supports_interpretation'] = True
            check['evidence']. append(f"Κείμενο: \"{constraint_text}\"")
            check['analysis'] = (
                "Το Άρθρο 103(2) απαγορεύει ρητά την τροποποίηση διατάξεων που αφορούν "
                "την εξέταση του χρεώστη. Αυτό αποτελεί ισχυρή υποστήριξη ότι η διαδικασία "
                "εξέτασης δεν μπορεί να αλλοιωθεί σε συνοπτική διαχείριση."
            )
        else:
            check['points_awarded'] = 3
            check['analysis'] = 'Η απαγόρευση υπάρχει αλλά είναι ασαφής'
        
        return check
    
    def _check_regulation_143_modifications(self) -> Dict:
        """
        Check if Regulation 143 actually modifies timelines.
        """
        check = {
            'name': 'regulation_143_modifications',
            'description': 'Κανονισμός 143: Τροποποίηση προθεσμίας σε 6 μήνες',
            'points_possible': 7,
            'points_awarded':  0,
            'supports_interpretation': False,
            'evidence': [],
            'analysis': ''
        }
        
        if '143' not in self.articles:
            check['analysis'] = 'Κανονισμός 143 δεν βρέθηκε'
            return check
        
        art143 = self.articles['143']
        
        # Check for timeline modification
        six_months_found = 'έξι μήνες' in art143.text
        single_dividend_found = 'ένα μόνο μέρισμα' in art143.text
        modifies_58 = '58' in art143.references_to
        
        points = 0
        if six_months_found:
            points += 3
            check['evidence'].append("Παράταση προθεσμίας σε 6 μήνες (Κανονισμός 143(i))")
        
        if single_dividend_found:
            points += 2
            check['evidence'].append("Διανομή σε ένα μόνο μέρισμα (Κανονισμός 143(ii))")
        
        if modifies_58:
            points += 2
            check['evidence'].append("Αναφέρεται στο Άρθρο 58(2)")
        
        check['points_awarded'] = points
        check['supports_interpretation'] = points >= 5
        
        check['analysis'] = (
            f"Ο Κανονισμός 143 επιβεβαιώνεται ότι:  "
            f"{'(1) παρατείνει την προθεσμία σε 6 μήνες, ' if six_months_found else ''}"
            f"{'(2) προβλέπει ένα μόνο μέρισμα, ' if single_dividend_found else ''}"
            f"{'(3) τροποποιεί το Άρθρο 58(2).' if modifies_58 else ''}"
        )
        
        return check
    
    def _check_modification_equivalence(self) -> Dict:
        """
        Critical check:  Does modifying dividend timeline = modifying examination? 
        This is the KEY ambiguity in the interpretation.
        """
        check = {
            'name': 'modification_equivalence',
            'description': 'Τροποποίηση χρόνου μερίσματος = Τροποποίηση εξέτασης;',
            'points_possible':  10,
            'points_awarded': 0,
            'supports_interpretation': False,
            'evidence': [],
            'analysis': '',
            'ambiguity_level': 'high'
        }
        
        # This is the crux of the legal argument
        
        # Supporting argument: Timeline modifications affect examination schedule
        supporting_logic = [
            "Άρθρο 27 απαιτεί ολοκλήρωση εξέτασης πριν την αποκατάσταση",
            "Κανονισμός 143 ορίζει 6μηνη προθεσμία για μέρισμα",
            "Ένα μόνο μέρισμα σημαίνει ταχεία ολοκλήρωση",
            "Αν η εξέταση δεν μπορεί να τροποποιηθεί, πρέπει να ολοκληρωθεί εντός 6 μηνών"
        ]
        
        # Contradicting argument: Different legal domains
        contradicting_logic = [
            "Άρθρο 103(2) αναφέρεται σε 'διατάξεις εξέτασης' (examination provisions)",
            "Κανονισμός 143 αναφέρεται σε 'προθεσμία μερίσματος' (dividend deadline)",
            "Το μέρισμα είναι οικονομική διαδικασία, όχι διαδικασία εξέτασης",
            "Άρθρο 28 δίνει 4ετή προθεσμία, όχι 6μηνη"
        ]
        
        # Score based on logical strength
        # The interpretation has SOME merit but is not conclusive
        
        # Award partial points:  The argument has logic but is ambiguous
        check['points_awarded'] = 4  # Out of 10 - reflects ambiguity
        check['supports_interpretation'] = False  # Not strongly supported
        
        check['evidence'] = supporting_logic + contradicting_logic
        
        check['analysis'] = (
            "ΚΡΙΣΙΜΗ ΑΣΑΦΕΙΑ: Υπάρχει νομική διάκριση μεταξύ:\n"
            "  (α) 'διατάξεων που αφορούν την εξέταση' (Άρθρο 103(2))\n"
            "  (β) 'προθεσμίας διανομής μερίσματος' (Κανονισμός 143(i))\n\n"
            "Η ερμηνεία προϋποθέτει ότι η τροποποίηση της προθεσμίας μερίσματος "
            "αποτελεί έμμεση τροποποίηση της διαδικασίας εξέτασης.  Αυτό ΔΥΝΑΤΟΝ "
            "να είναι αληθές αλλά ΔΕΝ είναι ρητά καθορισμένο στο νομοθετικό κείμενο.\n\n"
            "Το Άρθρο 28 προβλέπει προθεσμία 4 ετών για αποκατάσταση, όχι 6 μηνών, "
            "γεγονός που υποδηλώνει ότι οι δύο χρονοδιαγράμματα μπορεί να είναι ανεξάρτητα."
        )
        
        return check
    
    def _check_single_dividend_implication(self) -> Dict:
        """
        Check if single dividend distribution implies mandatory rehabilitation.
        """
        check = {
            'name': 'single_dividend_implication',
            'description': 'Ένα μόνο μέρισμα → Υποχρέωση αποκατάστασης;',
            'points_possible':  5,
            'points_awarded': 0,
            'supports_interpretation': False,
            'evidence': [],
            'analysis': ''
        }
        
        if '143' not in self.articles:
            return check
        
        art143 = self.articles['143']
        
        # Check for single dividend language
        single_dividend = 'ένα μόνο μέρισμα' in art143.text
        
        if single_dividend:
            # The logic:  single dividend = estate liquidated = process complete
            # Therefore:  rehabilitation should follow? 
            
            # This is WEAK logic - just because estate is liquidated doesn't mean
            # automatic rehabilitation
            
            check['points_awarded'] = 2  # Weak support
            check['supports_interpretation'] = False
            
            check['evidence']. append(
                "Κανονισμός 143(ii): Διανομή σε ένα μόνο μέρισμα κατά την ρευστοποίηση"
            )
            
            check['analysis'] = (
                "Η διανομή σε ένα μόνο μέρισμα υποδηλώνει ταχεία ολοκλήρωση της "
                "ρευστοποίησης. Ωστόσο, αυτό ΔΕΝ δημιουργεί αυτόματα υποχρέωση "
                "αποκατάστασης του χρεώστη.  Τα Άρθρα 27-28 διέπουν την αποκατάσταση "
                "και δεν αναφέρουν ρητή σύνδεση με το χρονοδιάγραμμα μερίσματος."
            )
        else:
            check['analysis'] = 'Δεν βρέθηκε αναφορά σε ένα μόνο μέρισμα'
        
        return check
    
    def _generate_summary(self, results: Dict) -> str:
        """Generate summary of logic validation."""
        score_pct = (results['score'] / results['max_score']) * 100
        
        if score_pct >= 70:
            rating = "ΙΣΧΥΡΗ"
        elif score_pct >= 50:
            rating = "ΜΕΤΡΙΑ"
        else: 
            rating = "ΑΔΥΝΑΜΗ"
        
        summary = f"Λογική Συνοχή: {rating} ({results['score']}/{results['max_score']})\n\n"
        
        summary += "ΥΠΟΣΤΗΡΙΚΤΙΚΑ ΣΤΟΙΧΕΙΑ:\n"
        for i, factor in enumerate(results['supporting_factors'], 1):
            summary += f"  {i}. {factor}\n"
        
        summary += "\nΑΝΤΙΦΑΤΙΚΑ ΣΤΟΙΧΕΙΑ:\n"
        for i, factor in enumerate(results['contradicting_factors'], 1):
            summary += f"  {i}. {factor}\n"
        
        return summary
    
    def validate_article_chain(self) -> Dict:
        """
        Validate the logical chain:  103 → 143 → 58 → 27
        """
        chain_validation = {
            'valid': True,
            'breaks':  [],
            'chain':  ['103', '143', '58', '27', '28', '16']
        }
        
        # Check each link
        if '103' in self.graph and '143' in self.graph:
            if not self. graph. has_edge('103', '143'):
                chain_validation['breaks'].append(('103', '143'))
        
        if '143' in self. graph and '58' in self. graph:
            if not self. graph.has_edge('143', '58'):
                chain_validation['breaks'].append(('143', '58'))
        
        chain_validation['valid'] = len(chain_validation['breaks']) == 0
        
        return chain_validation


if __name__ == '__main__':
    # Test
    from legal_parser import LegalParser
    from cross_reference_analyzer import CrossReferenceAnalyzer
    
    parser = LegalParser(verbose=True)
    articles = parser.load_all_articles()
    
    analyzer = CrossReferenceAnalyzer(articles, verbose=True)
    graph = analyzer.build_graph()
    
    validator = LogicValidator(articles, graph, verbose=True)
    results = validator.validate_interpretation()
    
    print(f"\n📊 ΑΠΟΤΕΛΕΣΜΑΤΑ ΛΟΓΙΚΗΣ ΕΠΑΛΗΘΕΥΣΗΣ")
    print("=" * 60)
    print(results['summary'])
    
    print("\nΛΕΠΤΟΜΕΡΕΙΕΣ ΕΛΕΓΧΩΝ:")
    for check in results['checks']:
        print(f"\n✓ {check['description']}")
        print(f"   Πόντοι: {check['points_awarded']}/{check['points_possible']}")
        print(f"   Ανάλυση: {check['analysis'][: 200]}...")