from polylib.parse import parse
from polylib.poly import Poly

if __name__ == '__main__':
	a = parse('x^2+1')
	b = parse('3x+2')

	# a = parse(input('input poly a: '))
	# b = parse(input('input poly b: '))

	print('a:', a)
	print('b:', b)
	print()

	print(f'a/b = {a//b} r {a%b}')
	print(f'a*b = {a*b}')

	print(f'factors of a: {a.factors()}')
	print(f'zeroes of a:  {a.zeroes()}')

	print(Poly.lagrange([(0, 1), (1, -2), (2, 5)]))
