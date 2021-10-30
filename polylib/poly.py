from sys import exit
from copy import deepcopy

'''
lib functions for polynomial, which is represented as list
of coefficients

ex.
3x^2+2x+1
[3, 2, 1]
'''

class Poly:
	def __init__(self, l: list = None):
		self.l = l if l else [0]

	def __str__(self) -> str:
		if len(self) == 1 and self.l[0] == 0: return '0'

		out = ''

		# loop backwards to print from highest to lowest order
		for i in range(len(self) - 1, -1, -1):
			if self.l[i] == 0: continue

			if i != len(self) - 1 and self.l[i] > 0:
				out += '+'
			
			if i == 0:
				out += str(int(self.l[i]) if self.l[i] % 1 == 0 else self.l[i])
				continue

			# coefficient string '-' if -1, nothing if 1
			coef_str = ''
			if self.l[i] == -1: coef_str = '-'
			elif self.l[i] != 1:
				# don't print decimal if uneccessary
				if self.l[i] % 1 == 0:
					coef_str = str(int(self.l[i]))
				else:
					coef_str = str(self.l[i])

			out += f"{coef_str}{'x' if i != 0 else ''}{('^'+str(i) if i > 1 else '')}"

		return out
	
	def __getitem__(self, pow) -> float:
		return self.l[pow] if pow < len(self) else 0
	def __delitem__(self, pow) -> None: del self.l[pow]
	
	def __setitem__(self, pow, coef) -> None:
		if pow < len(self):
			self.l[pow] = coef
		else:
			for _ in range(pow - len(self)):
				self.l.append(0)

			self.l.append(coef)
	
	def __len__(self) -> int: return len(self.l)

	def __add__(self, o):
		if type(o) is Poly:
			out = deepcopy(self)

			for pow, c in enumerate(o.l):
				out[pow] = c
			
			return out
		elif isinstance(o, float):
			out = deepcopy(self)

			out[0] = out[0] + o

			return out

	def __sub__(self, o):
		return self + o * -1

	def __add__(self, o):
		if type(o) is Poly:
			out = deepcopy(self)

			for pow, c in enumerate(o.l):
				out[pow] = out[pow] + c
			
			return out
		elif type(o) is int or type(o) is float:
			out = deepcopy(self)

			out[0] = out[0] + o

			return out
	
	def __rmul__(self, o): return self * o
	def __mul__(self, o):
		# FOIL
		if type(o) is Poly:
			if len(o) == 1:
				return self.__mul__(o.l[0])
			
			out = Poly()

			# loop through self
			for j in range(len(self)):
				# loop through other
				for i in range(len(o)):
					# multiply
					out[j + i] = out[j + i] + self[j] * o[i]
			
			return out
		elif type(o) is int or type(o) is float:
			out = deepcopy(self)

			for i in range(len(out)):
				out.l[i] *= o

			return out
	
	def derivative(self):
		out = Poly()
	
		for pow, term in enumerate(p.l):
			if pow == 0 or term == 0: continue

			out[pow - 1] = pow * term
	
		return out