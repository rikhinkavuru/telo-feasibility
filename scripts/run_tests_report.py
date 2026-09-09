"""Run the test suite and write results/manifests/test_report.json for the status checker."""

from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "manifests"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    junit = OUT / "junit.xml"
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q", f"--junitxml={junit}"], cwd=ROOT
    )
    tree = ET.parse(junit)
    root = tree.getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    passed = failed = errors = skipped = 0
    names: set[str] = set()
    for s in suites:
        failed += int(s.get("failures", 0))
        errors += int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
        for case in s.iter("testcase"):
            ok = (
                case.find("failure") is None
                and case.find("error") is None
                and case.find("skipped") is None
            )
            if ok:
                passed += 1
                names.add(case.get("name", ""))
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "passed": passed,
        "failed": failed + errors,
        "skipped": skipped,
        "crn_test_passed": "test_paired_strategies_share_demand_and_disruptions" in names
        and "test_common_random_numbers_world_identical_across_strategies" in names,
        "common_cause_test_passed": "test_independent_sites_help_and_perfectly_correlated_sites_do_not"
        in names,
        "mass_balance_property_passed": "test_property_mass_balance_and_nonnegativity_hold"
        in names,
        "exit_code": proc.returncode,
    }
    (OUT / "test_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
