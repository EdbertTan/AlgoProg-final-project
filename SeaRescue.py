import pygame

import random
from math import sin, cos, pi, radians
pygame.mixer.init()

class Sprite: #makes a super class for other classes
    def __init__(self, image, game): #makes an image attribute that is used by all sprite classes
        self.image = image
        self.position = [0, 0]
        self.game = game
        self.reset()
    def update(self):
        pass
    def draw(self):
        self.game.surface.blit(self.image, self.position)
    def reset(self):
        pass

    def intersects_with(self, sprite): #function for detecting when a sprite collides with another sprite
        max_x = self.position[0] + self.image.get_width()
        max_y = self.position[1] + self.image.get_height()

        smax_x = sprite.position[0] + sprite.image.get_width()
        smax_y = sprite.position[1] + sprite.image.get_height()
        if max_x < sprite.position[0]:
            return False
        if max_y < sprite.position[1]:
            return False
        if self.position[0] > smax_x:
            return False
        if self.position[1] > smax_y:
            return False
        return True


class Boat(Sprite): #boat sprite for the player character
    def reset(self): #function called to reset to center of the screen after starting/restarting the game
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.position[0] = (self.game.width - self.image.get_width()) / 2
        self.position[1] = (self.game.height - self.image.get_height()) / 2
        self.movement_speed = [5, 5]

    def update(self): #function for sprite movement
        if self.movingUp:
            self.position[1] = self.position[1] - (self.movement_speed[1])
        if self.movingDown:
            self.position[1] = self.position[1] + (self.movement_speed[1])
        if self.movingLeft:
            self.position[0] = self.position[0] - (self.movement_speed[0])
        if self.movingRight:
            self.position[0] = self.position[0] + (self.movement_speed[0])

        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[0] + self.image.get_width() > self.game.width:
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1] + self.image.get_height() > self.game.height:
            self.position[1] = self.game.height - self.image.get_height()

    def StartMoveUp(self): #function for moving the boat up
        self.movingUp = True
    def StopMoveUp(self): #function for stopping the boat from moving up when the up arrow button stops being pressed
        self.movingUp = False
    def StartMoveDown(self): #function for moving the boat down
        self.movingDown = True
    def StopMoveDown(self): #function for stopping the boat from moving down when the down arrow button stops being pressed
        self.movingDown = False
    def StartMoveLeft(self): #function for moving the boat left
        self.movingLeft = True
    def StopMoveLeft(self): #function for stopping the boat from moving left when the left arrow button stops being pressed
        self.movingLeft = False
    def StartMoveRight(self): #function for moving the boat right
        self.movingRight = True
    def StopMoveRight(self): #function for stopping the boat from moving right when the right arrow button stops being pressed
        self.movingRight = False

class People(Sprite): #the sprite of the people the player rescues for points
    def __init__(self, image, game, saving_sound):
        super().__init__(image, game)
        self.saving_sound = saving_sound
    def reset(self): #randomizes location of the sprite, used at the start and every time a point is gotten
        self.position[0] = random.randint(0,
                                          self.game.width - self.image.get_width())
        self.position[1] = random.randint(0,
                                          self.game.height - self.image.get_height())
    def update(self): #calls hitscore when colliding with boat, increasing score by 1 and then making another sprite appear in a random location on the screen
        if self.intersects_with(game.Boat_sprite):
            ohit.hitscore()

            self.saving_sound.play()
            self.reset()

class Shark(Sprite): #the sprite for the sharks that causes a game over

    def __init__(self, image, game, entry_delay): #puts a delay between each shark that appears
        super().__init__(image, game)
        self.entry_delay = entry_delay
    def update(self): #makes the shark move to the location of the boat at all times

        self.entry_count = self.entry_count + 1
        if self.entry_count < self.entry_delay:
            return

        if game.Boat_sprite.position[0] > self.position[0]:
            self.x_speed = self.x_speed + self.x_accel
        else:
            self.x_speed = self.x_speed - self.x_accel
        self.x_speed = self.x_speed * self.friction_value
        self.position[0] = self.position[0] + self.x_speed

        if game.Boat_sprite.position[1] > self.position[1]:
            self.y_speed = self.y_speed + self.y_accel
        else:
            self.y_speed = self.y_speed - self.y_accel
        self.y_speed = self.y_speed * self.friction_value
        self.position[1] = self.position[1] + self.y_speed

        if self.intersects_with(game.Boat_sprite): #stops music and loads the game over screen when colliding
            pygame.mixer.music.stop()
            pygame.display.quit()

            ocoverend.choices()

    def reset(self): #resets amount of sharks to 0 and sets their speed and acceleration
        self.entry_count = 0
        self.friction_value = 0.99
        self.x_accel = 0.05
        self.y_accel = 0.05
        self.x_speed = 0
        self.y_speed = 0
        self.position = [-100, -100]

class jellyfish1(Sprite): #sprite for the first jellyfish


    def __init__(self, image, game):
        super().__init__(image, game)



    def reset(self): #sets the position of the jellyfish when the game loads or reloads
        self.center_of_rotation_x = 600
        self.center_of_rotation_y = 300
        self.radius = 50
        self.angle = radians(45)
        self.omega = 0.05
        self.b=0
        self.c=5

        self.position[0] = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.position[1] = self.center_of_rotation_y - self.radius * sin(self.angle)

    def update(self): #spins in a circle that increases radius until 205 where the radius decreases until 45 and incrases again
        self.b=self.b+1
        if self.b%50==0:
            self.radius=self.radius+self.c
        if self.radius==205:
            self.c=-5
        elif self.radius==45:
            self.c=5
        self.angle = self.angle + self.omega
        self.position[0] = self.position[0] + self.radius * self.omega * cos(self.angle + pi / 2)
        self.position[1] = self.position[1] - self.radius * self.omega * sin(self.angle + pi / 2)

        if self.intersects_with(game.Boat_sprite): #stops music and loads the game over screen when colliding
            pygame.mixer.music.stop()
            pygame.display.quit()

            ocoverend.choices()


class jellyfish2(Sprite): #sprite for the second jellyfish

    def __init__(self, image, game):
        super().__init__(image, game)


    def reset(self): #sets the position of the jellyfish when the game loads or reloads
        self.center_of_rotation_x = 200
        self.center_of_rotation_y = 300
        self.radius = 50
        self.angle = radians(225)
        self.omega = 0.05
        self.b=0
        self.c=5

        self.position[0] = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.position[1] = self.center_of_rotation_y - self.radius * sin(self.angle)

    def update(self): #spins in a circle that increases radius until 205 where the radius decreases until 45 and incrases again
        self.b=self.b+1
        if self.b%50==0:
            self.radius=self.radius+self.c
        if self.radius==205:
            self.c=-5
        elif self.radius==45:
            self.c=5
        self.angle = self.angle + self.omega
        self.position[0] = self.position[0] + self.radius * self.omega * cos(self.angle + pi / 2)
        self.position[1] = self.position[1] - self.radius * self.omega * sin(self.angle + pi / 2)

        if self.intersects_with(game.Boat_sprite): #stops music and loads the game over screen when colliding
            pygame.mixer.music.stop()
            pygame.display.quit()

            ocoverend.choices()


class Sharkfin1(Sprite):  # sprite for the first shark fin

    def __init__(self, image, game):
        super().__init__(image, game)


    def reset(self): #sets the position to the left side of the screen
        self.x = 0
        self.position=[self.x,100]

    def update(self): #makes the shark fin move from left to right and resets when it hits the right side of the screen
        self.x=self.x+2
        if self.x==800:
            self.x=0
        self.position=[self.x,100]

        if self.intersects_with(game.Boat_sprite): #stops music and loads the game over screen when colliding
            pygame.mixer.music.stop()
            pygame.display.quit()

            ocoverend.choices()

class Sharkfin2(Sprite):  # sprite for the second shark fin

    def __init__(self, image, game):
        super().__init__(image, game)

    def reset(self): #sets the position to the left side of the screen
        self.x = 0
        self.position=[self.x,500]

    def update(self): #makes the shark fin move from left to right and resets when it hits the right side of the screen
        self.x=self.x+2
        if self.x==800:
            self.x=0
        self.position=[self.x,500]

        if self.intersects_with(game.Boat_sprite): #stops music and loads the game over screen when colliding
            pygame.mixer.music.stop()
            pygame.display.quit()

            ocoverend.choices()



class Hit: #class for the score collected
    def __init__(self, score):
        self.score = score

    def clearscore(self): #resets score when used
        self.score = 0

    def hitscore(self): #adds score by 1 for every time function is used
        self.score = self.score + 1


class Cover: #class for the start and game over screens
    def __init__(self, type):
        self.type = type

    def choices(self): #displays either the start screen or the game over screen depending on the type

        init_result = pygame.init()
        if init_result[1] != 0:
            print('pygame not installed properly')
            return

        self.width = 800
        self.height = 600
        self.size = (self.width, self.height)

        self.sprites = []

        self.surface = pygame.display.set_mode(self.size)

        pygame.display.set_caption('Sea Rescue')

        white = (55, 55, 55)

        font = pygame.font.SysFont("Arial", 24)

        if self.type == 1: #displays the "go and rescue" button if type is 1
            text1 = font.render(" GO AND RESCUE ", True, white)
        else: #displays the "start again" button in the same place if type is 2
            text1 = font.render(" START AGAIN", True, white)

        text3 = font.render(" QUIT ", True, white)

        rect1 = text1.get_rect(topleft=(500, 480))
        rect3 = text3.get_rect(topleft=(700, 480))

        bg = (127, 127, 127)
        msg = " "
        screen = pygame.display.set_mode((800, 600))

        if self.type == 1: #displays the starting screen if type is 1
            ship = pygame.image.load("frontscreen.png", "frontscreen.png")
        else: #displays the game over screen if type is 2
            ship = pygame.image.load("gameoverscreen.png", "gameoverscreen.png")

        screen.blit(ship, (0, 0))

        if self.type == 2: #displays the end score on the game over screen if type is 2
            msg = "TOTAL LIVES SAVED : " + str(ohit.score)

            img = font.render(msg, True, (0, 0, 255))
            imgrect = img.get_rect()
            imgrect.center = (200, 150)
            pygame.draw.rect(screen, bg, imgrect)
            screen.blit(img, imgrect)

        done = False

        while not done:


            for event in pygame.event.get():
                screen.blit(text1, rect1)
                screen.blit(text3, rect3)

                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect1.collidepoint(event.pos):


                        ohit.clearscore()

                        game.play_game()

                    if rect3.collidepoint(event.pos):
                        done = True

            if done == True:
                pygame.display.quit()
                pygame.quit()

            else:
                pygame.display.flip()



class SeaRescue:
    #starts the game
    def play_game(self):
        init_result = pygame.init()
        if init_result[1] != 0:
            print('pygame not installed properly')
            return

        self.width = 800
        self.height = 600
        self.size = (self.width, self.height)

        self.sprites = []

        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption('People Rescuing')

        background_image = pygame.image.load('background.png') #sets background image
        self.background_sprite = Sprite(image=background_image,
                                        game=self)

        self.sprites.append(self.background_sprite)

        pygame.mixer.music.load("mermaid.wav") #sets background music
        pygame.mixer.music.play(-1)

        People_image = pygame.image.load('People.png') #sets image for the people sprite
        People_save_sound = pygame.mixer.Sound('yay.wav') #plays a yay sound effect whenever a point is gotten

        for i in range(20): #limits the amount of people sprites on screen to be 20
            People_sprite = People(image=People_image,
                                   game=self, saving_sound=People_save_sound)
            self.sprites.append(People_sprite)

        Boat_image = pygame.image.load('Boat.png') #sets image for the boat sprite
        self.Boat_sprite = Boat(image=Boat_image,
                                game=self)

        self.sprites.append(self.Boat_sprite)

        Shark_image = pygame.image.load('Shark.png') #sets image for the shark sprite
        sharkfin_image = pygame.image.load('sharkfin.png') #sets image for the shark fin sprite
        jellyfish_image = pygame.image.load('jellyfish.png') #sets image for the jellyfish sprite

        for entry_delay in range(0, 3000, 300):
            Shark_sprite = Shark(image=Shark_image,
                                 game=self
                                 , entry_delay=entry_delay)
            self.sprites.append(Shark_sprite)

        jellyfish_1 = jellyfish1(image=jellyfish_image,
                                    game=self)
        self.sprites.append(jellyfish_1)

        jellyfish_2 = jellyfish2(image=jellyfish_image,
                                 game=self)
        self.sprites.append(jellyfish_2)

        Sharkfin_1 = Sharkfin1(image=sharkfin_image,
                                   game=self)
        self.sprites.append(Sharkfin_1)

        Sharkfin_2 = Sharkfin2(image=sharkfin_image,
                               game=self)
        self.sprites.append(Sharkfin_2)

        clock = pygame.time.Clock()

        game_state = "start_menu"

        while True:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

                    elif e.key == pygame.K_UP:
                        self.Boat_sprite.StartMoveUp()
                    elif e.key == pygame.K_DOWN:
                        self.Boat_sprite.StartMoveDown()
                    elif e.key == pygame.K_LEFT:
                        self.Boat_sprite.StartMoveLeft()
                    elif e.key == pygame.K_RIGHT:
                        self.Boat_sprite.StartMoveRight()
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_UP:
                        self.Boat_sprite.StopMoveUp()
                    if e.key == pygame.K_DOWN:
                        self.Boat_sprite.StopMoveDown()
                    if e.key == pygame.K_LEFT:
                        self.Boat_sprite.StopMoveLeft()
                    if e.key == pygame.K_RIGHT:
                        self.Boat_sprite.StopMoveRight()

            for sprite in self.sprites:
                sprite.update()

            for sprite in self.sprites:
                sprite.draw()

            pygame.display.flip()

#actual program starts from here==============================================

ohit = Hit(0) #sets starting score to 0

game = SeaRescue()

ocoverstart = Cover(1)

ocoverend = Cover(2)

ocoverstart.choices()
