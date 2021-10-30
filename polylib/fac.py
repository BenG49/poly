from .poly import Poly

def rat_roots(p: Poly) -> set:
	if len(p) < 2: return None

	# all terms must be integers
	for n in p.l:
		if n % 1 != 0:
			return None

	top_roots = [n for n in range(1, int(p[-1])+1) if int(p[-1]) % n == 0]
	bot_roots = [n for n in range(1, int(p[0])+1) if int(p[0]) % n == 0]

	out = set([])

	for q in top_roots:
		for p in bot_roots:
			out.add(p / q)
			out.add(-p / q)
	
	return out

def fac(p: Poly) -> list:
	pass
