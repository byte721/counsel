# Case file format

A case file is a JSON document that describes:

- A **client** that Counsel will defend
- A list of **allegations** against the client
- A list of **evidence** items available for the defense

## Top-level structure

```json
{
  "client": { ... },
  "allegations": [ ... ],
  "evidence": [ ... ]
}
```

## Client

```json
{
  "handle": "@elonmusk",
  "legal_name": "Elon Musk",
  "role": "Plaintiff in Musk v. Altman; co-founder of OpenAI",
  "public_corpus_id": "musk_public",
  "notes": "Optional context for the defense"
}
```

Required: `handle`. Everything else is optional.

## Allegations

Each allegation:

```json
{
  "id": "alleg_001",
  "accuser": "@sama",
  "summary": "Plain-text allegation in 1-3 sentences.",
  "severity": "serious",
  "source_urls": ["https://..."],
  "notes": ""
}
```

`severity` is one of: `nuisance`, `material`, `serious`, `critical`.

The `id` should be unique within the case. Counsel references it in responses.

## Evidence

Each evidence item:

```json
{
  "id": "ev_001",
  "role": "exculpatory",
  "summary": "Plain-text description of the evidence.",
  "source_url": "https://...",
  "weight": 3.5,
  "rebuttal_anticipated": "How an opposing party might respond"
}
```

`role` is one of: `exculpatory`, `mitigating`, `impeaching`, `foundational`.

`weight` is a float. It is used as a soft signal to the model about which
evidence to lean on. Default 1.0.

Counsel only stores evidence that helps the defense. Inculpatory evidence
against the client is not part of an EvidenceIndex.

## Example

See `examples/defending_musk.json` and `examples/defending_altman.json`
for full examples of cases drawn from the real Musk v. Altman litigation.

