import argparse
import json
from pathlib import Path
from .engine import evaluate,load_records

def main():
    p=argparse.ArgumentParser(description="PlanSense AI v0.1 synthetic-data research prototype")
    p.add_argument("--proposal",default="data/sample_proposal.json")
    p.add_argument("--records",default="data/synthetic_precedents.json")
    p.add_argument("--output",default=None)
    args=p.parse_args()
    proposal=json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    report=evaluate(proposal,load_records(args.records))
    result=json.dumps(report,indent=2,ensure_ascii=False)
    if args.output: Path(args.output).write_text(result+"\n",encoding="utf-8")
    else: print(result)
if __name__=="__main__": main()
