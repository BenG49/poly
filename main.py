from polylib.parse import parse

def main():
	a = parse(input('input poly a: '))
	print(a)
	b = parse(input('input poly b: '))
	print(b)

	c = a * b

	print(f'a*b={c}')
	print(f'f(3)={c.eval(3)}')

if __name__ == '__main__':
	main()
