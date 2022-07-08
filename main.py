import os

from polylib.parse import parse
from polylib.poly import Poly
from polylib.graph import *

import pygame as pg

def poly_demo():
	a = parse('x^2+1')
	b = parse('3x+2')

	print('a:', a)
	print('b:', b)
	print()

	print(f'a/b = {a//b} r {a%b}')
	print(f'a*b = {a*b}')

	print(f'factors of a: {a.factors()}')
	print(f'zeroes of a:  {a.zeroes()}')

	print(Poly.lagrange([(0, 1), (1, -2), (2, 5)]))

def plot_demo():
	screen = pg.display.set_mode((500, 500))

	w = Screen(500, 500)

	plane = Plane((-10, 10), (-10, 10), True)

	w.add(CpxGraph(plane, lambda x: x * x + 1, CpxGraph.MODE_HSV))
	w.add(Graph(plane, lambda x: x * x + 1))
	w.add(plane)
	
	w.draw(screen)

	running = True
	while running:
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
			elif e.type == pg.KEYDOWN:
				# ctrl + s
				if e.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.image.save(screen, os.path.join(
						os.getcwd(),
						input('FILENAME:').split('.')[0] + '.jpg'))
		
		pg.display.flip()

if __name__ == '__main__':
	plot_demo()
