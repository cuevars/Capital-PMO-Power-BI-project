import csv, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT/'data'/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
class TestPortfolio(unittest.TestCase):
    def test_unique_projects_and_references(self):
        projects=load('projects.csv'); ids={r['ProjectID'] for r in projects}
        self.assertEqual(len(projects),80)
        self.assertEqual(len(ids),80)
        for name in ['monthly_spend.csv','stage_gates.csv']:
            self.assertTrue(all(r['ProjectID'] in ids for r in load(name)))
    def test_spending_rows_and_amounts(self):
        spend=load('monthly_spend.csv')
        self.assertEqual(len(spend),960)
        self.assertTrue(all(float(r['ActualSpend'])>=0 for r in spend))
    def test_gate_document_flags(self):
        gates=load('stage_gates.csv')
        self.assertTrue(all(r['DocumentsComplete'] in ('Yes','No') for r in gates))
        self.assertTrue(all(r['Decision'] in ('Approved','Pending') for r in gates))
if __name__ == '__main__': unittest.main()
