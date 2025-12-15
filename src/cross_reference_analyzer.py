#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Reference Analyzer Module
Ενότητα Ανάλυσης Διασταυρούμενων Αναφορών

Builds and analyzes the network of relationships between legal articles. 
Uses graph theory to detect dependencies, conflicts, and circular references.
"""

import networkx as nx
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class CrossReferenceAnalyzer:
    """Analyzes cross-references between legal articles."""
    
    def __init__(self, articles: Dict, verbose: bool = False):
        self.articles = articles
        self.verbose = verbose
        self. graph = nx.DiGraph()
        self.chains = []
    
    def build_graph(self) -> nx.DiGraph:
        """Build directed graph of article relationships."""
        # Add nodes
        for article_no, article in self.articles.items():
            self.graph.add_node(
                article_no,
                title=article.title,
                has_constraints=bool(article.constraints),
                key_terms=article.key_terms
            )
        
        # Add edges (references)
        for article_no, article in self.articles.items():
            for ref in article.references_to:
                if ref in self.articles:
                    self.graph.add_edge(article_no, ref, relationship='references')
        
        # Special relationships for our interpretation
        self._add_interpretation_edges()
        
        if self.verbose:
            print(f"   📊 Γράφημα:  {self.graph.number_of_nodes()} κόμβοι, "
                  f"{self.graph.number_of_edges()} ακμές")
        
        return self.graph
    
    def _add_interpretation_edges(self):
        """Add specific edges relevant to the interpretation."""
        # Article 103 → Regulation 143 (enables summary administration)
        if '103' in self.graph and '143' in self.graph:
            self. graph.add_edge('103', '143', relationship='enables', critical=True)
        
        # Regulation 143 → Article 58 (modifies deadline)
        if '143' in self.graph and '58' in self.graph:
            self. graph.add_edge('143', '58', relationship='modifies', critical=True)
        
        # Article 27 → Article 16 (requires examination completion)
        if '27' in self.graph and '16' in self.graph:
            self. graph.add_edge('27', '16', relationship='requires', critical=True)
        
        # Article 28 → Article 27 (alternative to Article 27)
        if '28' in self.graph and '27' in self.graph:
            self.graph.add_edge('28', '27', relationship='alternative', critical=True)
    
    def find_interpretation_chain(self) -> List[str]:
        """
        Find the chain of articles relevant to the interpretation: 
        Article 103 → Regulation 143 → Article 58 → Article 27 → Article 16
        """
        chain = []
        
        # Primary chain: Summary administration to dividend timeline
        if '103' in self.graph:
            chain.append('103')
        if '143' in self.graph:
            chain.append('143')
        if '58' in self.graph:
            chain.append('58')
        
        # Rehabilitation chain
        if '27' in self.graph:
            chain. append('27')
        if '28' in self.graph:
            chain.append('28')
        if '16' in self.graph:
            chain.append('16')
        
        self.chains.append(('interpretation_chain', chain))
        
        if self.verbose:
            print(f"   🔗 Αλυσίδα ερμηνείας: {' → '.join(chain)}")
        
        return chain
    
    def detect_conflicts(self) -> List[Dict]:
        """Detect potential conflicts between articles."""
        conflicts = []
        
        # Conflict: Article 103(2) prohibition vs Regulation 143 modifications
        if '103' in self.articles and '143' in self.articles:
            art103 = self.articles['103']
            art143 = self.articles['143']
            
            if 'prohibition' in art103.constraints and 'modification' in art143.key_terms:
                conflicts.append({
                    'type': 'prohibition_vs_modification',
                    'articles': ['103', '143'],
                    'description': 'Άρθρο 103(2) απαγορεύει τροποποίηση εξέτασης, '
                                   'αλλά Κανονισμός 143 τροποποιεί προθεσμίες',
                    'severity': 'high',
                    'critical': True
                })
        
        # Conflict: 6-month timeline vs 4-year timeline
        if '143' in self.articles and '28' in self.articles:
            conflicts.append({
                'type':  'timeline_inconsistency',
                'articles':  ['143', '28'],
                'description': 'Κανονισμός 143: 6 μήνες vs Άρθρο 28: 4 έτη',
                'severity': 'medium',
                'critical': True
            })
        
        if self.verbose and conflicts:
            print(f"   ⚠️  Εντοπίστηκαν {len(conflicts)} πιθανές αντιφάσεις")
        
        return conflicts
    
    def analyze_article_103_constraint(self) -> Dict:
        """
        Deep analysis of Article 103(2) constraint:
        "no modification of examination or discharge provisions"
        """
        analysis = {
            'article':  '103',
            'constraint_text': '',
            'affects': [],
            'interpretation': '',
            'ambiguity_level': ''
        }
        
        if '103' not in self.articles:
            return analysis
        
        art103 = self.articles['103']
        
        # Extract the constraint
        for phrase in art103.critical_phrases:
            if 'δεν επιτρέπει' in phrase: 
                analysis['constraint_text'] = phrase
                break
        
        # What does this constraint affect?
        # Does modifying dividend timeline = modifying examination? 
        analysis['affects'] = ['examination_provisions', 'discharge_provisions']
        
        # Check if Regulation 143 violates this
        if '143' in self.articles:
            art143 = self.articles['143']
            
            # Regulation 143 modifies Article 58 (dividends)
            # Does this indirectly modify examination timeline?
            if '58' in art143.references_to:
                analysis['interpretation'] = (
                    'Κανονισμός 143 τροποποιεί προθεσμία μερίσματος (Άρθρο 58), '
                    'όχι απευθείας την εξέταση.  Ερώτημα: Αποτελεί αυτό έμμεση τροποποίηση;'
                )
                analysis['ambiguity_level'] = 'high'
        
        return analysis
    
    def count_relationships(self) -> int:
        """Count total relationships in graph."""
        return self.graph.number_of_edges()
    
    def get_article_dependencies(self, article_no: str) -> Dict[str, List[str]]: 
        """Get what an article depends on and what depends on it."""
        dependencies = {
            'depends_on': [],
            'depended_by': []
        }
        
        if article_no in self.graph:
            # What this article references
            dependencies['depends_on'] = list(self.graph. successors(article_no))
            # What references this article
            dependencies['depended_by'] = list(self.graph.predecessors(article_no))
        
        return dependencies
    
    def visualize_graph(self, output_file: str = 'outputs/reference_graph.png'):
        """Generate visualization of the reference graph."""
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 8))
            
            # Layout
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
            
            # Draw nodes
            critical_nodes = [n for n, d in self.graph.nodes(data=True) 
                            if d. get('has_constraints', False)]
            regular_nodes = [n for n in self.graph.nodes() if n not in critical_nodes]
            
            nx.draw_networkx_nodes(self.graph, pos, nodelist=critical_nodes,
                                 node_color='red', node_size=1500, alpha=0.8,
                                 label='Κρίσιμα Άρθρα')
            nx.draw_networkx_nodes(self.graph, pos, nodelist=regular_nodes,
                                 node_color='lightblue', node_size=1000, alpha=0.8)
            
            # Draw edges
            critical_edges = [(u, v) for u, v, d in self.graph.edges(data=True) 
                            if d.get('critical', False)]
            regular_edges = [(u, v) for u, v in self.graph.edges() 
                           if (u, v) not in critical_edges]
            
            nx.draw_networkx_edges(self.graph, pos, edgelist=critical_edges,
                                 edge_color='red', width=2, alpha=0.6,
                                 arrows=True, arrowsize=20)
            nx.draw_networkx_edges(self.graph, pos, edgelist=regular_edges,
                                 edge_color='gray', width=1, alpha=0.4,
                                 arrows=True, arrowsize=15)
            
            # Labels
            labels = {n: f"Άρθρο {n}" for n in self.graph.nodes()}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, 
                                  font_weight='bold')
            
            plt.title('Διάγραμμα Διασταυρούμενων Αναφορών\nCross-Reference Network',
                     fontsize=14, fontweight='bold')
            plt.legend()
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            if self.verbose:
                print(f"   📊 Διάγραμμα αποθηκεύτηκε: {output_file}")
            
        except ImportError:
            if self.verbose:
                print("   ⚠️  matplotlib δεν είναι εγκατεστημένο - παράλειψη οπτικοποίησης")


if __name__ == '__main__':
    # Test
    from legal_parser import LegalParser
    
    parser = LegalParser(verbose=True)
    articles = parser.load_all_articles()
    
    analyzer = CrossReferenceAnalyzer(articles, verbose=True)
    graph = analyzer.build_graph()
    
    print("\n🔍 Ανάλυση Άρθρου 103:")
    constraint_analysis = analyzer.analyze_article_103_constraint()
    print(f"   Περιορισμός: {constraint_analysis['constraint_text']}")
    print(f"   Ερμηνεία: {constraint_analysis['interpretation']}")
    
    print("\n⚠️  Πιθανές Αντιφάσεις:")
    conflicts = analyzer.detect_conflicts()
    for conflict in conflicts:
        print(f"   • {conflict['description']}")