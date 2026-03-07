# Changelog

## [0.3.4] - 2026-04-27
- fix: BriefStore handled empty cited_evidence_ids inconsistently
- chore: small docs touch-ups for the launch

## [0.3.3] - 2026-04-21
- feat: --provider flag on CLI for openai vs xai
- chore: bump default openai model to gpt-4o

## [0.3.2] - 2026-04-12
- fix: response parser handled fenced JSON inconsistently
- fix: AllegationSeverity comparisons in client.serious_count

## [0.3.1] - 2026-04-04
- feat: theory weaknesses field on DefenseTheory
- fix: clearer error when chat returns malformed JSON

## [0.3.0] - 2026-03-25
- breaking: rename Cabinet -> Counsel across the codebase
- feat: BriefStore JSON+text dual format

## [0.2.2] - 2026-03-12
- fix: evidence index counted by_role inconsistently for IMPEACHING items

## [0.2.1] - 2026-02-28
- feat: AttorneyConfig dataclass
- chore: ruff config tightened

## [0.2.0] - 2026-02-19
- feat: theory archetypes (denial, reframing, justification, procedural, affirmative, mitigation)
- feat: structured per-allegation responses

## [0.1.2] - 2026-02-09
- fix: ChatClient retry logic on 429s

## [0.1.1] - 2026-02-02
- fix: openai response parsing edge cases

## [0.1.0] - 2026-01-22
- initial: DefenseAttorney + Client + Allegation + EvidenceIndex





