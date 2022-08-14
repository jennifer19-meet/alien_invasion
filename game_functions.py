import pygame
from pygame.sprite import Group
import sys
from game_classes import *

def get_num_aliens_x(settings, random_alien):
	available_space_x = settings.width - (2 * random_alien.rect.width)
	max_number_aliens_x = int(available_space_x / (2 * random_alien.rect.width))
	return max_number_aliens_x

def get_num_aliens_y(settings, ship, random_alien):
	available_space_y = settings.height - (3 * random_alien.rect.height + ship.rect.height)
	max_number_aliens_y = int(available_space_y / (2 * random_alien.rect.width))
	return max_number_aliens_y

def create_and_append_alien(aliens, settings, i, row):
	new_alien = Alien(settings)
	new_alien.x += (2 * i * new_alien.rect.width)
	new_alien.rect.x = new_alien.x
	new_alien.rect.y += (row * 2 * new_alien.rect.height)
	aliens.add(new_alien)

def create_fleet(settings, aliens, ship):
	random_alien = Alien(settings)
	max_aliens_x = get_num_aliens_x(settings, random_alien)
	max_aliens_y = get_num_aliens_y(settings, ship, random_alien) 
	for row in range(max_aliens_y):
		for i in range(max_aliens_x):
			create_and_append_alien(aliens,settings, i, row)

def firing_bullet(bullets, settings, ship):
	if len(bullets)< settings.max_bullets:
		new_bullet = Bullet(settings, ship)
		bullets.add(new_bullet)

def keydown_events(event,settings, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		firing_bullet(bullets, settings, ship)
	elif event.key == pygame.K_q:
		sys.exit()

def check_events(settings, ship, bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			keydown_events(event,settings, ship, bullets)
			
		elif event.type == pygame.KEYUP:
			ship.moving_right = False
			ship.moving_left = False

def update_screen(settings1, ship1, bullets, aliens):
	settings1.screen.fill(settings1.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship1.blitme()
	
	aliens.draw(settings1.screen)
	pygame.display.flip()

def update_bullets(bullets):
	bullets.update()
	# Removing the bullet after it goes out of the screen
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def move_aliens(aliens, settings):
	aliens.update(settings)

def game_setup():
	'''Setting up the screen settings and allows pygame to respond to the keyboard and mouse'''
	game_settings = Settings()
	pygame.display.set_caption("Alien Invasion")

	ship = Ship(game_settings)

	# A group to store the bullets in
	bullets = Group()
	aliens = Group()

	create_fleet(game_settings, aliens, ship)
	create_fleet(game_settings, aliens, ship)

	while True:
		check_events(game_settings, ship, bullets)
		ship.update()
		update_bullets(bullets)
		move_aliens(aliens, game_settings)
		update_screen(game_settings, ship, bullets, aliens)



