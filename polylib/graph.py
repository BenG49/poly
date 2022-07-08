from math import atan2, pi
from typing import Any, Callable, Sequence, Tuple
from .cpx import cpx
import pygame as pg

'''
Drawable
- draw(screen)

Plane extends Drawable
- xrange, yrange, xstep=1, ystep=1
'''

def map_range(val: float, min_in: float, max_in: float, min_out: float, max_out: float) -> float:
	return ((val - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out

def clamp(x: float, min_val: float, max_val: float) -> float:
	return max(min(x, max_val), min_val)

def angle(x: float, y: float, min_val: float, max_val: float) -> float:
	zero_to_one = atan2(x, y) / (2 * pi)
	if zero_to_one < 0:
		zero_to_one += 1
	
	return zero_to_one * (max_val - min_val) + min_val


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

		return (map_range(
					screen_x,
					0, w,
					*self.x_range),
				map_range(
					screen_y,
					h, 0,
					*self.y_range))

	def screen_cord(self, screen, graph_x: float, graph_y: float) -> Tuple[int]:
		w, h = screen.get_size()

		return (int(map_range(
					graph_x,
					*self.x_range,
					0, w)),

				int(map_range(
					graph_y,
					*self.y_range,
					h, 0)))

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

	def __init__(self, plane: Plane, func: Callable[[float], float], color: Tuple[int] = (120, 200, 240), sample_step: int = 3):
		self.plane = plane
		self.func = func
		self.color = color
		self.sample_step = sample_step

	def draw(self, screen) -> None:
		prev = None

		for x in range(0, screen.get_size()[0], self.sample_step):
			wx = self.plane.graph_coord(screen, x, 0)[0]
			wy = self.func(wx)
			
			if prev:
				pg.draw.line(
					screen,
					self.color,
					self.plane.screen_cord(screen, *prev),
					self.plane.screen_cord(screen, wx, wy),
					Graph.THICKNESS)
			
			prev = (wx, wy)

class CpxGraph:
	# treats output angle as hue and magnitude as value
	MODE_HSV = 0
	# uses colormap to map function output to input
	MODE_COLORMAP = 1
	# colors based on real value of function output
	MODE_REAL = 2
	# colors based on imaginary value of function output
	MODE_IMAG = 3

	def __init__(self, plane: Plane, func: Callable[[cpx], cpx], mode: int = 0):
		self.plane = plane
		self.func = func
		self.mode = mode

	def draw(self, screen):
		w, h = screen.get_size()

		# x and y in [0, 1]
		def colormap(x: float, y: float) -> Tuple[int]:
			# t must be in [0, 1]
			def rgb_interp(t: float, *args) -> float:
				points = list(zip((i * 0.25 for i in range(5)), args))

				for i in range(1, len(points)):
					if points[i - 1][0] <= t and points[i][0] >= t:
						left = points[i - 1]
						right = points[i]
						
						break

				slope = (right[1] - left[1]) / (right[0] - left[0])
				val = slope * t + left[1] - (slope * left[0])
				return int(clamp(val, 0, 255))

			# rotate angle by 90 degrees
			ang = angle(x, y, 0, 1) + 0.25
			if ang > 1:
				ang -= 1

			r = rgb_interp(ang, 0, 0, 255, 255, 0)
			g = rgb_interp(ang, 0, 0, 255, 0, 0)
			b = rgb_interp(ang, 0, 255, 255, 0, 0)

			return (r, g, b)

		def hsv(x: float, y: float, max_mag: float) -> Tuple[float]:
			h = angle(x, y, 0, 6)
			s = 1
			v = clamp(((x ** 2 + y ** 2) ** 0.5) / max_mag, 0, 1)

			c = s * v
			n = c * (1 - abs(h % 2 - 1))

			if h < 1:   coords = (c, n, 0)
			elif h < 2: coords = (n, c, 0)
			elif h < 3: coords = (0, c, n)
			elif h < 4: coords = (0, n, c)
			elif h < 5: coords = (n, 0, c)
			else:       coords = (c, 0, n)

			return tuple(int(255 * (i + v - c)) for i in coords)

		x_delta = self.plane.x_len() / w
		y_delta = self.plane.y_len() / h

		# loop through graph coordinates
		y = self.plane.y_range[1]
		sy = 0
		while y >= self.plane.y_range[0]:
			x = self.plane.x_range[0]
			sx = 0
			while x <= self.plane.x_range[1]:
				z_out = self.func(cpx(x, y))

				if self.mode != CpxGraph.MODE_HSV:
					# in range [-1, 1]
					x_out = z_out.real / self.plane.x_len() * 2
					y_out = z_out.imag / self.plane.y_len() * 2

				if self.mode == CpxGraph.MODE_HSV:
					rgb = hsv(*z_out, self.plane.x_len() / 2)
				elif self.mode == CpxGraph.MODE_COLORMAP:
					rgb = colormap(x_out, y_out)
				elif self.mode == CpxGraph.MODE_REAL:
					rgb = (int(255 * clamp(x_out, 0, 1)), int(255 * clamp(-x_out, 0, 1)), 0)
				elif self.mode == CpxGraph.MODE_IMAG:
					rgb = (int(255 * clamp(y_out, 0, 1)), int(255 * clamp(-y_out, 0, 1)), 0)

				screen.set_at((sx, sy), rgb)

				x += x_delta
				sx += 1

			y -= y_delta
			sy += 1
