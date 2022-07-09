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
	pg.init()

	screen = pg.display.set_mode((500, 500))

	w = Window(500, 500)

	plane = Plane((-10, 10), (-10, 10), lbl_mode=Plane.MODE_CPXLBL, axes_only=False)

	# w.add(CpxGraph(plane, lambda x: x ** 4 + 625, CpxGraph.MODE_HSV))
	w.add(Graph(plane, lambda x: 2 ** x))
	w.add(plane)
	w.draw(screen)

if __name__ == '__main__':
	plot_demo()
