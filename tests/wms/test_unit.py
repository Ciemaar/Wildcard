from wms.database.models import Batch, Prompt, generate_uuid


def test_generate_uuid():
    """Test UUID generation function."""
    val1 = generate_uuid()
    val2 = generate_uuid()
    assert val1 != val2
    assert isinstance(val1, str)
    assert len(val1) == 36


def test_prompt_model():
    """Test the Prompt model initialization."""
    prompt = Prompt(text="Test", category="TestCat", difficulty=1)
    assert prompt.text == "Test"
    assert prompt.category == "TestCat"
    assert prompt.difficulty == 1


def test_batch_model():
    """Test the Batch model initialization."""
    batch = Batch(name="Test Batch")
    assert batch.name == "Test Batch"
