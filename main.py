import pygame
import math
import random
import sys
import asyncio


async def main():
    pygame.init()
    WIDTH = 1000
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    title = pygame.Surface((WIDTH, HEIGHT))
    pygame.display.set_caption("Cheese Chase")
    font = pygame.font.SysFont(None, 150)
    title_name = font.render('Cheese Chase', True, (0, 0, 0))
    lose = font.render('You lost', True, (0, 0, 0))
    win = font.render('You win', True, (0, 0, 0))
    clock = pygame.time.Clock()

    # background
    bg_image = pygame.image.load("background.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (1000, 800))
    b1 = pygame.image.load("b1.png").convert_alpha()
    b1 = pygame.transform.scale(b1, (1000, 800))

    # player
    player_image = pygame.image.load("player.png").convert_alpha()
    player_image = pygame.transform.scale(
        player_image,
        (100, 100)
    )
    player_image_right = player_image
    player_image_left = pygame.transform.flip(player_image, True, False)
    player_rect = pygame.Rect(380, 100, 40, 45)
    player_vel_x = 0
    player_vel_y = 0
    player_speed = 6
    GRAVITY = 0.8
    JUMP_STRENGTH = -15
    is_grounded = False

    # buttons
    exit = pygame.image.load("exit.png").convert_alpha()
    exit = pygame.transform.scale(
        exit,
        (50, 50)
    )
    start = pygame.image.load("start.png").convert_alpha()
    start = pygame.transform.scale(
        start,
        (50, 50)
    )

    class Button:
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            new_size = int(width * scale * 2), int(height * scale)
            self.image = pygame.transform.scale(image, new_size)
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self):
            title.blit(self.image, (self.rect.x, self.rect.y))

        def click(self):
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    return True

    class Enemy:
        def __init__(self, x, y):
            self.image = pygame.image.load("enemy.png").convert_alpha()
            self.image = pygame.transform.scale(
                self.image,
                (100, 100)
            )
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.collider = pygame.Rect(
                self.rect.x + 20,
                self.rect.y + 20,
                60,
                60
            )
            self.speed = 1.5

        def chase_player(self, player):
            distance = math.sqrt(
                (self.rect.x - player.x) ** 2 +
                (self.rect.y - player.y) ** 2
            )

            if distance < 200:
                if self.rect.x < player.x:
                    self.rect.x += abs(self.speed) * 2
                elif self.rect.x > player.x:
                    self.rect.x -= abs(self.speed) * 2
            else:
                self.rect.x += self.speed

            if self.rect.left < 0:
                self.rect.left = 0
                self.speed = 1.5

            if self.rect.right > 1000:
                self.rect.right = 1000
                self.speed = -1.5

            self.collider.topleft = (
                self.rect.x + 20,
                self.rect.y + 20
            )

        def draw(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))

    # target
    cheese = pygame.image.load("cheese.png").convert_alpha()
    cheese = pygame.transform.scale(
        cheese,
        (50, 50)
    )

    class Cheese:
        def __init__(self, x, y):
            self.image = cheese
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.collider = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        def draw(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))

        def eat(self, player):
            return self.rect.colliderect(player)

    platforms = [
        pygame.Rect(0, 725, 1000, 50),
        pygame.Rect(100, 575, 250, 20),
        pygame.Rect(450, 475, 250, 20),
        pygame.Rect(850, 375, 100, 20),
        pygame.Rect(850, 175, 100, 20),
        pygame.Rect(450, 150, 100, 20),
        pygame.Rect(450, 250, 220, 20),
        pygame.Rect(100, 175, 175, 20),
        pygame.Rect(100, 375, 100, 20),
    ]

    button1 = Button(350, 375, start, 3)
    button2 = Button(350, 550, exit, 3)
    che = []

    for i in range(20):
        while True:
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, HEIGHT - 50)
            cheese_rect = pygame.Rect(x, y, 50, 50)
            can_spawn = True
            for platform in platforms:
                if cheese_rect.colliderect(platform):
                    can_spawn = False
            if can_spawn:
                break

        c = Cheese(x, y)
        che.append(c)

    enemy = Enemy(500, 750)
    running = True
    page = False
    condition = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(title, (0, 0))
        if page == False:
            title.blit(bg_image, (0, 0))
            title.blit(title_name, (155, 175))
            button1.draw()
            button2.draw()
            screen.blit(title, (0, 0))

            if button2.click():
                running = False
                page = True
            if button1.click():
                page = True
        else:
            screen.blit(b1, (0, 0))

            enemy.chase_player(player_rect)

            if enemy.collider.colliderect(player_rect) and condition:
                screen.fill((255, 255, 255))
                screen.blit(bg_image, (0, 0))
                screen.blit(lose, (275, 175))
                screen.blit(button2.image, (button2.rect.x, button2.rect.y))
                pygame.display.flip()
                if button2.click():
                    running = False
                clock.tick(60)
                await asyncio.sleep(0)
                continue
            enemy.draw()

            keys = pygame.key.get_pressed()
            player_vel_x = 0

            if keys[pygame.K_a]:
                player_image = player_image_left
                player_vel_x = -player_speed
            if keys[pygame.K_d]:
                player_image = player_image_right
                player_vel_x = player_speed
            if keys[pygame.K_w] and is_grounded:
                player_vel_y = JUMP_STRENGTH
                is_grounded = False

            # Apply Gravity
            player_vel_y += GRAVITY

            # Move Horizontally & Handle Screen Boundaries
            player_rect.x += player_vel_x
            if player_rect.left < 0:
                player_rect.left = 0
            if player_rect.right > WIDTH:
                player_rect.right = WIDTH

            # Move Vertically & Handle Safe Platform Collisions
            player_rect.y += player_vel_y
            is_grounded = False

            for platform in platforms:
                if player_rect.colliderect(platform):
                    if player_vel_y > 0:
                        player_rect.bottom = platform.top
                        player_vel_y = 0
                        is_grounded = True
                    elif player_vel_y < 0:
                        player_rect.top = platform.bottom
                        player_vel_y = 0

            # Fall-back safety screen floor boundary check
            if player_rect.bottom > 725:
                player_rect.bottom = 725
                player_vel_y = 0
                is_grounded = True

            if enemy.rect.bottom > 750:
                enemy.rect.bottom = 750

            for c in che[:]:
                if c.eat(player_rect):
                    che.remove(c)
                else:
                    c.draw()

            screen.blit(player_image, (player_rect.x - 20, player_rect.y - 20))
            for platform in platforms:
                pygame.draw.rect(screen, (0, 0, 139), platform)

            if len(che) == 0:
                screen.fill((255, 255, 255))
                screen.blit(bg_image, (0, 0))
                screen.blit(win, (275, 175))
                screen.blit(button2.image, (button2.rect.x, button2.rect.y))
                pygame.display.flip()
                if button2.click():
                    running = False
                clock.tick(60)
                await asyncio.sleep(0)
                condition = False
                continue

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()



asyncio.run(main())

