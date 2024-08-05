import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
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

  def tick(self,INV):
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
    self.image = pygame.transform.scale(self.Oimage, (75, 40))
    self.rect = self.image.get_rect()
    self.x = width
    self.y = random.randint(0, height - self.rect.height)
    self.rect.x  = self.x
    self.rect.y = self.y
    self.speed = 4
    

  def update(self):
    self.x -= self.speed
    self.rect.x  = self.x + random.randint(-2,2)
    self.rect.y = self.y + random.randint(-2,2)
    if self.rect.x < -self.rect.width:
      self.kill()
    


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


# Set window title
SHIP = Ship()
Asteroids = pygame.sprite.Group()
Player = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.Oimage = pygame.image.load("sprites/bullet.png")
    self.image = pygame.transform.scale(self.Oimage, (40, 40))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.speed = 10
    
  def update(self):
    self.rect.x += self.speed
    if self.rect.x > width:
      self.kill()


Bullets = pygame.sprite.Group()
Player.add(SHIP)
pygame.display.set_caption("My Pygame Window")

#variables
Health = 6
INV = 0
running = True
Timer = 100
spacePressed = False
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
    if not spacePressed:
      Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y + 25))
      spacePressed = True
  else:
    spacePressed = False
  
  # game things

    

  
  # make the background
  
  screen.blit(BACKGROUND, (0, 0))
  SHIP.tick(INV)
  Player.update()
  Asteroids.update()
  Bullets.update()
  
  for i in Player:
    if pygame.sprite.spritecollideany(i, Asteroids) and INV <1:
      Shake = 10
      Health -= 1
      INV = 40

  x = 30
  for i in Get_HEALTH(Health):
    screen.blit(i,(x+random.randint(0-Shake,Shake),20+random.randint(0-Shake,Shake)))
    x += 30
    
  Player.draw(screen)
  Asteroids.draw(screen)
  Bullets.draw(screen)
  


  
  # Update the display
  pygame.display.flip()
  clock.tick(FPS)
# Quit Pygame
pygame.quit()