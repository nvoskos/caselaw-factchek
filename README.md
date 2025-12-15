# 📊 Caselaw Fact-Checker

## Σύστημα Επαλήθευσης Νομικής Ερμηνείας | Legal Fact-Checking System

Ένα ολοκληρωμένο σύστημα ανάλυσης και επαλήθευσης νομικών ερμηνειών για το Πτωχευτικό Δίκαιο της Κύπρου. 

A comprehensive system for analyzing and fact-checking legal interpretations in Cyprus Bankruptcy Law (Chapter 5) and Bankruptcy Procedural Regulation (368/1931).

---

## 🎯 Σκοπός | Purpose

Το σύστημα αναλύει τη νομική ερμηνεία: 

> "Ο Επίσημος Παραλήπτης όφειλε να προχωρήσει την αποκατάσταση του χρεώστη στο τέλος της προθεσμίας των 6 μηνών σε συνοπτική διαχείριση"

**English:**
> "The Official Receiver should have proceeded with the debtor's rehabilitation at the end of the 6-month deadline in summary administration"

---

## 🔍 Κεντρικό Νομικό Ερώτημα | Core Legal Question

**Ελληνικά:**
Σε συνοπτική διαχείριση (Άρθρο 103), όταν: 
- Η προθεσμία μερίσματος παρατείνεται σε 6 μήνες (Κανονισμός 143)
- Η περιουσία διανέμεται σε ένα μόνο μέρισμα
- Το Άρθρο 103(2) **δεν επιτρέπει τροποποίηση** διατάξεων εξέτασης

**Ερώτημα:** Υποχρεώνεται ο Επίσημος Παραλήπτης να προχωρήσει την αποκατάσταση εντός 6 μηνών;

**English:**
In summary administration (Article 103), when:
- The dividend deadline is extended to 6 months (Regulation 143)
- The estate is distributed in a single dividend
- Article 103(2) **does not permit modification** of examination provisions

**Question:** Is the Official Receiver obligated to proceed with rehabilitation within 6 months?

---

## 📦 Εγκατάσταση | Installation

### Προαπαιτούμενα | Prerequisites

- Python 3.9 or higher
- pip package manager

### Βήματα | Steps

```bash
# Clone the repository
git clone https://github.com/nvoskos/caselaw-factchek.git
cd caselaw-factchek

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Χρήση | Usage

### Βασική Χρήση | Basic Usage

```bash
python bankruptcy_factcheck.py
```

### Επιλογές | Options

```bash
# Specify output directory
python bankruptcy_factcheck.py --output-dir reports

# Choose output format
python bankruptcy_factcheck. py --format markdown

# Enable verbose mode
python bankruptcy_factcheck.py --verbose

# Full example
python bankruptcy_factcheck.py \
  --data-dir data \
  --output-dir outputs \
  --format html \
  --verbose
```

### Διαθέσιμες Μορφές | Available Formats

- `html` - Πλήρης HTML αναφορά με οπτικοποιήσεις (default)
- `markdown` - Markdown αναφορά για documentation
- `json` - Δομημένα δεδομένα για περαιτέρω ανάλυση

---

## 📊 Μεθοδολογία Ανάλυσης | Analysis Methodology

Το σύστημα χρησιμοποιεί 4 κριτήρια βαθμολόγησης: 

### 1. Υποστήριξη από Νομοθετικό Κείμενο (40 πόντοι)
- Ύπαρξη ρητών διατάξεων
- Αναφορές μεταξύ άρθρων
- Κρίσιμες φράσεις και περιορισμοί

### 2. Λογική Συνοχή (30 πόντοι)
- Συνέπεια ερμηνείας
- Έλεγχος αντιφάσεων
- Αλυσίδα λογικής

### 3. Χρονοδιάγραμμα (20 πόντοι)
- Συνέπεια προθεσμιών
- Αλληλουχία γεγονότων
- Σιωπηρές υποχρεώσεις

### 4. Νομολογία (10 πόντοι)
- Υποστήριξη από δικαστικές αποφάσεις
- Προηγούμενα precedents

---

## 📁 Δομή Έργου | Project Structure

```
caselaw-factchek/
├── README.md                    # Αυτό το αρχείο
├── requirements.txt             # Python dependencies
├── config.yaml                  # Ρυθμίσεις συστήματος
├── bankruptcy_factcheck.py      # Κύριο script
├── src/                         # Πηγαίος κώδικας
│   ├── __init__.py
│   ├── legal_parser.py          # Ανάλυση νομοθετικών κειμένων
│   ├── cross_reference_analyzer.py  # Διασταυρούμενες αναφορές
│   ├── logic_validator.py       # Λογική επαλήθευση
│   ├── timeline_analyzer.py     # Ανάλυση χρονοδιαγράμματος
│   ├── reasoning_engine.py      # Μηχανή ερμηνείας
│   ├── fact_checker.py          # Βαθμολόγηση
│   └── report_generator.py      # Δημιουργία αναφορών
├── data/                        # Νομοθετικά δεδομένα
│   ├── article_103.json
│   ├── regulation_143.json
│   ├── article_58.json
│   ├── article_27.json
│   ├── article_28.json
│   └── article_16.json
├── tests/                       # Unit tests
│   └── test_*. py
└── outputs/                     # Αναφορές (generated)
    └── .gitkeep
```

---

## 🔬 Ενότητες Συστήματος | System Modules

### 1. Legal Parser (`legal_parser.py`)
Φορτώνει και αναλύει νομοθετικά κείμενα από cylaw.org JSON format. 

**Χαρακτηριστικά:**
- Εξαγωγή βασικών όρων και περιορισμών
- Εντοπισμός διασταυρούμενων αναφορών
- Υποστήριξη ελληνικών κειμένων (UTF-8)

### 2. Cross-Reference Analyzer (`cross_reference_analyzer.py`)
Χτίζει γράφημα σχέσεων μεταξύ άρθρων.

**Χαρακτηριστικά:**
- Directed graph με NetworkX
- Εντοπισμός αλυσίδων ερμηνείας
- Ανίχνευση αντιφάσεων

### 3. Logic Validator (`logic_validator.py`)
Ελέγχει τη λογική συνοχή της ερμηνείας. 

**Έλεγχοι:**
- Ύπαρξη απαγόρευσης Άρθρου 103(2)
- Τροποποιήσεις Κανονισμού 143
- Ισοδυναμία τροποποιήσεων
- Συνεπαγωγή ενός μερίσματος

### 4. Timeline Analyzer (`timeline_analyzer.py`)
Αναλύει προθεσμίες και χρονοδιαγράμματα.

**Αναλύει:**
- 4 μήνες → 6 μήνες (Άρθρο 58 → Κανονισμός 143)
- 4ετής προθεσμία (Άρθρο 28)
- Σύγκρουση χρονοδιαγραμμάτων

### 5. Reasoning Engine (`reasoning_engine.py`)
Εφαρμόζει αρχές νομικής ερμηνείας.

**Παράγει:**
- Εναλλακτικές ερμηνείες
- Εφαρμογή ερμηνευτικών αρχών
- Εντοπισμός ασαφειών

### 6. Fact Checker (`fact_checker.py`)
Υπολογίζει τελική βαθμολογία.

**Βαθμολογεί:**
- Κείμενο:  0-40
- Λογική: 0-30
- Χρονοδιάγραμμα: 0-20
- Νομολογία: 0-10

### 7. Report Generator (`report_generator.py`)
Δημιουργεί αναφορές σε πολλαπλές μορφές.

**Μορφές:**
- HTML (με CSS styling)
- Markdown
- JSON

---

## 📈 Παράδειγμα Αποτελέσματος | Sample Output

```
═══════════════════════════════════════════════════════════
  ΣΥΣΤΗΜΑ ΕΠΑΛΗΘΕΥΣΗΣ ΝΟΜΙΚΗΣ ΕΡΜΗΝΕΙΑΣ
  Legal Fact-Checking System
  Πτωχευτικό Δίκαιο Κύπρου - Cyprus Bankruptcy Law
═══════════════════════════════════════════════════════════

📄 Φόρτωση νομοθετικών κειμένων...
   ✓ Φορτώθηκαν 6 άρθρα

🔗 Ανάλυση διασταυρούμενων αναφορών...
   ✓ Εντοπίστηκαν 12 σχέσεις

⚖️  Επαλήθευση λογικής συνοχής... 
   ✓ Βαθμολογία: 18/30

⏱️  Ανάλυση χρονοδιαγράμματος...
   ✓ Βαθμολογία: 13/20

🧠 Εφαρμογή αρχών νομικής ερμηνείας... 
   ✓ Εναλλακτικές ερμηνείες:  3

📊 Υπολογισμός τελικής βαθμολογίας...
   ✓ Συνολική βαθμολογία:  68/100
   ✓ Κατηγορία: Μερικώς Υποστηριζόμενη

📝 Δημιουργία αναφοράς...
   ✓ Αναφορά αποθηκεύτηκε:  outputs/bankruptcy_factcheck_20251215_120000.html

═══════════════════════════════════════════════════════════
ΠΕΡΙΛΗΨΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ / RESULTS SUMMARY
═══════════════════════════════════════════════════════════
Συνολική Βαθμολογία:  68/100
Κατηγορία: Μερικώς Υποστηριζόμενη / Partially Supported
Επίπεδο Εμπιστοσύνης:  Μέτρια Εμπιστοσύνη / Moderate Confidence
─────────────────────────────────────────────────────────
Υποστήριξη Κειμένου: 32/40
Λογική Συνοχή: 18/30
Χρονοδιάγραμμα: 13/20
Νομολογία: 5/10
═══════════════════════════════════════════════════════════

⚠ Η ερμηνεία έχει μερική νομική βάση

Πλήρης αναφορά: outputs/bankruptcy_factcheck_20251215_120000.html
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_legal_parser.py -v
```

---

## 📚 Νομοθετική Βάση | Legal Basis

### Άρθρα που Αναλύονται: 

1. **Άρθρο 103** - Συνοπτική διαχείριση σε μικρές υποθέσεις
2. **Κανονισμός 143** - Τροποποιήσεις για συνοπτική διαχείριση
3. **Άρθρο 58** - Κήρυξη και διανομή μερισμάτων
4. **Άρθρο 27** - Αποκατάσταση πτωχεύσαντα
5. **Άρθρο 28** - Διαδικασία αποκατάστασης
6. **Άρθρο 16** - Δημόσια εξέταση χρεώστη

### Πηγές: 

- [cylaw.org - Πτωχευτικός Νόμος ΚΕΦ. 5](https://www.cylaw.org/nomoi/enop/ind/0_5/)
- [cylaw.org - Κανονισμός 368/1931](https://www.cylaw.org/nomoi/kanon/ind/1931_368/)

---

## 🤝 Συνεισφορά | Contributing

Contributions are welcome! Please: 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚖️ Νομική Σημείωση | Legal Notice

**Ελληνικά:**
Η παρούσα εφαρμογή παρέχεται για ενημερωτικούς και ερευνητικούς σκοπούς.  Δεν αποτελεί νομική συμβουλή και δεν αντικαθιστά επαγγελματική νομική καθοδήγηση.  Για νομικά ζητήματα, συμβουλευτείτε έναν ειδικό δικηγόρο. 

**English:**
This application is provided for informational and research purposes only. It does not constitute legal advice and does not replace professional legal guidance. For legal matters, consult a qualified attorney.

---

## 📝 Άδεια | License

MIT License - See LICENSE file for details

---

## 👥 Συγγραφείς | Authors

- **nvoskos** - Initial work - [GitHub](https://github.com/nvoskos)

---

## 📞 Επικοινωνία | Contact

Για ερωτήσεις ή προτάσεις, παρακαλώ ανοίξτε ένα issue στο GitHub repository.

For questions or suggestions, please open an issue on the GitHub repository.

---

## 🙏 Ευχαριστίες | Acknowledgments

- cylaw.org για την πρόσβαση στα νομοθετικά κείμενα
- NetworkX για τη βιβλιοθήκη γράφων
- Η Κυπριακή νομοθεσία βασίζεται στο Commonwealth legal system

---

**Έκδοση | Version:** 1.0.0  
**Ημερομηνία | Date:** Δεκέμβριος 2025 | December 2025