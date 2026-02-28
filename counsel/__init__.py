"""counsel: an AI defense attorney for high-profile public disputes.

Pick a side. Counsel builds the defense.

The framework reads public allegations against a chosen client, indexes
exculpatory and mitigating evidence, frames a defense theory, and produces
a defense brief. It does not deliver verdicts. It does not rule on guilt.
It defends.

Decisions on which side to take are the user's. Counsel argues whichever
side it is asked to argue. That is the design.
"""

from counsel.cases.allegation import Allegation, AllegationSeverity
from counsel.cases.client import Client
from counsel.defense.attorney import DefenseAttorney
from counsel.defense.brief import DefenseBrief
from counsel.framing.theory import DefenseTheory

__version__ = "0.3.4"

__all__ = [
    "Allegation",
    "AllegationSeverity",
    "Client",
    "DefenseAttorney",
    "DefenseBrief",
    "DefenseTheory",
]




