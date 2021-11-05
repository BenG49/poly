from copy import deepcopy
from .poly import Poly

# all terms must be integers
def rat_roots(p: Poly) -> set:
	if len(p) < 2: return None

	top = int(p[p.order()])
	bot = int(p[0])

	out = set([])

	# all combinations of factors of highest and lowest coefficients
	for q in [n for n in range(1, top+1) if top % n == 0]:
		for p in [n for n in range(1, bot+1) if bot % n == 0]:
			out.add(p / q)
			out.add(-p / q)

	return out

# (root, unfactorable poly)
def newton(p: Poly) -> tuple:
	EPSILON = 0.0000000000001
	MAX_ITER = 100

	d = p.derivative()

	x = 1
	delta = 1
	iter = 0

	while delta > EPSILON and iter < MAX_ITER:
		delta = p(x) / d(x)
		x -= delta
		iter += 1
	
	if not iter < MAX_ITER:
		return None

	return (x, p // Poly({ 1 : 1, 0 : -x }))

# (list of roots, unfactorable poly)
def fac(p: Poly) -> tuple:
	out = []

	while p.order() > 1:
		found_root = False
		roots = rat_roots(p)

		for r in roots:
			r_p = Poly({ 1 : 1, 0 : -r })
			print(r_p)
			if p % r_p == 0:
				out.append(r)
				p = p // r_p

				found_root = True
				break

		if not found_root:
			return out, p
	
	return out, Poly()
