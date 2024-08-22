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

  def __init__(self,type):
    super().__init__()
    self.type = type
    self.Oimage = pygame.image.load("sprites/asteroid.png")
    if self.type == 1:
      self.Oimage = pygame.transform.rotate(self.Oimage, 180)
      self.image = pygame.transform.scale(self.Oimage, (85, 45))
      self.speed = 4
      self.Health = 80
      self.max_health = 80
      self.Bar_Length = 50
    elif self.type == 2:
      self.Oimage = pygame.transform.rotate(self.Oimage, 180)
      self.image = pygame.transform.scale(self.Oimage, (170, 90))
      self.speed = 3
      self.Health = 360
      self.max_health = 360
      self.Bar_Length = 75
    
    self.rect = self.image.get_rect()
    self.x = width
    self.y = random.randint(0, height - self.rect.height)
    self.rect.x = self.x
    self.rect.y = self.y
    self.frozen = False
    self.frozenTimer = 0


  def update(self):
    
    if self.frozen:
      self.frozenTimer -= 1
      self.Oimage = pygame.image.load("sprites/FrozenAsteroid.png")
      self.Oimage = pygame.transform.rotate(self.Oimage, 180)
      if self.type == 1:
        self.image = pygame.transform.scale(self.Oimage, (50, 45))
      elif self.type == 2:
        self.image = pygame.transform.scale(self.Oimage, (120, 90))
      if self.frozenTimer < 100:
        self.rect.x = self.x + random.randint(-2, 2)
        self.rect.y = self.y + random.randint(-2, 2)
      if self.frozenTimer < 1:
        self.frozen = False
        self.frozenTimer = 0
      print(self.frozenTimer)  
      
    elif not self.frozen:  
      self.Oimage = pygame.image.load("sprites/asteroid.png")
      self.Oimage = pygame.transform.rotate(self.Oimage, 180)
      if self.type == 1:
        self.image = pygame.transform.scale(self.Oimage, (85, 45))
      elif self.type == 2:
        self.image = pygame.transform.scale(self.Oimage, (170, 90))  
      self.x -= self.speed
      self.rect.x = self.x + random.randint(-2, 2)
      self.rect.y = self.y + random.randint(-2, 2)
      if self.rect.x < -self.rect.width:
        self.kill()
    if self.Health < self.max_health:
      self.draw_health()
      
  def damage(self,damage):
    if self.frozen:
      self.Health -= damage*2
      self.frozen = False
      self.frozenTimer = 0
    else:
      self.Health -= damage
    
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

  def __init__(self, x, y,Images,type):
    super().__init__()
    
    self.type = type
    if self.type == 1:
      
      self.Oimage = pygame.image.load("sprites/Bullets/bullet.png")
      self.image = pygame.transform.scale(self.Oimage, (30, 10))
      self.speed = 10
      self.damage = 20
    else:
      self.Oimage = pygame.image.load("sprites/Bullets/IceBullet.png")
      self.image = pygame.transform.scale(self.Oimage, (30, 10))
      self.speed = 7
      self.damage = 5
      
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
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
      if self.type == 1:
        self.ATimer += 1
        if self.ATimer > 2:
          self.AStage += 1
          self.ATimer = 0
        
        if self.AStage > 6:
          self.kill()
        
        else: 
          self.Oimage = self.Images[self.AStage]
          self.image = self.Oimage  
      else:
        self.kill()
        
      

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

BulletTypes = []
for i in ["bullet","IceBullet"]:
  BImage = pygame.image.load(f"sprites/Bullets/{i}.png")
  BImage = pygame.transform.scale(BImage, (30, 10))
  #BImage = pygame.transform.rotate(BImage, 90)
  
  BulletTypes.append(BImage)
  

#variables 
Health = 6
INV = 0
running = True
Timer = 100
spacePressed = False
Start = False
cooldown = 0
BulletType = 1
Ammo = 20
BulletCooldown = [20]
# Create a clock object to control the frame rate
FPS = 80
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
    type = random.randint(1,6)
    type = 2 if type == 1 else 1
    if Timer <= 0:
      Asteroids.add(Asteroid(type))

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

  
  cooldown -= 1
  if keys[pygame.K_0]:
    Start = True
  if keys[pygame.K_1]:
    BulletType = 1
  elif keys[pygame.K_2] and Ammo >1:
    BulletType = 2 

  if keys[pygame.K_SPACE] and cooldown <= 0:
    
    Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y + 40,Bullet_Images,BulletType))
    Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y,Bullet_Images,BulletType))
    if BulletType == 1:
      cooldown = 15
    elif BulletType == 2:  
      Ammo -= 2
      cooldown = 30
      if Ammo < 1:
        BulletType =1

  if Ammo < 1:
    BulletCooldown[0] -= 1
  if BulletCooldown[0] < 1:
    BulletCooldown[0] = 500
    Ammo = 20

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
          if j.type == 1:
            i.damage(j.damage)
            j.collide()
          else:
            i.damage(j.damage)
            i.frozen = True
            i.frozenTimer = 400
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
    
  
  Bx = 150
  BNUM = 1
  for i in BulletTypes:
    font = pygame.font.SysFont(None, 10)
    text = font.render(f"{BNUM}", True, (255, 255, 255))
    screen.blit(text,(Bx-10,10))
    screen.blit(i, (Bx,20))
    Bx += 50
    BNUM += 1
    

  # ... other code ...

  font = pygame.font.SysFont(None, 15)
  if Ammo < 1:
    font = pygame.font.SysFont(None, 12)
    text = font.render("RELOADING...", True, (255, 255, 255))
  else:
    font = pygame.font.SysFont(None, 15)
    text = font.render(f"{Ammo}", True, (255, 255, 255))

  # Render the text onto the screen
  
  screen.blit(text, (210, 40))   
  
  if BulletType == 2:
    pygame.draw.rect(screen, (255, 255, 255), (185, 5, 60, 50), 2)
  else:
    pygame.draw.rect(screen, (255, 255, 255), (135, 5, 55, 50), 2)
    
    

  # ... rest of your game loop ...  
  # Update the display
  pygame.display.flip()
  clock.tick(FPS)
# Quit Pygame
pygame.quit()
