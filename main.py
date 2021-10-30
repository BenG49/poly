from polylib.parse import parse

def main():
	a = parse(input('input poly a: '))
	print(a)
	b = parse(input('input poly b: '))
	print(b)

	print(f'a*b={a*b}')

if __name__ == '__main__':
	main()
