from math import atan2, cos, sin

class cpx:
	def __init__(self, real: float, imag: float):
		self.real = real
		self.imag = imag

	def __repr__(self) -> str: return str(self)
	def __str__(self) -> str:
		if self.real == 0 and self.imag == 0:
			return '0'
		elif self.real != 0 and self.imag > 0:
			if self.imag == 1:
				return f'{self.real}+i'
			else:
				return f'{self.real}+{self.imag}i'

		out = ''

		if self.real != 0:
			out += str(self.real)

		if self.imag == 1:
			out += 'i'
		elif self.imag == -1:
			out += '-i'
		elif self.imag != 0:
			out += f'{self.imag}i'

		return out

	def __eq__(self, o: object) -> bool:
		if isinstance(o, cpx) or type(o) is complex:
			return self.real == o.real and self.imag == o.imag
		if type(o) is int or type(o) is float:
			return self.imag == 0 and self.real == o

		return False

	def __getitem__(self, i: int) -> float:
		if i < 0 or i > 1: raise IndexError

		return self.real if i == 0 else self.imag

	def __setitem__(self, i: int, v: float) -> float:
		if i < 0 or i > 1: raise IndexError

		if i == 0:
			self.real = v
		else:
			self.imag = v

	def __radd__(self, o): return self + o
	def __add__(self, o):
		if isinstance(o, cpx) or type(o) is complex:
			return cpx(self.real + o.real, self.imag + o.imag)
		elif type(o) is int or type(o) is float:
			return cpx(self.real + o, self.imag)

	def __rsub__(self, o):
		if isinstance(o, cpx) or type(o) is complex:
			return cpx(o.real - self.real, o.imag - self.imag)
		elif type(o) is int or type(o) is float:
			return cpx(o - self.real, -self.imag)

		return NotImplemented

	def __sub__(self, o):
		if isinstance(o, cpx) or type(o) is complex:
			return cpx(self.real - o.real, self.imag - o.imag)
		elif type(o) is int or type(o) is float:
			return cpx(self.real - o, self.imag)

		return NotImplemented

	def __rmul__(self, o): return self * o
	def __mul__(self, o):
		if isinstance(o, cpx) or type(o) is complex:
			return cpx(self.real * o.real - self.imag * o.imag, self.real * o.imag + self.imag + o.real)
		elif type(o) is int or type(o) is float:
			return cpx(self.real * o, self.imag * o)

		return NotImplemented

	def __pow__(self, o):
		r = abs(self)
		arg = atan2(self.imag, self.real)

		if type(o) is int or type(o) is float:
			return cpx(cos(o * arg), sin(o * arg)) * (r ** o)

		return NotImplemented

	def __truediv__(self, o):
		if isinstance(o, cpx) or type(o) is complex:
			return cpx(self.real * o.real, self.imag * o.real - self.real * o.imag)
		elif type(o) is int or type(o) is float:
			return cpx(self.real / o, self.imag / o)

		return NotImplemented

	def __abs__(self) -> float:
		if self.real == 0 and self.imag == 0:
			return 0

		return (self.real * self.real + self.imag * self.imag) ** 0.5

	def __round__(self):
		return cpx(round(self.real), round(self.imag))

	def __neg__(self):
		return cpx(-self.real, -self.imag)
