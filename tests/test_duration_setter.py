from duration_setter import DurationSetter
from tests.mock_todoist_wrapper import MockTodoistWrapper


def test_already_annotated():
    ds = DurationSetter(MockTodoistWrapper())
    assert not ds.already_annotated("hello world")
    assert not ds.already_annotated("hello [10m] world")
    assert ds.already_annotated("hello world [10m]")
