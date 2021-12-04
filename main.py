from polylib.parse import parse

def main():
	a = parse('6x^2-5x+1')
	b = parse('3x+2')

	# a = parse(input('input poly a: '))
	# b = parse(input('input poly b: '))

	print(a)
	print(b)
	print()

	print(f'a/b = {a//b} r {a%b}')
	print(f'a*b = {a*b}')

	print(f'factors of a: {a.factors()}')
	print(f'zeroes of a:  {a.zeroes()}')

if __name__ == '__main__':
	main()
