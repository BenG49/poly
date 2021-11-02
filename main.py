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

	print(f'a/b = {a//b} r {a%b}')

if __name__ == '__main__':
	main()
