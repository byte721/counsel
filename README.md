# counsel

> An AI defense attorney for high-profile public disputes. Pick a side. Counsel builds the defense.

[![python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](#)
[![license MIT](https://img.shields.io/badge/license-MIT-green.svg)](#)

`counsel` reads public allegations against a chosen client, indexes exculpatory and mitigating evidence, frames a defense theory, and produces a defense brief. It does not deliver verdicts. It does not rule on guilt. It defends.

The framework takes the client's position as given and argues it. Decisions on which side to take are the user's. Counsel argues whichever side it is asked to argue. That is the design.

## Install

```bash
git clone https://github.com/byte721/counsel.git
cd counsel
pip install -e ".[dev]"
```

Set credentials:

```bash
export OPENAI_API_KEY="..."
# Optional, for using Grok instead:
export XAI_API_KEY="..."
```

## Use

Draft a defense brief from an example case:

```bash
counsel represent --case examples/defending_musk.json --print
```

Switch sides:

```bash
counsel represent --case examples/defending_altman.json --print
```

Switch providers:

```bash
counsel represent --case examples/defending_altman.json --provider xai
```

## How it works

1. **Load the case.** A case file is a JSON document with the client, allegations against them, and evidence available for the defense.
2. **Build the prompt.** Counsel formats the case into a structured prompt for the chosen LLM provider.
3. **Draft the brief.** The model returns a structured JSON brief with theory, factual recitation, per-allegation responses, and closing.
4. **Persist the brief.** Briefs are saved as JSON for analysis and as text for posting.

## Defense theory

A defense theory is the one-line answer to "what is your case." Every piece of evidence and every counter-argument should serve the theory. If a piece of evidence does not serve it, drop the evidence, not the theory.

Counsel supports six theory archetypes:

- **denial**: the act did not occur or the client did not do it
- **reframing**: the act occurred but is not what the accuser claims it is
- **justification**: the act occurred and was justified
- **procedural**: the accuser lacks standing or process was not followed
- **affirmative**: the act was lawful and consistent with the client's authority
- **mitigation**: the act occurred and the client acknowledges, but seeks reduced consequence

The model picks an archetype per case based on the available evidence.

## Layout

```
counsel/
    cases/        client and allegation schemas
    defense/      attorney, brief, prompts
    evidence/     evidence index, role classification
    framing/      defense theory archetypes
    clients/      LLM provider adapters (openai + xai)
    io/           file-based brief storage
    cli.py        counsel CLI entrypoint
tests/            pytest suite
examples/         sample case files
```

## What this is not

Counsel is not neutral. Counsel is not a judge. Counsel does not decide who is right.

Counsel is also not a brief written by a licensed attorney. Briefs produced by this tool are AI-generated and are not legal advice. They are research artifacts intended to explore how language models reason about adversarial public disputes.

If you are involved in actual litigation, hire an actual attorney.

## License

MIT.













