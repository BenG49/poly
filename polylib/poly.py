from copy import deepcopy
from .cpx import cpx

class Poly:
	# takes in dictionary of {power : coefficient}
	def __init__(self, d: dict = None):
		if d:
			self.d = d
			self.leading_c = max(d.keys())
		else:
			self.d = {}
			self.leading_c = 0

	# create Poly from leading term and list of roots
	# not sure if there is a more efficient way to do this
	def from_roots(a: float, roots: list):
		# the number 1
		out = Poly({0 : 1})

		for r in roots:
			# multiply by x - r
			out *= Poly({1 : 1, 0 : -r})
		
		return out * a

	# takes in list of points (tuples), returns Poly passing through those points
	def lagrange(points: list):
		# returns a partial polynomial given 
		def partial(point: tuple):
			# the number 1
			out = Poly({0 : 1})

			for r, _ in points:
				if r == point[0]:
					continue
				
				out *= Poly({1 : 1, 0 : -r})

			return (point[1] / out(point[0])) * out
		
		out = Poly()

		for p in points:
			out += partial(p)
		
		return out
	
	def __repr__(self) -> str:
		return self.__str__()
	def __str__(self) -> str:
		if not self.d: return '0'

		out = ''
		first = True

		for p, c in sorted(self.d.items(), reverse=True):
			if first: first = False
			elif isinstance(c, cpx) or type(c) is complex:
				if c.real > 0:
					out += '+'
				elif c.real == 0 and c.imag > 0:
					out += '+'

				out += str(c)
				continue
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
	
	# sets coefficient at given term
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
	
	# number of nonzero coefficients
	def __len__(self) -> int: return len(self.d)

	def __eq__(self, o) -> bool:
		if type(o) is Poly:
			if len(self) != len(o): return False

			for p, c in self.d.items(0):
				if o[p] != c:
					return False
			
			return True
		else:
			return len(self) == 1 and self[0] == o

	def __sub__(self, o): return self + o * -1
	
	def __iadd__(self, o):
		if type(o) is Poly:
			for p, c in o.d.items():
				self[p] += c

			return self
		else:
			self[0] += o

			return self

	def __add__(self, o):
		if type(o) is Poly:
			out = deepcopy(self)

			for p, c in o.d.items():
				out[p] += c
			
			return out
		else:
			out = deepcopy(self)

			out[0] += o

			return out
	
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
		else:
			out = deepcopy(self)

			for p in self.d:
				out[p] *= o

			return out
	
	# divide self by denom and return (quotient, remainder)
	def div_rem(self, denom) -> tuple:
		# (pow, coefficient)
		def div_terms(dividend: tuple, divisor: tuple) -> tuple:
			return (dividend[0] - divisor[0],
					dividend[1] / divisor[1])

		if type(denom) is Poly:
			if denom.order() > self.order():
				raise ValueError

			out = Poly()
			# numer will be modified, make copy
			numer = deepcopy(self)

			while numer.order() >= denom.order():
				(p, c) = div_terms(
					numer.leading(),
					denom.leading())

				out[p] = c

				# multiply and sub
				numer -= denom * Poly({ p : c })

			return out, numer
		else:
			out = deepcopy(self)

			for p in self.d:
				out[p] /= denom

			return out, 0

	# TRUE DIV NOT SUPPORTED, CANNOT RET REMAINDER
	def __floordiv__(self, denom):
		return self.div_rem(denom)[0]

	# returns remainder of self / denom
	def __mod__(self, denom):
		return self.div_rem(denom)[1]

	# evaluates poly for given x value
	def __call__(self, x: float):
		if x == 0:
			if self.d.get(0):
				return self.d[0]
			else:
				return 0

		acc = 0

		for p, c, in self.d.items():
			acc += c * x ** p

		return acc
	
	# TODO: add Nth derivatives
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
			r, p = p.newton()

			if r is None:
				roots.append(p)
				return roots

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
			d = self[1] ** 2 - 4 * self[2] * self[0]

			if d < 0:
				# could just do sqrt d, but this has cleaner output
				d = cpx(0, (-d) ** 0.5)
			else:
				d = d ** 0.5

			a2 = 2 * self[2]
			return [(-self[1] + d) / a2, (-self[1] - d) / a2]
		else:
			f = self.factors()
			out = []

			for r in f:
				out += r.zeroes()
			
			return out

	# finds a single factor and returns remaining polynomial
	# (factor, remaining)
	def newton(self, imag: bool = False) -> tuple:
		def round_digits(f: float, digits: int = 5) -> float:
			n = 10 ** digits
			return int(f * n) / n

		EPSILON = 0.0000000000001
		MAX_ITER = 1000
	
		d = self.derivative()
		
		x = cpx(0, 1) if imag else 1 # initial guess
		i = 0 # iteration count
		
		while i < MAX_ITER and abs(self(x)) > EPSILON:
			delta = d(x)
	
			if delta != 0:
				x -= self(x) / delta
			else:
				# nudge x
				x -= EPSILON
	
			i += 1
	
		# could not find real roots
		if not i < MAX_ITER:
			if imag:
				# should not happen, didn't find roots in complex plane
				return None, self
			else:
				return self.newton(True)
		
		# round if very close to integer
		if imag:
			x = cpx(round_digits(x.real), round_digits(x.imag))

			if x.imag == 0:
				x = x.real
		else:
			x = round_digits(x)
		
		# factor(x) = x - root
		out = Poly({ 1 : 1, 0 : -x })

		# shouldn't be remainder
		return (out, self // out)
