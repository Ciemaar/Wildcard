from wms.database.models import Batch, Mission, generate_uuid


def test_generate_uuid():
    """Test UUID generation function."""
    val1 = generate_uuid()
    val2 = generate_uuid()
    assert val1 != val2
    assert isinstance(val1, str)
    assert len(val1) == 36


def test_mission_model():
    """Test the Mission model initialization."""
    mission = Mission(text="Test", category="TestCat", difficulty=1)
    assert mission.text == "Test"
    assert mission.category == "TestCat"
    assert mission.difficulty == 1


def test_batch_model():
    """Test the Batch model initialization."""
    batch = Batch(name="Test Batch")
    assert batch.name == "Test Batch"
