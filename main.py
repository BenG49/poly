from polylib.poly import Poly
from polylib.parse import parse

def main():
	p = Poly()
	p[-1] = 10
	print(p)
	print(p.derivative())

	a = parse(input('input poly a: '))
	print(a)
	b = parse(input('input poly b: '))
	print(b)

	c = a * b

	print(f'a*b={c}')
	print(f'f(3)={c.eval(3)}')
	print(f'a order: {a.order()}, b order: {b.order()}')

if __name__ == '__main__':
	main()
