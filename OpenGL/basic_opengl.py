import pygame
from pygame.locals import *
# OpenGL brings our objects to life
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
	(1,-1,-1),
	(1,1,-1),
	(-1,1,-1),
	(-1,-1,-1),
	(1,-1,1),
	(1,1,1),
	(-1,-1,1),
	(-1,1,1),
	)

edges = (
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7),
	)

surfaces = (
	(0,1,2,3),
	(3,2,7,6),
	(6,7,5,4),
	(4,5,1,0),
	(1,5,7,2),
	(4,0,3,6),
	)

colors = (
	(1,0,0),
	(0,1,0),
	(0,0,1),
	(0,1,0),
	(1,1,1),
	(0,1,1),
	(1,0,0),
	(0,1,0),
	(0,0,1),
	(1,0,0),
	(1,1,1),
	(0,1,1),
	)

def Cube():
	# every OpenGL code is enclosed within glBegin() and glEnd()

	glBegin(GL_QUADS)
	for surface in surfaces:
		x = 0
		for vertex in surface:
			x+=1
			# (r,g,b)
			glColor3fv(colors[x])
			glVertex3fv(vertices[vertex])

	glEnd()

	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()

def main():
	pygame.init()
	display = (800,600)
	# notify pygame that its display is set to OpenGL
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

	# field of view (degrees), aspect ratio, zNear (near clipping plane distance), zFar (far clipping plane distance)
	gluPerspective(45, (display[0]/display[1]),0.1,50.0)
	
	# the translation from the origin (x,y,z)
	glTranslatef(0.0,0.0,-10)	

	# (angle, x, y, z) - angle with which you want to rotate
	# (x,y,z) - the axis about which you want to rotate
	glRotatef(25,2,1,0)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					glTranslatef(-1,0,0)
				if event.key == pygame.K_RIGHT:
					glTranslatef(1,0,0)

				if event.key == pygame.K_UP:
					glTranslatef(0,1,0)
				if event.key == pygame.K_DOWN:
					glTranslatef(0,-1,0)

			if event.type == pygame.MOUSEBUTTONDOWN: 
				# mouse wheel is rolling
				if event.button == 4:
					glTranslatef(0,0,1.0)
				if event.button == 5:
					glTranslatef(0,0,-1.0)


		# glRotatef(1,3,1,1)

		# clear the slate clean
		# args are the things that we want to clear
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Cube()
		# update() doesn't work here with OpenGL
		pygame.display.flip()
		pygame.time.wait(10) # in milliseconds

main()