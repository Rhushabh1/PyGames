import pygame
import time
from towerSolver import *
from Colors import *


pygame.font.init()
clock = pygame.time.Clock()
delay = 10

colors = [red[1], green[1], yellow[1], blue[1], magenta[1], orange[1], chocolate[1]]
i_colors = [red[1], green[1], yellow[1], blue[1], magenta[1], orange[1], chocolate[1]]

# start_pole = []
# helper_pole = []
# end_pole = []


class Game:
	def __init__(self, game_width, game_height, puck_count=7):
		pygame.display.set_caption("Tower Of Hanoi")
		self.game_width = game_width
		self.game_height = game_height
		self.gameDisplay = pygame.display.set_mode((game_width, game_height))
		self.puck_count = puck_count
		self.score = 0
		self.solution = None
		self.pole_length = 0.5*game_height
		self.poles_xs = [0.25*i*game_width for i in range(1, 4)]
		self.base_coord = (game_height+self.pole_length)/2
		
		self.puck_height = self.pole_length/(puck_count+1)
		self.puck_width = [(0.25*game_width*i)/puck_count for i in range(1, 8)]
		self.pucks_ys = [(self.base_coord-(0.5+i)*self.puck_height) for i in range(puck_count)]
		self.reset_button = None
		self.solve_button = None

	# intialise pucks status
	def initialise_game(self):
		self.score = 0
		start_pole = [Puck(i+1, self.poles_xs[0], self.pucks_ys[self.puck_count-i-1], self.poles_xs[0]/4, self.puck_height, self.puck_width[i], self.puck_height, colors[i], i_colors[i]) for i in range(self.puck_count)]
		start_pole = start_pole[::-1]
		helper_pole = []
		end_pole = []
		self.poles = [start_pole, helper_pole, end_pole]

	def set_solution(self):
		self.solution = transfer_function(0,2,1,self.puck_count)

	def shift_top_puck(self, start, end):
		if start == end or len(self.poles[start]) == 0:
			return 
		if len(self.poles[end]) != 0 and self.poles[start][-1].weight > self.poles[end][-1].weight:
			return 

		# puck = self.poles[start].pop()
		puck = self.poles[start][-1]

		# # procedure to move from start to end
		while puck.y > self.base_coord-self.pole_length:
			puck.move_puck(puck.x, puck.y-puck.speed_y)
			pygame.display.update()
			display(self, self.reset_button, self.solve_button)
		while puck.x != self.poles_xs[end]:
			if start<end:
				puck.move_puck(puck.x+puck.speed_x, puck.y)
			else:
				puck.move_puck(puck.x-puck.speed_x, puck.y)
			pygame.display.update()
			display(self, self.reset_button, self.solve_button)
		while puck.y != self.pucks_ys[ len(self.poles[end]) ]:
			puck.move_puck(puck.x, puck.y+puck.speed_y)
			pygame.display.update()
			display(self, self.reset_button, self.solve_button)

		self.poles[start].pop()
		self.poles[end].append(puck)
		tmp = [puck.weight for puck in self.poles[2]]
		# self.score = max(sum(tmp), self.score)
		self.score += 1


class Puck:
	def __init__(self, weight, x, y, speed_x, speed_y, puck_width, puck_height, active_color, inactive_color, action=None):
		self.weight = weight
		self.x = x # center x
		self.y = y # center y
		self.speed_x = speed_x
		self.speed_y = speed_y
		self.width = puck_width
		self.height = puck_height
		self.action = action
		self.active_color = active_color
		self.inactive_color = inactive_color

	def display_puck(self, game):
		x = self.x-(self.width/2)
		y = self.y-(self.height/2)
		w = self.width
		h = self.height
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x+w>mouse[0]>x and y+h>mouse[1]>y:
			pygame.draw.rect(game.gameDisplay, self.active_color, (x,y,w,h))
			if click[0]==1 and self.action!=None:
				self.action()
		else:
			pygame.draw.rect(game.gameDisplay, self.inactive_color, (x,y,w,h))

	def move_puck(self, new_x, new_y):
		self.x = new_x
		self.y = new_y
		# time.sleep(0.1)


class Button:
	def __init__(self, msg, x, y, w, h, inactive_color, active_color, text_color, action=None):
		self.msg = msg
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.inactive_color = inactive_color
		self.active_color = active_color
		self.text_color = text_color
		self.action = action

	def display_button(self, game):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if self.x+self.w>mouse[0]>self.x and self.y+self.h>mouse[1]>self.y:
			pygame.draw.rect(game.gameDisplay, self.active_color, (self.x, self.y, self.w, self.h))
			if click[0]==1 and self.action!=None:
				self.action()
		else:
			pygame.draw.rect(game.gameDisplay, self.inactive_color, (self.x, self.y, self.w, self.h))

		smalltext = pygame.font.SysFont("comicsansms",20)
		textSurf, textRect = text_objects(self.msg, smalltext, self.text_color)
		textRect.center = (self.x+(self.w/2), self.y+(self.h/2) )
		game.gameDisplay.blit(textSurf, textRect)	


def text_objects(msg, font, text_color):
	textSurf = font.render(msg, True, text_color)
	return textSurf, textSurf.get_rect()


# score and buttons
def display_ui(game, score, reset_button, solve_button):
	myfont = pygame.font.SysFont('Segoe UI', 20, True)
	letters = ["START", "HELPER", "END"]
	for i in range(3):
		text = myfont.render(letters[i], True, black[1])
		game.gameDisplay.blit(text, (game.poles_xs[i], game.base_coord+10))

	# display buttons
	text_score = myfont.render("MOVES : "+str(score), True, black[1])
	game.gameDisplay.blit(text_score, (game.poles_xs[0], (game.game_height*7)/8))
	reset_button.display_button(game)
	solve_button.display_button(game)


# everything on gameDisplay
def display(game, reset_button, solve_button):
	game.gameDisplay.fill(white[1])
	# draw poles
	for i in range(3):
		pygame.draw.rect(game.gameDisplay, gray[1], (game.poles_xs[i]-2.5, game.base_coord-game.pole_length, 5, game.pole_length))

	# draw base_coord
	pygame.draw.rect(game.gameDisplay, gray[1], (0, game.base_coord, game.game_width, 5))	

	# display ui
	display_ui(game, game.score, reset_button, solve_button)

	# draw pucks
	for pole in game.poles:
		for puck in pole:
			puck.display_puck(game)
	
	pygame.display.update()
	pygame.time.wait(delay)


def display_solver(game):
	for step in game.solution:
		game.shift_top_puck(step[0], step[1])
		# time.sleep(0.2)
		pygame.time.wait(delay)


def quitGame():
	pygame.quit()
	quit()


def run():
	pygame.init()
	game = Game(800, 800, 7)
	game.initialise_game()
	start = -1
	end = -1
	# msg, x, y, w, h, inactive_color, active_color, text_color, action=None
	game.reset_button = Button("RESET", game.poles_xs[1]-40, (game.game_height*7)/8-20, 80, 40, peru[1], burly_wood[1], black[1], game.initialise_game )
	game.solve_button = Button("SOLVE", game.poles_xs[2]-40, (game.game_height*7)/8-20, 80, 40, peru[1], burly_wood[1], black[1], game.set_solution )

	while True:
		# v = time.time()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitGame()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT: # 0
					if start == -1:
						start = 0
					elif end == -1:
						end = 0
					else:
						start, end = 0, -1
				elif event.key == pygame.K_RIGHT: # 2
					if start == -1:
						start = 2
					elif end == -1:
						end = 2
					else:
						start, end = 2, -1
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN: # 1
					if start == -1:
						start = 1
					elif end == -1:
						end = 1
					else:
						start, end = 1, -1
		if game.solution != None:
			display_solver(game)
			game.solution = None
		else:
			if start != -1 and end != -1:
				# print(start, end)
				game.shift_top_puck(start, end)
				start, end = -1, -1
			display(game, game.reset_button, game.solve_button)
			# clock.tick(60)
		# last = time.time()
	

run()