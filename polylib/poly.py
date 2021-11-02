from copy import deepcopy

class Poly:
	def __init__(self, d = None):
		self.d = d if d else {}
		self.leading = 0
	
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
			self.leading = max(self.leading, pow)
			self.d[pow] = coef
	def __getitem__(self, pow) -> float:
		v = self.d.get(pow)
		return v if v is not None else 0
	def __delitem__(self, pow):
		if self.d.get(pow) is not None:
			del self.d[pow]

			if pow == self.leading:
				self.leading = max(self.d.keys())
	
	def __len__(self) -> int: return len(self.d)

	def __sub__(self, o):
		return self + o * -1
	
	def __iadd__(self, o):
		if type(o) is Poly:
			for p, c in o.d.items():
				self.d[p] = self[p] + c

			return self
		elif type(o) is int or type(o) is float:
			self.d[0] += o

			return self

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
				out.d[p] *= o

			return out
	
	def derivative(self):
		out = Poly()
	
		for p, c in self.d.items():
			out[p - 1] = p * c
	
		return out

	def eval(self, x: float) -> float:
		sum = 0

		for p, c, in self.d.items():
			sum += c * x ** p

		return sum
	
	def order(self) -> int:
		return self.leading
