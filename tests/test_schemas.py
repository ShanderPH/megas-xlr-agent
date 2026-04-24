import pytest
from pydantic import ValidationError

from schemas.backlog import Backlog, BacklogItem, Layer, Priority

def test_backlog_roundtrip() -> None:
    data = {
        "project": "BR Masters",
        "feature": "Lineup",
        "summary": "Build a lineup feature",
        "items": [
            {
                "id": "BR-LINEUP-001",
                "title": "Basic grid",
                "description": "Grid of players",
                "layer": "UI",
                "priority": "P1",
                "acceptance_criteria": ["Given X, when Y, then Z", "Given A, when B, then C"],
                "dependencies": [],
                "estimate_hours": 2.5
            }
        ],
        "open_questions": [],
        "estimated_total_hours": 2.5
    }
    backlog = Backlog.model_validate(data)
    assert backlog.project == "BR Masters"
    assert len(backlog.items) == 1
    assert backlog.items[0].id == "BR-LINEUP-001"
    assert backlog.estimated_total_hours == 2.5

def test_backlog_item_id_rejects_lowercase() -> None:
    with pytest.raises(ValidationError) as exc_info:
        BacklogItem(
            id="br-lineup-001",
            title="Basic grid",
            description="Grid of players",
            layer="UI",
            priority="P1",
            acceptance_criteria=["Crit 1", "Crit 2"],
            estimate_hours=1.0
        )
    assert "UPPER-CASE slug" in str(exc_info.value)

def test_backlog_item_acceptance_criteria_min_2() -> None:
    with pytest.raises(ValidationError) as exc_info:
        BacklogItem(
            id="BR-LINEUP-001",
            title="Basic grid",
            description="Grid of players",
            layer="UI",
            priority="P1",
            acceptance_criteria=["Only one criteria"],
            estimate_hours=1.0
        )
    assert "List should have at least 2 items after validation" in str(exc_info.value)

def test_backlog_estimated_total_hours_mismatch() -> None:
    data = {
        "project": "BR Masters",
        "feature": "Lineup",
        "summary": "Build a lineup feature",
        "items": [
            {
                "id": "BR-LINEUP-001",
                "title": "Basic grid",
                "description": "Grid of players",
                "layer": "UI",
                "priority": "P1",
                "acceptance_criteria": ["Given X, when Y, then Z", "Given A, when B, then C"],
                "dependencies": [],
                "estimate_hours": 2.5
            }
        ],
        "open_questions": [],
        "estimated_total_hours": 4.0
    }
    with pytest.raises(ValidationError) as exc_info:
        Backlog.model_validate(data)
    assert "does not match sum of items" in str(exc_info.value)

def test_backlog_item_estimate_hours_limits() -> None:
    # 0.5 is valid
    item = BacklogItem(
        id="BR-LINEUP-001",
        title="Basic grid",
        description="Grid of players",
        layer="UI",
        priority="P1",
        acceptance_criteria=["Crit 1", "Crit 2"],
        estimate_hours=0.5
    )
    assert item.estimate_hours == 0.5
    
    # 0.4 is invalid
    with pytest.raises(ValidationError):
        BacklogItem(
            id="BR-LINEUP-002",
            title="Basic grid",
            description="Grid of players",
            layer="UI",
            priority="P1",
            acceptance_criteria=["Crit 1", "Crit 2"],
            estimate_hours=0.4
        )
        
    # 41.0 is invalid
    with pytest.raises(ValidationError):
        BacklogItem(
            id="BR-LINEUP-003",
            title="Basic grid",
            description="Grid of players",
            layer="UI",
            priority="P1",
            acceptance_criteria=["Crit 1", "Crit 2"],
            estimate_hours=41.0
        )
