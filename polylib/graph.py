from math import atan2, pi
from typing import Any, Callable, List, Sequence, Tuple
from .cpx import cpx
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

	def __init__(self, x_range: Sequence[float], y_range: Sequence[float]):
		self.x_range = x_range
		self.y_range = y_range

	def graph_coord(self, screen, screen_x: int, screen_y: int) -> Tuple[float]:
		w, h = screen.get_size()

		return (transform(
					screen_x,
					0, w,
					*self.x_range),
				transform(
					screen_y,
					0, h,
					*self.y_range))

	def screen_cord(self, screen, graph_x: float, graph_y: float) -> Tuple[int]:
		w, h = screen.get_size()

		return (int(transform(
					graph_x,
					*self.x_range,
					0, w)),

				int(transform(
					graph_y,
					*self.y_range,
					0, h)))

	def x_len(self):
		return self.x_range[1] - self.x_range[0]

	def y_len(self):
		return self.y_range[1] - self.y_range[0]

	def draw(self, screen) -> None:
		w, h = screen.get_size()

		# horizontal lines
		for y in range(*self.y_range):
			sy = self.screen_cord(screen, 0, y)[1]

			pg.draw.line(
				screen,
				'white',
				(0, sy),
				(w, sy),
				Plane.ORIGIN_AXES_THICKNESS if y == 0 else 1)

		for x in range(*self.x_range):
			sx = self.screen_cord(screen, x, 0)[0]

			pg.draw.line(
				screen,
				'white',
				(sx, 0),
				(sx, h),
				Plane.ORIGIN_AXES_THICKNESS if x == 0 else 1)

class Graph(Drawable):
	THICKNESS = 2

	def __init__(self, plane: Plane, func: Callable[[float], float], sample_step: int = 3):
		self.plane = plane
		self.func = func
		self.sample_step = sample_step

	def draw(self, screen) -> None:
		prev = None

		for x in range(0, screen.get_size()[0], self.sample_step):
			wx = self.plane.graph_coord(screen, x, 0)[0]
			wy = self.func(wx)
			
			if prev:
				pg.draw.line(
					screen,
					'green',
					self.plane.screen_cord(screen, *prev),
					self.plane.screen_cord(screen, wx, wy),
					Graph.THICKNESS)
			
			prev = (wx, wy)

class CpxColorGraph:
	def __init__(self, plane: Plane, func: Callable[[cpx], cpx]):
		self.plane = plane
		self.func = func

	def draw(self, screen):
		w, h = screen.get_size()

		def clamp(x: float, min_val: float, max_val: float) -> float:
			return max(min(x, max_val), min_val)

		# x and y normalized between 0 and 1
		def colormap(x: float, y: float) -> Tuple[int]:
			def rgb_interp(t: float, *args) -> float:
				points = list(zip((i * 0.25 for i in range(5)), args))

				left, right = (0, 0), (0, 0)

				if t < points[0][0]:
					left = points[0]
					right = points[1]
				elif x > points[-1][0]:
					left = points[-2]
					right = points[-1]
				else:
					for i in range(1, len(points)):
						if points[i - 1][0] <= t and points[i][0] >= t:
							left = points[i - 1]
							right = points[i]
							
							break

				slope = ((right[1] - left[1]) / (right[0] - left[0]))
				val = int(slope * t + left[1] - (slope * left[0]))
				return clamp(val, 0, 255)

			# normalize angle from 0 to 1, rotate by 90 degrees
			rad = atan2(x, y) / (2 * pi) + 0.25
			if rad < 0:
				rad += 1

			r = rgb_interp(rad, 0, 0, 255, 255, 0)
			g = rgb_interp(rad, 0, 0, 255, 0, 0)
			b = rgb_interp(rad, 0, 255, 255, 0, 0)

			return (r, g, b)

		x_delta = self.plane.x_len() / w
		y_delta = self.plane.y_len() / h

		# loop through graph coordinates
		y = self.plane.y_range[0]
		sy = 0
		while y <= self.plane.y_range[1]:
			x = self.plane.y_range[0]
			sx = 0
			while x <= self.plane.x_range[1]:
				z_out = self.func(cpx(x, y))

				# in range [-1, 1]
				x_out = z_out.real / self.plane.x_len() * 2
				y_out = z_out.imag / self.plane.y_len() * 2

				screen.set_at(
					(sx, sy),
					colormap(x_out, y_out))
					# (int(255 * clamp(x_out, 0, 1)), int(255 * clamp(-x_out, 0, 1)), 0))
					# (int(255 * clamp(y_out, 0, 1)), int(255 * clamp(-y_out, 0, 1)), 0))


				x += x_delta
				sx += 1

			y += y_delta
			sy += 1

		# slightly slower
		# for sy in range(h):
		# 	for sx in range(w):
		# 		z_out = self.func(
		# 			cpx(*self.plane.graph_coord(screen, sx, sy)))

		# 		# x and y are in range [-1, 1]
		# 		x = z_out.real / self.plane.x_len() * 2
		# 		y = z_out.imag / self.plane.y_len() * 2

		# 		screen.set_at(
		# 			(sx, sy),
		# 			colormap(x, y))
		# 			# (int(255 * clamp(x, 0, 1)), int(255 * clamp(-x, 0, 1)), 0))
		# 			# (int(255 * clamp(y, 0, 1)), int(255 * clamp(-y, 0, 1)), 0))
