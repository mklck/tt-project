import pytest

from game.circleCross import (
	BoardPoint,
	Field,
	FieldType,
	CircleCrossChecker
)

@pytest.fixture
def examples():
	c0 = [
		Field(pos=BoardPoint(1,0), type=FieldType.cross),
		Field(pos=BoardPoint(1,1), type=FieldType.cross),
		Field(pos=BoardPoint(0,2), type=FieldType.circle),
		Field(pos=BoardPoint(1,2), type=FieldType.circle),
		Field(pos=BoardPoint(2,2), type=FieldType.circle)
	]
	c1 = [
		Field(pos=BoardPoint(0,0), type=FieldType.cross)
	]
	c2 = [
		Field(pos=BoardPoint(0,0), type=FieldType.cross),
		Field(pos=BoardPoint(1,1), type=FieldType.cross),
		Field(pos=BoardPoint(2,2), type=FieldType.cross),
		Field(pos=BoardPoint(0,2), type=FieldType.cross),
	]
	return {
		FieldType.circle:	c0,
		None:			c1,
		FieldType.cross:	c2,
	}

class TestCircleCrossChecker:
	def test_check(self, examples):
		for key in examples:
			t = CircleCrossChecker(examples[key])
			assert t.check() == key
