# Architecture

Counsel is a small framework. The interesting choices are about what it
does NOT do.

## What it does

Given a Client and a list of Allegations against them, plus an EvidenceIndex
of material that supports the defense, Counsel:

1. Builds a structured prompt for the LLM
2. Calls the model with system and user messages
3. Parses the JSON response into typed objects
4. Returns a DefenseBrief

That is the entire pipeline.

## What it does not do

Counsel does not:

- Decide guilt
- Issue verdicts
- Pretend to be neutral
- Argue against its own client
- Refuse a case based on perceived merit
- Offer legal advice in the real world

This is by design. A defense attorney's job is to produce the best argument
the record will support, regardless of what the attorney privately believes.
Counsel models that role specifically.

## Design choices

### Single ChatClient, multiple providers

Earlier framework projects in this codebase family used separate classes
per provider. Counsel uses a single ChatClient parameterized by a provider
config. Less code, fewer paths to bug, easy to add a new provider by
appending to the PROVIDERS dict.

### Defense theory as a first-class concept

Most LLM-based legal tools generate text. They do not commit to a frame.
Counsel commits to a frame: every brief has an explicit theory archetype
(denial, reframing, justification, procedural, affirmative, mitigation) and
the rest of the brief must serve it.

This is what real defense attorneys do. The brief should not just be a list
of responses. It should be one cohesive argument.

### Evidence is tagged with a defense role

A piece of evidence is not just "evidence." It is exculpatory, mitigating,
impeaching, or foundational. Each role serves a different purpose in a brief.
Counsel forces this tagging at evidence intake time, which means the prompt
to the model includes role-tagged evidence rather than a flat list.

### File-based persistence

Briefs are JSON+text on disk. No database. No remote storage. Briefs are
small, infrequent, and the user is expected to inspect them by hand or paste
them into X. SQLite would be overkill.

### No automatic adversarial loop

Counsel does not run a back-and-forth between defense and prosecution. There
is no opposing counsel built in. The user is the prosecution. The user
brings allegations. Counsel responds.

This is intentional. Adversarial loops between two LLMs converge on the
same plausible-sounding language. The defense should be sharper than that.

## What we considered and didn't ship

- **Multi-pass refinement.** A second model pass that critiques the brief.
  Tested, didn't help much. The first pass with strict prompting was good
  enough.
- **Citation formatting.** Bluebook-style legal citations. Out of scope. The
  briefs are research artifacts, not court filings.
- **A prosecutor agent.** The opposite of Counsel. Plausible future work
  but kept out of this repo for clarity.




