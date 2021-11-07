from polylib.parse import parse

def main():
	# a = parse('x^2+5x-6')
	# b = parse('x-1')

	a = parse(input('input poly a: '))
	print(a)
	b = parse(input('input poly b: '))
	print(b)

	print(f'a/b = {a//b} r {a%b}')

	print(f'factors of a: {a.factors()}')
	print(f'zeroes of a:  {a.zeroes()}')

if __name__ == '__main__':
	main()
