import pygame
from pygame.sprite import Sprite

class Settings(object):
	def __init__(self):
		pygame.init()
		self.width = 1200
		self.height = 800
		self.sound = True
		self.bg_color = (230,250,230)
		self.screen = pygame.display.set_mode((self.width,self.height))
		
		self.ship_speed_factor = 1.5

		self.bullet_speed_factor = 2
		self.bullet_height = 15
		self.bullet_width = 3
		self.bullet_color = "Pink"
		self.max_bullets = 6

		self.alien_speed_factor = 2
		# self.alien_

	def change_height(self,new_height):
		self.height = new_height
		self.screen = pygame.display.set_mode((self.width,self.height))

	def change_width(self, new_width):
		self.width = new_width
		self.screen = pygame.display.set_mode((self.width,self.height))

	def change_sound(self, new_sound):
		self.sound = new_sound

	def change_bg_color(self, new_bg_color):
		self.bg_color = new_bg_color

class Ship(object):
	def __init__(self,settings):
		"""initialize the ship and set its starting position"""
		self.settings = settings
		self.screen = settings.screen
		self.moving_right = False
		self.moving_left = False
		self.shooting = False

		#Load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = settings.screen.get_rect()

		# Start each new ship at the bottom center of the screen
		self.rect.centerx = float(self.screen_rect.centerx)
		self.rect.bottom = self.screen_rect.bottom

	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.rect.centerx += self.settings.ship_speed_factor
		elif self.moving_left and self.rect.left > 0:
			self.rect.centerx -= self.settings.ship_speed_factor

	def blitme(self):
		'''Draw the ship at its current location'''
		self.screen.blit(self.image, self.rect)

class Bullet(Sprite):
	def __init__(self, settings, ship):
		'''Create a bullet object at the ships current position'''
		super().__init__()
		self.screen = settings.screen

		# Create a Rect object at (0, 0) and then set correct position
		self.rect = pygame.Rect(0,0, settings.bullet_width, settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		# Store the bullet's postition as a deciimal value
		self.y = float(self.rect.y)

		# Set the default settings for the bullet 
		self.color = settings.bullet_color
		self.speed_factor = settings.bullet_speed_factor

	def update(self):
		"""Move the bullet up the screen"""
		# Update the decimal position of the bullet
		self.y -= self.speed_factor
		# Update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)

class Alien(Sprite):
	def __init__(self, settings):
		super().__init__()
		self.screen = settings.screen
		self.settings = settings

		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)

		self.speed_factor = settings.alien_speed_factor
		self.moving_right = True

	def update(self, settings):
		if self.rect.right +self.speed_factor <= settings.width and self.moving_right ==True:
			self.moving_right = True
		elif self.rect.right +self.speed_factor > settings.width and self.moving_right ==True:
			self.moving_right = False
		elif self.rect.left - self.speed_factor >= 0 and self.moving_right ==False:
			self.moving_right = False
		elif self.rect.left - self.speed_factor < 0 and self.moving_right ==False:
			self.moving_right = True

		if self.moving_right == True:
			self.x += self.speed_factor
			self.rect.x = self.x
		else:
			self.x -= self.speed_factor
			self.rect.x = self.x

	def blitme(self):
		self.screen.blit(self.image, self.rect)

