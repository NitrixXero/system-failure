# Copyright 2023 Elijah Gordon (NitrixXero) <nitrixxero@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pygame
import sys
import argparse

pygame.init()

parser = argparse.ArgumentParser(description='Matrix-like text display with customizable color.')
parser.add_argument('-c', '--color', default='green', help='Color of the text (default: green)')
parser.add_argument('-a', '--ascii', action='store_true', help='Display ASCII art')
parser.add_argument('-l', '--list-colors', action='store_true', help='List available colors')
parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0', help='Display version information')

args = parser.parse_args()

if args.list_colors:
    print('-----------------')
    print('Available colors:')
    print('-----------------')
    print('green')
    print('red')
    print('yellow')
    print('blue')
    print('magenta')
    print('cyan')
    print('white')
    sys.exit()

if args.ascii:
    ascii_art = '''
              (`.         ,-,
               `\ `.    ,;' /
                \`. \ ,'/ .'
          __     `.\ Y /.'
       .-'  ''--.._` ` (
     .'            /   `
    ,           ` '   Q '
    ,         ,   `._    \\
    |         '     `-.;_'
    `  ;    `  ` --,.._;
    `    ,   )   .'
     `._ ,  '   /_
        ; ,''-,;' ``-
         ``-..__\``--`       Follow the white rabbit.
    '''
    print(ascii_art)
    sys.exit()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption('Wake up, Neo...')

icon = pygame.image.load('icon/icon.jpg')
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)

texts = ['Wake up, Neo...', 'The Matrix has you...', 'Follow the white rabbit.', 'Knock, knock, Neo.']
typing_speed = 6
typing_delay = 1 / typing_speed
current_time = pygame.time.get_ticks()
index = 0
sub_index = 0
typed_text = ""

colors = {
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'magenta': (255, 0, 255),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255)
}

color = colors.get(args.color.lower(), (0, 255, 0))

running = True
typing_finished = False
system_failure_visible = False
system_failure_timer = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not typing_finished:
        if index < len(texts):
            text = texts[index]
            if sub_index < len(text) and pygame.time.get_ticks() - current_time > typing_delay * 1000:
                typed_text += text[sub_index]
                sub_index += 1
                current_time = pygame.time.get_ticks()
            elif sub_index == len(text):
                pygame.time.wait(1000)
                typed_text = ""
                sub_index = 0
                index += 1
                if index == len(texts):
                    typing_finished = True

    screen.fill((0, 0, 0))

    text_surface = font.render(typed_text, True, color)
    text_rect = text_surface.get_rect(topleft=(20, 20))
    screen.blit(text_surface, text_rect)

    if typing_finished:
        if pygame.time.get_ticks() - system_failure_timer > 500:
            system_failure_visible = not system_failure_visible
            system_failure_timer = pygame.time.get_ticks()

        if system_failure_visible:
            system_failure_surface = font.render('SYSTEM FAILURE', True, color)
            system_failure_rect = system_failure_surface.get_rect(center=(screen_width // 2, screen_height // 2))

            border_thickness = 2
            pygame.draw.rect(screen, color, (system_failure_rect.x - border_thickness, system_failure_rect.y - border_thickness, system_failure_rect.width + 2 * border_thickness, system_failure_rect.height + 2 * border_thickness), border_thickness)
            screen.blit(system_failure_surface, system_failure_rect)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
