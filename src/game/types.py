from dataclasses	import dataclass, field

@dataclass(frozen=True, eq=True)
class Point:
	x : int
	y : int
	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		return Point(x, y)
	def __mul__(self, other):
		if type(other) is Point:
			x = self.x * other.x
			y = self.y * other.y
			return Point(x, y)
		else:
			return Point(
				self.x * other,
				self.y * other
			)
	def asTuple(self):
		return self.x, self.y
