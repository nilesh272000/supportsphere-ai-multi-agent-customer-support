"""Command-line entry point."""
import argparse
import json
from pathlib import Path
from .agents import SupportCoordinator

def run_eval() -> int:
    cases_path = Path(__file__).resolve().parents[2] / "eval" / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    agent = SupportCoordinator()
    passed = 0
    for case in cases:
        result = agent.handle(case["input"], session_id="eval")
        ok = result["route"] == case["expected_route"] and case["expected_phrase"].lower() in result["answer"].lower()
        print(f"{'PASS' if ok else 'FAIL'} | {case['name']} | route={result['route']}")
        passed += int(ok)
    print(f"\nEvaluation: {passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1

def main() -> None:
    parser = argparse.ArgumentParser(prog="supportsphere", description="Multi-agent customer support demo")
    sub = parser.add_subparsers(dest="command", required=True)
    ask = sub.add_parser("ask", help="Ask a customer support question")
    ask.add_argument("message", nargs="+")
    ask.add_argument("--session", default="default")
    sub.add_parser("eval", help="Run deterministic evaluation cases")
    args = parser.parse_args()
    if args.command == "ask":
        result = SupportCoordinator().handle(" ".join(args.message), args.session)
        print(f"Route: {result['route']}\nAnswer: {result['answer']}")
    else:
        raise SystemExit(run_eval())

if __name__ == "__main__":
    main()
