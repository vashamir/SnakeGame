import pygame
import sys
import random

is_retry = False

head_images = [pygame.image.load('head_top.png'), pygame.image.load(
    'head_bot.png'), pygame.image.load('head_right.png'), pygame.image.load('head_left.png')]


class Game():

    def __init__(self):
        self.screen_width = 725
        self.screen_height = 450

        self.red = pygame.Color("Red")
        self.green = pygame.Color("Green")
        self.black = pygame.Color("Black")
        self.white = pygame.Color("White")
        self.brown = pygame.Color("Brown")

        self.fps_controller = pygame.time.Clock()

        self.score = 0

    def check_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def window(self):
        self.play_surface = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

    def snake_direction(self, change_to):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        game.fps_controller.tick(14)

    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('arial', 24)
        s_surf = s_font.render('Score: {0}'.format(
            self.score), True, self.black)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        is_retry = True
        go_font = pygame.font.SysFont('arial', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        go_font_r = pygame.font.SysFont('arial', 30)
        go_surf_r = go_font_r.render(
            'press R for restarting', True, self.black)
        go_rect_r = go_surf_r.get_rect()
        go_rect_r.midtop = (350, 170)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        self.play_surface.blit(go_surf_r, go_rect_r)
        pygame.display.flip()
        while is_retry:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        is_retry = False

        game = Game()
        snake = Snake(game.green)
        food = Food(game.brown, game.screen_width, game.screen_height)

        game.check_errors()
        game.window()

        while True:
            snake.change_to = game.snake_direction(snake.change_to)

            snake.change_direction()
            snake.change_head_position()
            game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                                   game.screen_height)
            snake.draw_snake(game.play_surface, game.white)

            food.draw_food(game.play_surface)

            snake.check_for_collapse(
                game.game_over, game.screen_width, game.screen_height)

            game.show_score()
            game.refresh_screen()


class Snake():

    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.head_image = head_images[2]
        self.change_to = self.direction

    def change_direction(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.head_image = head_images[2]
            self.snake_head_pos[0] += 25
        elif self.direction == "LEFT":
            self.head_image = head_images[3]
            self.snake_head_pos[0] -= 25
        elif self.direction == "UP":
            self.head_image = head_images[0]
            self.snake_head_pos[1] -= 25
        elif self.direction == "DOWN":
            self.head_image = head_images[1]
            self.snake_head_pos[1] += 25

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width // 25) * 25,
                        random.randrange(1, screen_height // 25) * 25]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        self.head = True
        play_surface.blit(pygame.image.load('bg.jpg'), (0, 0))
        for pos in self.snake_body:
            if self.head:
                play_surface.blit(self.head_image, (pos[0], pos[1]))
                self.head = False
            else:
                play_surface.blit(pygame.image.load('body.png'), (pos[0], pos[1]))

    def check_for_collapse(self, game_over, screen_width, screen_height):
        if any((self.snake_head_pos[0] > screen_width - 10 or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10 or self.snake_head_pos[1] < 0)):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):
                game_over()


class Food():

    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 25
        self.food_size_y = 25
        self.food_pos = [random.randrange(
            1, screen_width // 25) * 25, random.randrange(1, screen_height // 25) * 25]

    def draw_food(self, play_surface):
        game.play_surface.blit(pygame.image.load('apple.png'), (self.food_pos[0], self.food_pos[1]))


game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)

game.check_errors()
game.window()

while True:
    snake.change_to = game.snake_direction(snake.change_to)

    snake.change_direction()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                           game.screen_height)
    snake.draw_snake(game.play_surface, game.white)

    food.draw_food(game.play_surface)

    snake.check_for_collapse(
        game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.refresh_screen()
