from numba import jit
import numpy as np
import pygame
import random
import time

@jit
def mandelbrot(creal,cimag,maxiter):
	real = creal
	imag = cimag
	for n in range(maxiter):
		real2 = real*real
		imag2 = imag*imag
		if real2+imag2 > 4.0:
			return n
		imag = 2 * real * imag + cimag
		real = real2 - imag2 + creal
	return 0

@jit
def escapeTime(xmin,xmax,ymin,ymax,width,height,maxiters):
	r1 = np.linspace(xmin,xmax,width)
	r2 = np.linspace(ymin,ymax,height)
	n3 = np.empty((width,height))
	for i in range(width):
		for j in range(height):
			n3[i,j] = mandelbrot(r1[i],r2[j],maxiters)
	
	return (r1,r2,n3)

@jit	
def draw(screen,xmin,xmax,ymin,ymax,img_width,img_height,maxiters):
	print("Calculating...")
	x,y,z = escapeTime(xmin,xmax,ymin,ymax,img_width,img_height,maxiters)
	print("Calculated")
	
	mapping = []
	r = random.randrange(0,255-(img_height%255))
	g = random.randrange(0,255-(img_height%255))
	b = random.randrange(0,255-(img_height%255))
	hue = 10
	for i in range(img_height):
		#tupp = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
		tupp = (r,g,b)
		mapping.append(tupp)
		r = (r+hue) % 255
		#g = (g+hue) % 255
		#b = (b+hue) % 255
	
	row = 0
	col = 0
	#print(z)
	for zz in z:
		for zzz in zz:
			color = (0,0,0)
			if zzz <= 0.0:
				color = (0,0,0)
			else:
				colorIdx = int(zzz) % len(mapping)
				color = mapping[colorIdx] if colorIdx>=0 else (0,0,0)
			screen.set_at((row,col),color)
			col += 1
		col = 0
		row += 1

@jit
def main(screen, xmin, xmax, ymin, ymax, img_width, img_height, maxiters):
	quit = False
	while not quit:
		time.sleep(1)
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					print("Drawing...")
					draw(screen, xmin, xmax, ymin, ymax, img_width, img_height, maxiters)
					print("Drawn")
				if e.key == pygame.K_ESCAPE:
					quit = True
					print("Quitting")
		pygame.display.flip()
	pygame.display.quit()
	
pygame.display.init()
img_width = 400
img_height = 400
#img_width = 20
#img_height = 20
screen = pygame.display.set_mode((img_width,img_height))

if __name__ == "__main__":
	screen.fill((0,0,0))
	
	xStart = -2.0
	xStop = 0.5
	yStart = -1.25
	yStop = 1.25
	xdecrease = 0.3743850
	ydecrease = 0.0520424
	
	xmin = -2.0
	#xmin = -0.74877
	xmax = 0.5
	#xmax = -0.74872
	ymin = -1.25
	#ymin = -1.25*ydecrease
	ymax = 1.25
	#ymax = -0.065013
	maxiters = 250
	
	main(screen, xmin, xmax, ymin, ymax, img_width, img_height, maxiters)
