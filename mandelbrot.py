import cmath
import pygame

from random import randrange as rr
from time import sleep

done = False
winx = 0
winy = 0
x_scale = -1.0
y_scale = 0.0
x_zoom = 1.0
y_zoom = 1.0

#x_scale = -0.01
#y_scale = 0.05
#x_zoom = 5.0
#y_zoom = 10.0
redraw = True

def scale(i, mp):
	if mp == 0:
		return i
	return (i - mp) / mp

def update(mid,debug=False):
	global done, x_zoom, y_zoom, x_scale, y_scale, redraw
	
	scaling_factor = 75
	zoom_factor = 0.75
	half_scaling_factor = scaling_factor // 2
	quarter_scaling_factor = half_scaling_factor // 2
	eighth_scaling_factor = quarter_scaling_factor // 2

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			done = True
			break

		if e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 4 or e.button == 5:
				pos = pygame.mouse.get_pos()
				posvec = pygame.math.Vector2(pos[0], pos[1])
				diffvec = posvec - mid
				if not diffvec.is_normalized():
					try:
						diffvec.normalize_ip()
					except:
						pass

				# Scale the magnitude down to something manageable
				diffvec /= 10

				if debug:
					print("diffvec.x", diffvec.x)
					print("diffvec.y", diffvec.y)

				x_zoom_factor = abs(diffvec.x) * zoom_factor
				y_zoom_factor = abs(diffvec.y) * zoom_factor
				if e.button == 4: # zoom in
					x_zoom_factor = abs(diffvec.x) * zoom_factor
					y_zoom_factor = abs(diffvec.y) * zoom_factor

					x_zoom += x_zoom_factor
					y_zoom += y_zoom_factor

					x_scale += diffvec.x / quarter_scaling_factor
					y_scale += diffvec.y / eighth_scaling_factor
				elif e.button == 5: # zoom out
					x_zoom -= x_zoom_factor
					y_zoom -= y_zoom_factor

					x_scale -= diffvec.x / quarter_scaling_factor
					y_scale -= diffvec.y / eighth_scaling_factor

				if debug:
					print("x_scale", x_scale)
					print("y_scale", y_scale)
					print("x_zoom", x_zoom)
					print("y_zoom", y_zoom)
					print("")
				redraw = True
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				x_scale = -1.0
				y_scale = 0.0
				x_zoom = 1.0
				y_zoom = 1.0
				if debug:
					print("reset")
				redraw = True
			if e.key == pygame.K_ESCAPE:
				done = True
				break

def render(screen, midpoint, palette, max_iters, debug=False):
	global winx, winy, x_scale, y_scale, x_zoom, y_zoom, redraw
	while redraw:
		redraw = False
		screen.fill((0,0,0))
		lxzoom = x_zoom
		lyzoom = y_zoom
		lx_scale = x_scale
		ly_scale = y_scale
		for i in range(winx):
			update(midpoint,debug)
			if done or redraw:
				break
			for j in range(winy):
				x0 = scale(i, midpoint.x * lxzoom) + lx_scale
				y0 = scale(j, midpoint.y * lyzoom) + ly_scale
				x = 0.0
				y = 0.0
				x2 = 0
				y2 = 0
				iter = 0
				while (x2 + y2 <= 4 and iter < max_iters):
					y = 2 * x * y + y0
					x = x2 - y2 + x0
					x2 = x * x
					y2 = y * y
					iter += 1

				# if iter == max_iters, it's in the mandelbrot set
				screen.set_at((i,j), palette[iter])
			pygame.display.flip()
	pygame.display.flip()

def main(wx,wy):
	global done, winx, winy, mousedown, redraw
	winx = wx
	winy = wy
	
	if winx == 0 or winy == 0:
		print("Need window values > 0")
		return

	pygame.display.init()
	screen = pygame.display.set_mode((winx, winy))
	midpoint = pygame.math.Vector2(winx//2, winy//2)

	# Mandelbrot x scale (-2.00, 0.47)
	# Mandelbrot y scale (-1.12, 1.12)
	max_iters = 1000
	palette = {max_iters:(0,0,0)}
	for i in range(max_iters):
		r1 = rr(0,255)
		r2 = rr(0,255)
		r3 = rr(0,255)
		palette[i] = (min(255,i + r1), min(255,i + r2), min(255,i + r3))

	done = False
	while not done:
		update(midpoint)
		if redraw:
			#print("Rendering...")
			render(screen, midpoint, palette, max_iters)
			#print("Done rendering.")
		if done:
			continue
		sleep(0.5)

	pygame.display.quit()

main(300,300)
