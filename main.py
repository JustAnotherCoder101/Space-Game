import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
#Sprites


class Ship(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.Oimage = pygame.image.load("sprites/ship.png")
    self.image = pygame.transform.scale(self.Oimage, (50, 50))
    self.rect = self.image.get_rect()
    self.rect.x = 50
    self.rect.y = 200

  def tick(self, INV):
    if INV > 1:
      self.image = pygame.transform.scale(self.Oimage, (50, 50))
      self.image.set_alpha(100)
    else:
      self.image = pygame.transform.scale(self.Oimage, (50, 50))
      self.image.set_alpha(255)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
      self.rect.y -= 5

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      self.rect.y += 5

    if self.rect.y < 0:
      self.rect.y = 0
    if self.rect.y > height - self.rect.height:
      self.rect.y = height - self.rect.height


class Asteroid(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.Oimage = pygame.image.load("sprites/asteroid.png")
    self.Oimage = pygame.transform.rotate(self.Oimage, 180)
    self.image = pygame.transform.scale(self.Oimage, (85, 45))
    self.rect = self.image.get_rect()
    self.x = width
    self.y = random.randint(0, height - self.rect.height)
    self.rect.x = self.x
    self.rect.y = self.y
    self.speed = 4
    self.Health = 80
    self.max_health = 80
    self.Bar_Length = 50

  def update(self):
    self.x -= self.speed
    self.rect.x = self.x + random.randint(-2, 2)
    self.rect.y = self.y + random.randint(-2, 2)
    if self.rect.x < -self.rect.width:
      self.kill()
    if self.Health < self.max_health:
      self.draw_health()
      
  def damage(self):
    self.Health -= 20
    if self.Health < 1:
      self.kill()

  def draw_health(self):
    health = (self.Health / self.max_health) * self.Bar_Length

    pygame.draw.rect(
        screen, (0, 0, 0),
        (self.rect.x - 5, self.rect.y - 15, self.Bar_Length + 10, 15))
    pygame.draw.rect(screen, (255, 0, 0),
                     (self.rect.x, self.rect.y - 10, self.Bar_Length, 5))
    pygame.draw.rect(screen, (0, 255, 0),
                     (self.rect.x, self.rect.y - 10, health, 5))

    
    


class Bullet(pygame.sprite.Sprite):

  def __init__(self, x, y,Images):
    super().__init__()
    self.Oimage = pygame.image.load("sprites/bullet.png")
    self.image = pygame.transform.scale(self.Oimage, (30, 10))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.speed = 10
    self.active = True
    self.AStage = -1
    self.ATimer = 0
    self.Images = Images

  def update(self):
    if self.active:
      #self.speed += 1
      self.rect.x += self.speed
      if self.rect.x > width:
        self.kill()
    else: 
      self.ATimer += 1
      if self.ATimer > 2:
        self.AStage += 1
        self.ATimer = 0
        
      if self.AStage > 6:
        self.kill()
        
      else: 
        self.Oimage = self.Images[self.AStage]
        self.image = self.Oimage    
        
      

  def collide(self):
    self.active = False  
  

def Get_HEALTH(Health):
  Full = pygame.image.load("sprites/Heart/Full.png")
  Full = pygame.transform.scale(Full, (20, 20))
  Half = pygame.image.load("sprites/Heart/Half.png")
  Half = pygame.transform.scale(Half, (20, 20))
  Empty = pygame.image.load("sprites/Heart/Empty.png")
  Empty = pygame.transform.scale(Empty, (20, 20))
  list = []

  if Health > 0:
    if Health > 1:
      list.append(Full)
      if Health > 3:
        list.append(Full)
        if Health > 5:
          list.append(Full)
        elif Health == 5:
          list.append(Half)
      elif Health == 3:
        list.append(Half)
    elif Health == 1:
      list.append(Half)

  else:
    list = [Empty, Empty, Empty]

  length = len(list)
  if length == 1:
    list.append(Empty)
    list.append(Empty)
  elif length == 2:
    list.append(Empty)

  return list


# Load the images
BACKGROUND = pygame.image.load("sprites/BACKGROUND.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))

Bullet_Images = []
for i in range(1,8):
  Bullet_Images.append(pygame.image.load(f"sprites/Animations/Bullet/{str(i)}.png"))
print(len(Bullet_Images))  

# Set screen title
SHIP = Ship()
Asteroids = pygame.sprite.Group()
Player = pygame.sprite.Group()

Bullets = pygame.sprite.Group()
Player.add(SHIP)
pygame.display.set_caption("My Pygame screen")

#variables
Health = 6
INV = 0
running = True
Timer = 100
spacePressed = False
Start = False
cooldown = 0
# Create a clock object to control the frame rate
FPS = 60
Shake = 0
clock = pygame.time.Clock()

# Loop
print("Done")

while running:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  
  if Start:
    if Timer <= 0:
      Asteroids.add(Asteroid())

      Timer = 100
    Timer -= 1

  if Shake > 0:
    Shake -= 1

  if INV >= 0:
    INV -= 1
  if Health <= 0:
    running = False

  # game things

  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    if cooldown <= 0:
      Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y + 40,Bullet_Images))
      Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y,Bullet_Images))
      cooldown = 15
  
  cooldown -= 1
  if keys[pygame.K_1]:
    Start = True

  # game things

  # make the background

  screen.blit(BACKGROUND, (0, 0))
  SHIP.tick(INV)
  Player.update()
  Asteroids.update()
  Bullets.update()

  for i in Player:
    if pygame.sprite.spritecollideany(i, Asteroids) and INV < 1:
      Shake = 10
      Health -= 1
      INV = 40

  for i in Asteroids:
    for j in Bullets:
      if pygame.sprite.collide_rect(i, j):
        if j.active:
          i.damage()
          j.collide()
        else:
          pass
  for i in Bullets:
    if pygame.sprite.spritecollideany(i, Asteroids):
      i.active = False
      
  
  Player.draw(screen)
  Asteroids.draw(screen)
  Bullets.draw(screen)

  x = 30
  for i in Get_HEALTH(Health):
    screen.blit(i, (x + random.randint(0 - Shake, Shake),
                    20 + random.randint(0 - Shake, Shake)))
    x += 30

  # Update the display
  pygame.display.flip()
  clock.tick(FPS)
# Quit Pygame
pygame.quit()
