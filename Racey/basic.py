import pygame
import time
import random

# intialise the pygame module
pygame.init()

crash_sound = pygame.mixer.Sound("Crash.wav")
pygame.mixer.music.load("Jazz_In_Paris.wav")

# dynamic screen resolution
display_width = 800
display_height = 600

# color definitions
black = (0,0,0)
white = (255,255,255)
block_color = (53, 115, 255)

red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)

bright_red = (255, 0,0)
bright_green = (0,255,0)

car_width = 73

pause = False

# creates a display / frame / window for the game
# with single parameter (tuple of dimensions)
gameDisplay = pygame.display.set_mode((display_width,display_height))
# setting up the caption for the window
pygame.display.set_caption('A bit Racey')
# setting clock of the game
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')

# setting up the icon of the game
pygame.display.set_icon(carImg)

def things_dodged(count):
	font = pygame.font.SysFont('comicsansms', 25)
	text = font.render("Dodged: "+str(count), True, black)
	gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
	pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
	# draws image on the window
	gameDisplay.blit(carImg, (x,y))

def text_objects(msg, font):
	textSurface = font.render(msg, True, black)
	return textSurface, textSurface.get_rect()

def message_display(msg):
	largeText = pygame.font.SysFont('comicsansms', 115)
	TextSurf, TextRect = text_objects(msg, largeText)
	TextRect.center = ((display_width/2), (display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()

	time.sleep(2)
	game_loop()

def crash():

	pygame.mixer.music.stop()
	pygame.mixer.Sound.play(crash_sound)

	largeText = pygame.font.SysFont('comicsansms', 115)
	TextSurf, TextRect = text_objects("You Crashed", largeText)
	TextRect.center = ((display_width/2), (display_height/2))
	gameDisplay.blit(TextSurf, TextRect)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# gameDisplay.fill(white)

		button("Play Again",150,450,100,50,green,bright_green,game_loop)
		button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

def quitgame():
	pygame.quit()
	quit()

def unpaused():
	global pause
	pygame.mixer.music.unpause()
	pause = False

def paused():

	pygame.mixer.music.pause()

	largeText = pygame.font.SysFont('comicsansms', 115)
	TextSurf, TextRect = text_objects("Paused", largeText)
	TextRect.center = ((display_width/2), (display_height/2))
	gameDisplay.blit(TextSurf, TextRect)
	
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# gameDisplay.fill(white)

		button("Continue",150,450,100,50,green,bright_green,unpaused)
		button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

# ic = inactive color, ac = active color
def button(msg,x,y,w,h,ic,ac, action=None):
	mouse = pygame.mouse.get_pos()
	# (l,m,r) = left, middle, right button click on mouse
	click = pygame.mouse.get_pressed()
	# add buttons and interaction
	# lighten up the buttons
	if x+w>mouse[0]>x and y+h>mouse[1]>y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action!=None:
			action()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h)) 

	# text on button
	smallText = pygame.font.SysFont('comicsansms',20)
	textSurf, textRect = text_objects(msg,smallText)
	textRect.center = (x+(w/2), y+(h/2))
	gameDisplay.blit(textSurf, textRect)


def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		largeText = pygame.font.SysFont('comicsansms', 115)
		TextSurf, TextRect = text_objects("A Bit Racey", largeText)
		TextRect.center = ((display_width/2), (display_height/2))
		gameDisplay.blit(TextSurf, TextRect)

		button("GO!",150,450,100,50,green,bright_green,game_loop)
		button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)


def game_loop():
	global pause

	pygame.mixer.music.play(-1)



	x = display_width * 0.45
	y = display_height * 0.8
	x_change = 0
	
	# things' measurements
	thing_starty = -600
	thing_speed = 7
	thing_width = 100
	thing_height = 100
	thing_startx = random.randrange(0, (display_width-thing_width)//1)

	# score
	dodged = 0
	thing_count = 1

	# variable that handles the running and closing state of the game
	game_exit = False

	# GAME LOOP
	while not game_exit:
		# pygame.event.get() gives the list of all the events that occured per frame per second
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
				pygame.quit()
				quit()

			# key is pressed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
				if event.key == pygame.K_p:
					pause = True
					paused()


			# key is released
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		x += x_change

		# fills the window with white
		gameDisplay.fill(white)

		# things generation
		things(thing_startx, thing_starty, thing_width, thing_height, block_color)
		thing_starty += thing_speed
		car(x,y)
		things_dodged(dodged)

		if x>display_width-car_width or x<0:
			crash()

		# to create a new thing as soon as one goes out of the window
		if thing_starty > display_height:
			thing_starty = 0- thing_height
			thing_startx = random.randrange(0, (display_width-thing_width)//1)
			dodged += 1
			thing_speed += 1
			thing_width += (dodged * 1.2)

		# y crossover
		if y<thing_starty+thing_height:
			# x crossover
			if x>thing_startx-car_width and x<thing_startx+thing_width:
				crash()

		# function updates the window (renders the updated version)
		pygame.display.update()
		# argument - number of frames per second (fps)
		# more the fps, smoother the game will be
		clock.tick(60)

game_intro()
game_loop()
# quit from the window
pygame.quit()
# command to close the python program
quit()