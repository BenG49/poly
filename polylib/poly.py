from copy import deepcopy
from math import sqrt

# (root, remaining)
def newton(p) -> tuple:
	EPSILON = 0.0000000000001
	MAX_ITER = 1000

	d = p.derivative()

	x = 1
	i = 0

	while i < MAX_ITER and abs(p(x)) > EPSILON:
		_d = d(x)

		# works tm
		if _d:
			x -= p(x) / _d
		else:
			x -= EPSILON

		i += 1
	
	if not i < MAX_ITER:
		return None, p
	
	# round if very close to integer
	if abs(round(x) - x) <= EPSILON:
		x = round(x)
	
	out = Poly({ 1 : 1, 0 : -x })

	return (out, p // out)

class Poly:
	def __init__(self, d: dict = None):
		if d:
			self.d = d
			self.leading_c = max(d.keys())
		else:
			self.d = {}
			self.leading_c = 0
	
	def __repr__(self) -> str:
		return self.__str__()
	def __str__(self) -> str:
		if not self.d: return '0'

		out = ''
		first = True

		for p, c in sorted(self.d.items(), reverse=True):
			if first: first = False
			elif c > 0:
				out += '+'
			
			coef_str = str(int(c) if c % 1 == 0 else c)

			if p == 0:
				out += coef_str
			elif p < 0:
				out += f'({coef_str}/x'
				if p != -1:
					out += f'^{-p}'
				out += ')'
			else:
				# coefficient string '-' if -1, nothing if 1
				if c == -1: out += '-'
				elif c != 1: out += coef_str

				out += 'x'
				if p != 1:
					out += f'^{p}'

		return out
	
	def __setitem__(self, pow, coef):
		if coef != 0:
			self.leading_c = max(self.leading_c, pow)
			self.d[pow] = coef
		else:
			if self.d.get(pow) is not None:
				del self[pow]
	def __getitem__(self, pow) -> float:
		v = self.d.get(pow)
		return v if v is not None else 0
	def __delitem__(self, pow):
		if self.d.get(pow) is not None:
			del self.d[pow]

			if pow == self.leading_c:
				self.leading_c = 0 if len(self.d.keys()) == 0 else max(self.d.keys())
	
	def __len__(self) -> int: return len(self.d)

	def __eq__(self, o) -> bool:
		if type(o) is Poly:
			if len(self) != len(o): return False

			for p, c in self.d.items(0):
				if o[p] != c:
					return False
			
			return True
		elif type(o) is int or type (o) is float:
			return len(self) == 1 and self[0] == o
		else:
			raise ValueError

	def __sub__(self, o): return self + o * -1
	
	def __iadd__(self, o):
		if type(o) is Poly:
			for p, c in o.d.items():
				self[p] += c

			return self
		elif type(o) is int or type(o) is float:
			self[0] += o

			return self
		else:
			raise ValueError

	def __add__(self, o):
		if type(o) is Poly:
			out = deepcopy(self)

			for p, c in o.d.items():
				out[p] += c
			
			return out
		elif type(o) is int or type(o) is float:
			out = deepcopy(self)

			out[0] += o

			return out
		else:
			raise ValueError
	
	def __rmul__(self, o): return self * o
	def __mul__(self, o):
		# FOIL
		if type(o) is Poly:
			if len(o) == 1 and o.d.get(0) is not None:
				return self.__mul__(o.d[0])

			out = Poly()

			# loop through self
			for p1, c1 in self.d.items():
				# loop through other
				for p2, c2 in o.d.items():
					# multiply
					out[p1 + p2] += c1 * c2

			return out
		elif type(o) is int or type(o) is float:
			out = deepcopy(self)

			for p in self.d:
				out[p] *= o

			return out
		else:
			raise ValueError
	
	# (pow, coefficient)
	def div_terms(dividend: tuple, divisor: tuple) -> tuple:
		return (dividend[0] - divisor[0],
		        dividend[1] / divisor[1])
	
	def div_rem(self, denom) -> tuple:
		if type(denom) is Poly:
			if denom.order() > self.order():
				raise ValueError

			out = Poly()
			# numer will be modified, make copy
			numer = deepcopy(self)

			while numer.order() >= denom.order():
				(p, c) = Poly.div_terms(
					numer.leading(),
					denom.leading())

				out[p] = c

				# multiply and sub
				numer -= denom * Poly({ p : c })

			return out, numer
		elif type(denom) is int or type(denom) is float:
			out = deepcopy(self)

			for p in self.d:
				out[p] /= denom

			return out, 0
		else:
			raise ValueError

	# TRUE DIV NOT SUPPORTED, CANNOT RET REMAINDER
	def __floordiv__(self, denom):
		return self.div_rem(denom)[0]

	def __mod__(self, denom):
		return self.div_rem(denom)[1]

	def __call__(self, x: float) -> float:
		sum = 0

		for p, c, in self.d.items():
			sum += c * x ** p

		return sum
	
	def derivative(self):
		out = Poly()
	
		for p, c in self.d.items():
			out[p - 1] = p * c
	
		return out
	
	def order(self) -> int:
		return self.leading_c
	
	def leading(self) -> tuple:
		return (self.leading_c, self[self.leading_c])
	
	def monic(self):
		return deepcopy(self) // self.leading_c

	# returns list of polynomials
	def factors(self) -> list:
		p = deepcopy(self)
		roots = []

		while p.order() > 1:
			r, p = newton(p)

			if r is None:
				return roots + p

			roots.append(r)

		if p.order() == 1:
			roots.append(p)
			return roots

		return roots + p

	def zeroes(self) -> list:
		if self.order() == 1:
			return [-self[0] / self[1]]
		elif self.order() == 2:
			# quadratic formula
			d = sqrt(self[1] ** 2 - 4 * self[2] * self[0])
			a2 = 2 * self[2]
			return [(-self[1] + d) / a2, (-self[1] - d) / a2]
		else:
			f = self.factors()
			out = []

			for r in f:
				out += r.zeroes()
			
			return out
