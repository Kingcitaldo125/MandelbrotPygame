import cmath
import pygame

from random import randrange as rr
from time import sleep

done = False
winx = 0
winy = 0
x_scale = 0.0
y_scale = 0.0

def scale(i, mp):
	return (i - mp) / mp

def check_events():
	global done, x_scale, y_scale
	events = pygame.event.get()
	retv = None

	for e in events:
		if e.type == pygame.QUIT:
			done = True
			break

		if e.type == pygame.MOUSEBUTTONDOWN:
			retv = pygame.mouse.get_pos()
			print("mousedown")
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				x_scale = 0.0
				y_scale = 0.0
				print("reset")
				retv = (winx//2, winy//2)
			if e.key == pygame.K_ESCAPE:
				done = True
				break

	return retv

def render(screen, midpointx, midpointy):
	global winx, winy, x_scale, y_scale
	screen.fill((0,0,0))

	# mandelbrot x scale (-2.00, 0.47)
	# mandelbrot y scale (-1.12, 1.12)
	max_iters = 1000
	palette = {max_iters:(0,0,0)}
	for i in range(max_iters):
		r1 = rr(0,255)
		r2 = rr(0,255)
		r3 = rr(0,255)
		palette[i] = (min(255,i + r1), min(255,i + r2), min(255,i + r3))

	for i in range(winx):
		if done:
			break
		for j in range(winy):
			if done:
				break

			x0 = scale(i, midpointx) + x_scale
			y0 = scale(j, midpointy) + y_scale
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

	print("Done rendering.")
	pygame.display.flip()

def main(wx,wy):
	global done, winx, winy
	winx = wx
	winy = wy
	
	if winx == 0 or winy == 0:
		print("Need window values > 0")
		return

	pygame.display.init()
	screen = pygame.display.set_mode((winx, winy))
	midpointx = winx // 2
	midpointy = winy // 2

	render(screen, midpointx, midpointy)
	sleep(5)
	done = True
	while not done:
		mget = check_events()
		if mget:
			posx = mget[0]
			posy = mget[1]
			xscale = scale(posx, midpointx)
			yscale = scale(posy, midpointy)
			render(screen, winx, winy, xscale, yscale)

		sleep(0.25)
	pygame.display.quit()

main(400,400)
