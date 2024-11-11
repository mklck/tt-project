from battleship		import *
from battleship.types	import saturate, Point

import pytest

def test_saturate():
	tests = {
		# (min, max, val): expected
		(1, 3, 5):	3,
		(0, 0, 4):	0,
		(-1, 5, 2):	2,
		(6, 2, 1):	6
	}

	for given in tests:
		assert saturate(*given) == tests[given]

class TestRect:
	@pytest.fixture
	@classmethod
	def examples(cls):
		r0 = Rect(BoardPoint(1,1), BoardPoint(1,2))
		r1 = Rect(BoardPoint(4, 4), BoardPoint(2, 2))
		r2 = Rect(BoardPoint(3, 3), BoardPoint(4, 4))
		r3 = Rect(BoardPoint(1, 1), BoardPoint(5, 5))
		return [r0, r1, r2, r3]

	def test_init(self, examples):
		areas = [2, 9, 4, 25]

		for a, x in zip(areas, examples):
			assert x.area == a

	def test_overlap(self, examples):
		e = examples
		
		assert	not e[0].overlap(e[1])
		assert	not e[0].overlap(e[2])
		assert	e[1].overlap(e[2])
		assert	e[3].overlap(e[1])
		assert	e[1].overlap(e[3])

	def test_extends(self, examples):
		e = examples

		assert	e[1].extends(e[2])
		assert	e[0].extends(e[0])
		assert	not e[2].extends(e[1])
		assert	not e[1].extends(e[0])
		assert	not e[0].extends(e[2])
		assert	e[2].extends(e[2])

class TestBoardPoint:
	def test_init(self):
		valid = [(1, 1), (2, 4), (10, 10)]
		invalid = [(0, 0), (5, 0), (12, 10), (-1, 0)]

		[BoardPoint(*x) for x in valid]
		try:
			for x in invalid:
				BoardPoint(*x)
				assert False, x
		except Exception as e:
			assert type(e) is ValueError
	
	def test_fromAlnum(self):
		valid = [('a', 7), ('b', 1), ('f', 6), ('j', 10)]
		invalid = [('ą', 1), ('aa', 5), ('a', -1), ('k', 8), (1, 5)]

		[BoardPoint.fromAlnum(*x) for x in valid]
		try:
			for x in invalid:
				BoardPoint.fromAlnum(*x)
				assert False, x
		except:
			pass

	def test_toAlnum(self):
		tests = {
			BoardPoint(1, 1):	('a', 1),
			BoardPoint(5, 7):	('e', 7),
			BoardPoint(3, 5):	('c', 5),
			BoardPoint(10, 2):	('j', 2),
		}
		
		for g, t in tests.items():
			assert g.toAlnum() == t

class TestShip:

	@pytest.fixture
	@classmethod
	def examples(cls):
		s0 = Ship(ShipSize(3), BoardPoint(1, 1), 'vertical')
		s1 = Ship(ShipSize(2), BoardPoint(5, 5), 'horizontal')
		s2 = Ship(ShipSize(4), BoardPoint(5, 3), 'vertical')

		return [s0, s1, s2]
		
	def test_belong(self, examples):
		e = examples
		p0 = BoardPoint(1, 3)
		p1 = BoardPoint(6, 5)

		assert 	e[0].belong(p0)
		assert	not e[0].belong(p1)
		assert	not e[1].belong(p0)
		assert	e[1].belong(p1)

	def test_collide(self, examples):
		e = examples

		assert	not e[0].collide(e[1])
		assert	e[2].collide(e[1])
		assert	e[1].collide(e[2])
		
	def test_getSize(self, examples):
		sizes = [3, 2, 4]

		for g, t in zip(examples, sizes):
			assert g.getSize() == t

class TestBoard:

	def test_init(self):
		bp = BoardPoint(1, 1)
		ships = [Ship(ShipSize(4), bp, 'horizontal')]
		b = Board(ships=ships)
		b.hit(bp)
		try:
			b.hit(bp)
			assert False, "Expected PositionHitBefore exception"
		except Exception as e:
			assert type(e) is PositionHitBefore

class TestBoardConstructor:

	def test_add(self):
		bc = BoardConstructor()
		try:
			bc.addShipHor(size=ShipSize(4), pos=BoardPoint(1, 1))
			bc.addShipVer(size=ShipSize(3), pos=BoardPoint(4, 1))
		except ShipIsColliding:
			pass
		except Exception as e:
			assert False, e
		try:
			bc.addShipVer(size=ShipSize(4), pos=BoardPoint(7, 5))
		except TooMuchShipsOfSize:
			pass
		except Exception as e:
			assert False, e

	def test_boardConstruction(self):
		bc = BoardConstructor()
		try:
			bc.addShipHor(ShipSize(1), BoardPoint(1, 10))
			bc.addShipHor(ShipSize(1), BoardPoint(3, 10))
			bc.addShipHor(ShipSize(1), BoardPoint(5, 10))
			bc.addShipHor(ShipSize(1), BoardPoint(7, 10))

			bc.addShipHor(ShipSize(2), BoardPoint(1, 8))
			bc.addShipHor(ShipSize(2), BoardPoint(4, 8))
			bc.addShipHor(ShipSize(2), BoardPoint(7, 8))

			bc.addShipHor(ShipSize(3), BoardPoint(1, 6))
			bc.addShipHor(ShipSize(3), BoardPoint(5, 6))

			bc.addShipHor(ShipSize(4), BoardPoint(1, 4))
		except Exception as e:
			assert False, e
		assert bc.isReady()
		bc.getBoard()