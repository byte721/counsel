"""Tests for case schemas."""
from __future__ import annotations

from counsel.cases.allegation import Allegation, AllegationSeverity
from counsel.cases.client import Client


def _alleg(severity: AllegationSeverity = AllegationSeverity.MATERIAL) -> Allegation:
    return Allegation(
        id="alleg_1",
        accuser="@accuser",
        summary="did the thing",
        severity=severity,
    )


def test_allegation_critical_check():
    a = _alleg(AllegationSeverity.CRITICAL)
    assert a.is_critical()
    assert a.is_substantive()


def test_allegation_nuisance_not_substantive():
    a = _alleg(AllegationSeverity.NUISANCE)
    assert not a.is_critical()
    assert not a.is_substantive()


def test_client_serious_count():
    c = Client(handle="@client")
    c.allegations.append(_alleg(AllegationSeverity.NUISANCE))
    c.allegations.append(_alleg(AllegationSeverity.SERIOUS))
    c.allegations.append(_alleg(AllegationSeverity.CRITICAL))
    c.allegations.append(_alleg(AllegationSeverity.MATERIAL))
    assert c.serious_count() == 2


def test_client_critical_check():
    c = Client(handle="@client")
    c.allegations.append(_alleg(AllegationSeverity.CRITICAL))
    assert c.has_critical_allegations

