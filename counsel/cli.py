"""counsel CLI."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from counsel.cases.allegation import Allegation, AllegationSeverity
from counsel.cases.client import Client
from counsel.defense.attorney import AttorneyConfig, DefenseAttorney
from counsel.evidence.index import DefenseEvidence, EvidenceIndex, EvidenceRole
from counsel.io.store import BriefStore


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _load_case(path: Path) -> tuple[Client, EvidenceIndex]:
    data = json.loads(path.read_text())
    client = Client(
        handle=data["client"]["handle"],
        legal_name=data["client"].get("legal_name"),
        role=data["client"].get("role", ""),
        public_corpus_id=data["client"].get("public_corpus_id"),
        notes=data["client"].get("notes", ""),
    )
    for a in data.get("allegations", []):
        client.allegations.append(
            Allegation(
                id=a["id"],
                accuser=a["accuser"],
                summary=a["summary"],
                severity=AllegationSeverity(a.get("severity", "material")),
                source_urls=a.get("source_urls", []),
                notes=a.get("notes", ""),
            )
        )
    evidence = EvidenceIndex()
    for e in data.get("evidence", []):
        evidence.add(
            DefenseEvidence(
                id=e["id"],
                role=EvidenceRole(e["role"]),
                summary=e["summary"],
                source_url=e.get("source_url"),
                weight=e.get("weight", 1.0),
                rebuttal_anticipated=e.get("rebuttal_anticipated", ""),
            )
        )
    return client, evidence


def cmd_represent(args: argparse.Namespace) -> int:
    case_path = Path(args.case)
    if not case_path.exists():
        print(f"case file not found: {case_path}", file=sys.stderr)
        return 2

    client, evidence = _load_case(case_path)
    cfg = AttorneyConfig(provider=args.provider, model=args.model)
    attorney = DefenseAttorney(config=cfg)
    brief = asyncio.run(attorney.represent(client, evidence))

    store = BriefStore(root=args.out)
    path = store.save(brief)
    print(f"brief saved: {path}")
    if args.print:
        print()
        print(brief.render())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="counsel")
    p.add_argument("--log-level", default="INFO")
    sub = p.add_subparsers(dest="cmd", required=True)

    represent = sub.add_parser("represent", help="draft a defense brief from a case file")
    represent.add_argument("--case", required=True, help="path to case json file")
    represent.add_argument("--provider", default="openai", choices=["openai", "xai"])
    represent.add_argument("--model", default=None)
    represent.add_argument("--out", default="briefs")
    represent.add_argument("--print", action="store_true", help="also print to stdout")
    represent.set_defaults(func=cmd_represent)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.log_level)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())




