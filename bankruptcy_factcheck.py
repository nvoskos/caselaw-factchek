#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bankruptcy Law Fact-Checking System
Σύστημα Επαλήθευσης Νομικής Ερμηνείας - Πτωχευτικό Δίκαιο Κύπρου

Main CLI application for analyzing legal interpretations
regarding Cyprus Bankruptcy Law (Chapter 5) and Regulation 368/1931. 
"""

import click
import json
from pathlib import Path
from datetime import datetime
from src.legal_parser import LegalParser
from src.cross_reference_analyzer import CrossReferenceAnalyzer
from src.logic_validator import LogicValidator
from src. timeline_analyzer import TimelineAnalyzer
from src.reasoning_engine import ReasoningEngine
from src.fact_checker import FactChecker
from src.report_generator import ReportGenerator


@click.command()
@click.option('--data-dir', default='data', help='Directory containing legal article JSON files')
@click.option('--output-dir', default='outputs', help='Directory for generated reports')
@click.option('--format', default='html', type=click.Choice(['html', 'markdown', 'json']), 
              help='Output report format')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def main(data_dir, output_dir, format, verbose):
    """
    Αναλύει τη νομική ερμηνεία σχετικά με τη συνοπτική διαχείριση πτώχευσης. 
    
    Analyzes legal interpretation regarding summary bankruptcy administration.
    """
    click.echo("═" * 70)
    click.echo("  ΣΥΣΤΗΜΑ ΕΠΑΛΗΘΕΥΣΗΣ ΝΟΜΙΚΗΣ ΕΡΜΗΝΕΙΑΣ")
    click.echo("  Legal Fact-Checking System")
    click.echo("  Πτωχευτικό Δίκαιο Κύπρου - Cyprus Bankruptcy Law")
    click.echo("═" * 70)
    click.echo()
    
    # Initialize components
    parser = LegalParser(data_dir, verbose=verbose)
    
    # Step 1: Load legal articles
    click.echo("📄 Φόρτωση νομοθετικών κειμένων...")
    articles = parser.load_all_articles()
    click.echo(f"   ✓ Φορτώθηκαν {len(articles)} άρθρα\n")
    
    # Step 2: Cross-reference analysis
    click.echo("🔗 Ανάλυση διασταυρούμενων αναφορών...")
    cross_ref = CrossReferenceAnalyzer(articles, verbose=verbose)
    reference_graph = cross_ref.build_graph()
    click.echo(f"   ✓ Εντοπίστηκαν {cross_ref.count_relationships()} σχέσεις\n")
    
    # Step 3: Logic validation
    click.echo("⚖️  Επαλήθευση λογικής συνοχής...")
    logic_validator = LogicValidator(articles, reference_graph, verbose=verbose)
    logic_results = logic_validator.validate_interpretation()
    click.echo(f"   ✓ Βαθμολογία: {logic_results['score']}/30\n")
    
    # Step 4: Timeline analysis
    click.echo("⏱️  Ανάλυση χρονοδιαγράμματος...")
    timeline = TimelineAnalyzer(articles, verbose=verbose)
    timeline_results = timeline.analyze_deadlines()
    click.echo(f"   ✓ Βαθμολογία:  {timeline_results['score']}/20\n")
    
    # Step 5: Legal reasoning
    click.echo("🧠 Εφαρμογή αρχών νομικής ερμηνείας...")
    reasoning = ReasoningEngine(articles, reference_graph, verbose=verbose)
    reasoning_results = reasoning.analyze()
    click.echo(f"   ✓ Εναλλακτικές ερμηνείες: {len(reasoning_results['alternatives'])}\n")
    
    # Step 6: Fact-checking score
    click.echo("📊 Υπολογισμός τελικής βαθμολογίας...")
    fact_checker = FactChecker(
        articles, 
        logic_results, 
        timeline_results, 
        reasoning_results,
        verbose=verbose
    )
    final_score = fact_checker.calculate_score()
    click.echo(f"   ✓ Συνολική βαθμολογία: {final_score['total']}/100")
    click.echo(f"   ✓ Κατηγορία: {final_score['category']}\n")
    
    # Step 7: Generate report
    click.echo("📝 Δημιουργία αναφοράς...")
    report_gen = ReportGenerator(
        articles,
        reference_graph,
        logic_results,
        timeline_results,
        reasoning_results,
        final_score,
        verbose=verbose
    )
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bankruptcy_factcheck_{timestamp}.{format}"
    output_file = output_path / filename
    
    if format == 'html':
        report_gen.generate_html(output_file)
    elif format == 'markdown':
        report_gen.generate_markdown(output_file)
    else: 
        report_gen.generate_json(output_file)
    
    click.echo(f"   ✓ Αναφορά αποθηκεύτηκε: {output_file}\n")
    
    # Summary
    click.echo("═" * 70)
    click.echo("ΠΕΡΙΛΗΨΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ / RESULTS SUMMARY")
    click.echo("═" * 70)
    click.echo(f"Συνολική Βαθμολογία:  {final_score['total']}/100")
    click.echo(f"Κατηγορία: {final_score['category']}")
    click.echo(f"Επίπεδο Εμπιστοσύνης: {final_score['confidence']}")
    click.echo("─" * 70)
    click.echo(f"Υποστήριξη Κειμένου: {final_score['text_support']}/40")
    click.echo(f"Λογική Συνοχή: {logic_results['score']}/30")
    click.echo(f"Χρονοδιάγραμμα: {timeline_results['score']}/20")
    click.echo(f"Νομολογία: {final_score['precedent']}/10")
    click.echo("═" * 70)
    click.echo()
    
    if final_score['total'] >= 70:
        click.secho("✓ Η ερμηνεία έχει ισχυρή νομική βάση", fg='green', bold=True)
    elif final_score['total'] >= 50:
        click.secho("⚠ Η ερμηνεία έχει μερική νομική βάση", fg='yellow', bold=True)
    else:
        click.secho("✗ Η ερμηνεία έχει αδύναμη νομική βάση", fg='red', bold=True)
    
    click.echo()
    click.echo(f"Πλήρης αναφορά: {output_file}")
    click.echo()


if __name__ == '__main__':
    main()