from .poly import Poly

def parse(s: str):
	out = Poly()

	prev = ''
	c = 1
	pow = 0

	i = 0
	while i < len(s):
		if s[i] == ' ':
			i += 1
			continue

		elif s[i].isdigit() or s[i] == '.':
			tmp = ''
			while i < len(s) and (s[i].isdigit() or s[i] == '.'):
				tmp += s[i]
				i += 1

			i -= 1 # i will be incremented later

			# number can be power or coefficient
			if prev == '^':
				pow = int(tmp)
			else:
				# multiply to preserve sign
				c *= float(tmp)
		else:
			# last char was carat, current char isnt num
			if prev == '^':
				exit(f'Parse error: no number after carat at index {i}!')

			if s[i] in '+-':
				# if not leading negatigve sign
				if prev != '':
					out[pow] = c

				# reset for new term
				c = -1 if s[i] == '-' else 1
				pow = 0

			# for case where x has no power
			elif s[i] == 'x': pow = 1

			# ignored, instead of processing here last_char is used
			elif s[i] == '^': pass

			else:
				exit(f'Error: invalid character {s[i]} at index {i}!')

		if i == len(s):
			break

		prev = s[i]
		i += 1

	out[pow] = c

	return out
