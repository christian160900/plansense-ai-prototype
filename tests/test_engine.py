import json
import unittest
from pathlib import Path
from plansense.engine import extract_themes, haversine_km, comparable, evaluate,load_records
ROOT=Path(__file__).resolve().parents[1]
class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=load_records(ROOT/'data'/'synthetic_precedents.json')
        cls.proposal=json.loads((ROOT/'data'/'sample_proposal.json').read_text())
    def test_theme_extraction(self):
        self.assertEqual(extract_themes('Loss of light and parking pressure'),['loss_of_light','parking'])
    def test_geodistance(self):
        self.assertAlmostEqual(haversine_km(51.5,-0.1,51.5,-0.1),0)
    def test_matching_deterministic(self):
        a=comparable(self.proposal,self.records)
        self.assertEqual(a,comparable(self.proposal,self.records))
        self.assertTrue(a[0]['same_proposal_type'])
        self.assertTrue(all(a[i]['match_score']>=a[i+1]['match_score'] for i in range(len(a)-1)))
    def test_outputs_and_disclosures(self):
        report=evaluate(self.proposal,self.records)
        self.assertTrue(0<=report['planning_feasibility_index']<=100)
        self.assertTrue(0<=report['objection_risk_index']<=100)
        self.assertEqual(len(report['comparables']),5)
        self.assertIn('uncalibrated', ' '.join(report['notices']))
    def test_constraint_shifts_score(self):
        base=evaluate(self.proposal,self.records)
        changed=json.loads(json.dumps(self.proposal))
        changed['constraints']['conservation_area']=True
        modified=evaluate(changed,self.records)
        self.assertLess(modified['planning_feasibility_index'],base['planning_feasibility_index'])
    def test_reject_missing_fields(self):
        with self.assertRaisesRegex(ValueError,'Missing proposal field'):
            evaluate({'address':'test'},self.records)
    def test_coordinate_bounds(self):
        modified={**self.proposal,'latitude':999}
        with self.assertRaisesRegex(ValueError,'Coordinates out of range'):
            evaluate(modified,self.records)
    def test_synthetic_source_labels(self):
        self.assertTrue(all('SYNTHETIC' in r['source_label'] for r in self.records))
if __name__=='__main__': unittest.main()
