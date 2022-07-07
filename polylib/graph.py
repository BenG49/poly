from random import sample
from typing import Any, Callable, Sequence, Tuple
import pygame as pg

'''
Drawable
- draw(screen)

Plane extends Drawable
- xrange, yrange, xstep=1, ystep=1
'''

def transform(val, min_in, max_in, min_out, max_out):
	return ((val - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out


class Drawable:
	def draw(self, screen) -> None:
		...

def kwarg(self, kwargs: dict, key: str, default: Any) -> None:
	self.__dict__[key] = kwargs[key] if (key in kwargs) else default

class Screen(Drawable):
	def __init__(self, width: int, height: int) -> None:
		self.width = width
		self.height = height
		
		# list of drawables, drawn in order
		self.layers = []

	def add(self, drawable: Drawable) -> None:
		self.layers.append(drawable)

	def draw(self, screen) -> None:
		screen.fill((0, 0, 0))

		for layer in self.layers:
			layer.draw(screen)

'''
add axis labels
fix tick spacing
'''
class Plane(Drawable):
	ORIGIN_AXES_THICKNESS = 3

	def __init__(self, xrange: Sequence[float], yrange: Sequence[float]):
		self.xrange = xrange
		self.yrange = yrange

	def world_coord(self, screen, screen_cord: Tuple[int]) -> Tuple[float]:
		w, h = screen.get_size()

		return (transform(
					screen_cord[0],
					0, w,
					*self.xrange),
				transform(
					screen_cord[1],
					0, h,
					*self.yrange))

	def screen_cord(self, screen, world_coord: Tuple[float]) -> Tuple[int]:
		w, h = screen.get_size()

		return (int(transform(
					world_coord[0],
					*self.xrange,
					0, w)),

				int(transform(
					world_coord[1],
					*self.yrange,
					0, h)))

	def draw(self, screen) -> None:
		w, h = screen.get_size()

		# horizontal lines
		for y in range(*self.yrange):
			sy = self.screen_cord(screen, (0, y))[1]

			pg.draw.line(
				screen,
				'white',
				(0, sy),
				(w, sy),
				Plane.ORIGIN_AXES_THICKNESS if y == 0 else 1)

		for x in range(*self.xrange):
			sx = self.screen_cord(screen, (x, 0))[0]

			pg.draw.line(
				screen,
				'white',
				(sx, 0),
				(sx, h),
				Plane.ORIGIN_AXES_THICKNESS if x == 0 else 1)

class Graph(Drawable):
	def __init__(self, plane: Plane, func: Callable[[float], float], sample_step: int = 3):
		self.plane = plane
		self.func = func
		self.sample_step = sample_step

	def draw(self, screen) -> None:
		prev = None

		for x in range(0, screen.get_size()[0], self.sample_step):
			wx = self.plane.world_coord(screen, (x, 0))[0]
			wy = self.func(wx)
			
			if prev:
				pg.draw.line(
					screen,
					'green',
					self.plane.screen_cord(screen, prev),
					self.plane.screen_cord(screen, (wx, wy)))
			
			prev = (wx, wy)
