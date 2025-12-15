#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Generator Module
Ενότητα Δημιουργίας Αναφοράς

Generates comprehensive fact-checking reports in multiple formats. 
"""

import json
import networkx as nx
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """Generates comprehensive fact-checking reports."""
    
    def __init__(self, articles: Dict, reference_graph: nx.DiGraph,
                 logic_results: Dict, timeline_results: Dict,
                 reasoning_results: Dict, final_score: Dict, verbose: bool = False):
        self.articles = articles
        self.graph = reference_graph
        self. logic_results = logic_results
        self.timeline_results = timeline_results
        self.reasoning_results = reasoning_results
        self.final_score = final_score
        self.verbose = verbose
        self.timestamp = datetime.now()
    
    def generate_html(self, output_file: str):
        """Generate HTML report."""
        html = self._create_html_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        if self.verbose:
            print(f"   ✓ HTML αναφορά:  {output_file}")
    
    def generate_markdown(self, output_file: str):
        """Generate Markdown report."""
        md = self._create_markdown_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        if self.verbose:
            print(f"   ✓ Markdown αναφορά: {output_file}")
    
    def generate_json(self, output_file: str):
        """Generate JSON report."""
        report_data = {
            'timestamp':  self.timestamp. isoformat(),
            'interpretation': self.reasoning_results['primary_interpretation']['statement'],
            'final_score': self.final_score,
            'logic_results': self.logic_results,
            'timeline_results':  self.timeline_results,
            'reasoning_results': self.reasoning_results,
            'articles_analyzed': list(self.articles.keys())
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"   ✓ JSON αναφορά: {output_file}")
    
    def _create_html_report(self) -> str:
        """Create HTML report content."""
        total = self.final_score['total']
        category = self.final_score['category']
        
        # Determine color scheme based on score
        if total >= 70:
            color_class = "success"
            color_hex = "#28a745"
        elif total >= 50:
            color_class = "warning"
            color_hex = "#ffc107"
        else:
            color_class = "danger"
            color_hex = "#dc3545"
        
        html = f"""<! DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Αναφορά Επαλήθευσης Νομικής Ερμηνείας</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background:  #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        
        . header {{
            text-align:  center;
            border-bottom: 3px solid {color_hex};
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .header . subtitle {{
            font-size: 1.2em;
            color: #7f8c8d;
        }}
        
        .score-box {{
            background: linear-gradient(135deg, {color_hex} 0%, {color_hex}dd 100%);
            color: white;
            padding: 30px;
            border-radius:  8px;
            text-align: center;
            margin:  30px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        . score-box . score {{
            font-size:  4em;
            font-weight:  bold;
            margin: 10px 0;
        }}
        
        .score-box . category {{
            font-size: 1.5em;
            margin-top: 10px;
        }}
        
        .section {{
            margin:  40px 0;
        }}
        
        .section h2 {{
            font-size: 1.8em;
            color: #2c3e50;
            border-left: 5px solid {color_hex};
            padding-left: 15px;
            margin-bottom:  20px;
        }}
        
        .section h3 {{
            font-size: 1.4em;
            color: #34495e;
            margin:  25px 0 15px 0;
        }}
        
        .interpretation-box {{
            background: #ecf0f1;
            padding: 25px;
            border-radius:  8px;
            border-left: 5px solid #3498db;
            margin:  20px 0;
        }}
        
        .interpretation-box p {{
            font-size: 1.1em;
            line-height: 1.8;
        }}
        
        .breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .breakdown-item {{
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        
        .breakdown-item h4 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        
        .breakdown-item . score-display {{
            font-size: 2. 5em;
            font-weight: bold;
            color: {color_hex};
            margin:  15px 0;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: {color_hex};
            transition: width 0.3s ease;
        }}
        
        .check-list {{
            list-style: none;
            padding: 0;
        }}
        
        .check-list li {{
            padding: 12px;
            margin: 10px 0;
            border-left: 4px solid #ddd;
            background: #f9f9f9;
        }}
        
        .check-list li.support {{
            border-left-color: #28a745;
            background: #d4edda;
        }}
        
        .check-list li.contradict {{
            border-left-color: #dc3545;
            background: #f8d7da;
        }}
        
        .check-list li.neutral {{
            border-left-color: #ffc107;
            background: #fff3cd;
        }}
        
        .article-reference {{
            background: #f8f9fa;
            padding: 15px;
            border-radius:  5px;
            margin: 15px 0;
            border:  1px solid #dee2e6;
        }}
        
        .article-reference . article-no {{
            font-weight: bold;
            color: #007bff;
            font-size: 1.1em;
        }}
        
        .article-reference .article-text {{
            margin-top: 10px;
            font-style: italic;
            color: #555;
        }}
        
        .timeline-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        .timeline-table th,
        .timeline-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .timeline-table th {{
            background: {color_hex};
            color:  white;
            font-weight:  bold;
        }}
        
        .timeline-table tr:hover {{
            background: #f5f5f5;
        }}
        
        .alternatives {{
            margin: 30px 0;
        }}
        
        .alternative-item {{
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .alternative-item h4 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .alternative-item .probability {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius:  20px;
            font-size:  0.9em;
            margin-bottom: 10px;
        }}
        
        . ambiguity-box {{
            background:  #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        
        .ambiguity-box . issue {{
            font-weight: bold;
            color: #856404;
            margin-bottom: 10px;
        }}
        
        . recommendation-box {{
            background: #d1ecf1;
            border-left: 5px solid #17a2b8;
            padding: 25px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .recommendation-box h3 {{
            color: #0c5460;
            margin-bottom: 15px;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
        }}
        
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        .metadata table {{
            width: 100%;
        }}
        
        .metadata td {{
            padding: 8px;
        }}
        
        .metadata td:first-child {{
            font-weight: bold;
            width: 200px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 ΑΝΑΦΟΡΑ ΕΠΑΛΗΘΕΥΣΗΣ ΝΟΜΙΚΗΣ ΕΡΜΗΝΕΙΑΣ</h1>
            <p class="subtitle">Legal Fact-Checking Report</p>
            <p class="subtitle">Πτωχευτικό Δίκαιο Κύπρου - Cyprus Bankruptcy Law</p>
        </div>
        
        <div class="metadata">
            <table>
                <tr>
                    <td>Ημερομηνία Ανάλυσης: </td>
                    <td>{self.timestamp. strftime('%d/%m/%Y %H:%M:%S')}</td>
                </tr>
                <tr>
                    <td>Άρθρα που Αναλύθηκαν:</td>
                    <td>{', '.join(sorted(self.articles.keys()))}</td>
                </tr>
                <tr>
                    <td>Σύστημα Ανάλυσης:</td>
                    <td>Caselaw Fact-Checker v1.0</td>
                </tr>
            </table>
        </div>
        
        <div class="score-box">
            <div>ΣΥΝΟΛΙΚΗ ΒΑΘΜΟΛΟΓΙΑ</div>
            <div class="score">{total}/100</div>
            <div class="category">{category}</div>
            <div style="margin-top: 15px; font-size: 1.1em;">
                Επίπεδο Εμπιστοσύνης: {self.final_score['confidence']}
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 ΕΡΜΗΝΕΙΑ ΠΡΟΣ ΕΠΑΛΗΘΕΥΣΗ</h2>
            <div class="interpretation-box">
                <p><strong>Ελληνικά:</strong><br>
                {self.reasoning_results['primary_interpretation']['statement']}</p>
                <p style="margin-top: 15px;"><strong>English:</strong><br>
                {self.reasoning_results['primary_interpretation']['english']}</p>
            </div>
            
            <h3>Λογική Αλυσίδα Ερμηνείας: </h3>
            <ul class="check-list">
"""
        
        for step in self.reasoning_results['primary_interpretation']['logical_chain']:
            html += f"                <li class='neutral'>{step}</li>\n"
        
        html += f"""            </ul>
            
            <h3>Κεντρική Υπόθεση:</h3>
            <div class="interpretation-box" style="background: #fff3cd; border-left-color: #ffc107;">
                <p>{self.reasoning_results['primary_interpretation']['key_assumption']}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 ΑΝΑΛΥΣΗ ΒΑΘΜΟΛΟΓΙΑΣ</h2>
            
            <div class="breakdown">
"""
        
        for component, data in self.final_score['breakdown'].items():
            html += f"""                <div class="breakdown-item">
                    <h4>{component. replace('_', ' ').title()}</h4>
                    <div class="score-display">{data['score']}/{data['max']}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['percentage']}%;"></div>
                    </div>
                    <p style="margin-top: 10px;">{data['status']}</p>
                </div>
"""
        
        html += """            </div>
        </div>
        
        <div class="section">
            <h2>⚖️ ΛΟΓΙΚΗ ΕΠΑΛΗΘΕΥΣΗ</h2>
"""
        
        for check in self.logic_results['checks']:
            status_class = 'support' if check['supports_interpretation'] else 'contradict'
            html += f"""            <div class="article-reference">
                <div class="article-no">✓ {check['description']}</div>
                <p><strong>Πόντοι:</strong> {check['points_awarded']}/{check['points_possible']}</p>
                <p style="margin-top: 10px;">{check['analysis']}</p>
            </div>
"""
        
        html += """        </div>
        
        <div class="section">
            <h2>⏱️ ΑΝΑΛΥΣΗ ΧΡΟΝΟΔΙΑΓΡΑΜΜΑΤΟΣ</h2>
            
            <h3>Προθεσμίες που Εντοπίστηκαν: </h3>
            <table class="timeline-table">
                <thead>
                    <tr>
                        <th>Άρθρο</th>
                        <th>Περιγραφή</th>
                        <th>Διάρκεια</th>
                        <th>Γεγονός Ενεργοποίησης</th>
                        <th>Υποχρεωτική</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for deadline in self.timeline_results['deadlines']:
            mandatory = "Ναι" if deadline['mandatory'] else "Όχι"
            html += f"""                    <tr>
                        <td><strong>{deadline['article']}</strong></td>
                        <td>{deadline['description']}</td>
                        <td>{deadline['duration']}</td>
                        <td>{deadline['trigger_event']}</td>
                        <td>{mandatory}</td>
                    </tr>
"""
        
        html += """                </tbody>
            </table>
            
            <div class="ambiguity-box">
                <div class="issue">ΚΡΙΣΙΜΟ ΕΥΡΗΜΑ: </div>
"""
        
        html += f"                <p>{self.timeline_results['critical_finding']. replace(chr(10), '<br>')}</p>\n"
        
        html += """            </div>
        </div>
        
        <div class="section">
            <h2>🔄 ΕΝΑΛΛΑΚΤΙΚΕΣ ΕΡΜΗΝΕΙΕΣ</h2>
            <div class="alternatives">
"""
        
        for alt in self.reasoning_results['alternatives']:
            html += f"""                <div class="alternative-item">
                    <h4>{alt['title']}</h4>
                    <div class="probability">Πιθανότητα:  {alt['probability']}</div>
                    <p style="margin:  15px 0;"><strong>{alt['statement']}</strong></p>
                    <h5>Επιχειρηματολογία:</h5>
                    <ul>
"""
            for reason in alt['reasoning']:
                html += f"                        <li>{reason}</li>\n"
            
            html += f"""                    </ul>
                    <p style="margin-top: 10px;"><strong>Ισχύς:</strong> {alt['strength']. capitalize()}</p>
                </div>
"""
        
        html += """            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ ΚΡΙΣΙΜΕΣ ΑΣΑΦΕΙΕΣ</h2>
"""
        
        for amb in self.reasoning_results['ambiguities']: 
            html += f"""            <div class="ambiguity-box">
                <div class="issue">{amb['issue']}</div>
                <p><strong>Ερώτημα:</strong> {amb['question']}</p>
                <p><strong>Σημασία:</strong> {amb['importance']. capitalize()}</p>
                <p><strong>Απαιτείται:</strong> {amb['resolution_needed']}</p>
            </div>
"""
        
        html += f"""        </div>
        
        <div class="section">
            <h2>📋 ΤΕΛΙΚΗ ΑΞΙΟΛΟΓΗΣΗ</h2>
            <div class="interpretation-box">
                {self.final_score['interpretation']. replace(chr(10), '<br>')}
            </div>
        </div>
        
        <div class="section">
            <h2>💡 ΣΥΣΤΑΣΕΙΣ</h2>
            <div class="recommendation-box">
                <h3>Προτεινόμενα Επόμενα Βήματα:</h3>
                {self.final_score['recommendation'].replace(chr(10), '<br>')}
            </div>
            
            <h3>Προτεραιότητες Έρευνας:</h3>
            <ol>
"""
        
        for rec in self.reasoning_results['recommendations']:
            html += f"""                <li>
                    <strong>{rec['title']}</strong><br>
                    {rec['description']}
                </li>
"""
        
        html += """            </ol>
        </div>
        
        <div class="section">
            <h2>📚 ΑΝΑΦΟΡΕΣ ΝΟΜΟΘΕΤΙΚΩΝ ΚΕΙΜΕΝΩΝ</h2>
"""
        
        for article_no, article in sorted(self.articles.items()):
            html += f"""            <div class="article-reference">
                <div class="article-no">Άρθρο {article_no}:  {article. title}</div>
                <div class="article-text">{article.text[: 300]}...</div>
                <p style="margin-top:  10px;">
                    <a href="{article.url}" target="_blank">🔗 Πλήρες κείμενο στο cylaw.org</a>
                </p>
            </div>
"""
        
        html += f"""        </div>
        
        <div class="footer">
            <p><strong>Αναφορά δημιουργήθηκε: </strong> {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Caselaw Fact-Checker System | Πτωχευτικό Δίκαιο Κύπρου</p>
            <p style="margin-top: 15px; font-size: 0.9em; color: #999;">
                Η παρούσα αναφορά παρέχεται για ενημερωτικούς σκοπούς και δεν αποτελεί νομική συμβουλή. 
                <br>This report is provided for informational purposes and does not constitute legal advice.
            </p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _create_markdown_report(self) -> str:
        """Create Markdown report content."""
        total = self.final_score['total']
        category = self.final_score['category']
        
        md = f"""# 📊 ΑΝΑΦΟΡΑ ΕΠΑΛΗΘΕΥΣΗΣ ΝΟΜΙΚΗΣ ΕΡΜΗΝΕΙΑΣ
## Legal Fact-Checking Report
### Πτωχευτικό Δίκαιο Κύπρου - Cyprus Bankruptcy Law

---

**Ημερομηνία Ανάλυσης:** {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}  
**Άρθρα που Αναλύθηκαν:** {', '.join(sorted(self.articles.keys()))}  
**Σύστημα Ανάλυσης:** Caselaw Fact-Checker v1.0

---

## 🎯 ΣΥΝΟΛΙΚΗ ΒΑΘΜΟΛΟΓΙΑ
