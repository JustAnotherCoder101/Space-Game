import pygame 
import random
import math

# Initialize Pygame
pygame.init()

# Set screen dimensions
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
#Sprites

SCORE = 0
ASTEROIDSPAWN = True



class Explode(pygame.sprite.Sprite):
  def __init__(self, x, y, size):
    super().__init__()
    self.Oimage = pygame.image.load(f"sprites/Bullets/Explosion{random.randint(1,2)}.png")
    self.image = pygame.transform.scale(self.Oimage, (50, 50))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.exploding = True
    self.expanding = True
    self.retracting = False
    self.Timer = 50
    self.size = 50
    self.Msize = size
    self.OY = self.rect.y
    self.OX = self.rect.x        
    if size == 200:
      self.type = 2
    else:
      self.type = 1  
  
  def update(self):

    self.image = pygame.transform.scale(self.Oimage, (self.size, self.size))
    if self.size > self.Msize:
      self.expanding = False
      self.retracting = True
    if self.expanding:
      self.rect.y = self.OY - (self.size / 2)

      self.rect.x = self.OX - (self.size / 2)
      self.size += 10
    else:
      self.rect.y = self.OY - (self.size / 2)
      self.rect.x = self.OX - (self.size / 2)

      
      self.size -= 5 /self.type
    if self.retracting and self.size < 10:
      self.kill()


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
  global SCORE
  
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
      self.S = 1
      self.size = 100
    elif self.type == 2:
      self.Oimage = pygame.transform.rotate(self.Oimage, 180)
      self.image = pygame.transform.scale(self.Oimage, (170, 90))
      self.speed = 3
      self.Health = 360
      self.max_health = 360
      self.Bar_Length = 75
      self.S = 3
      self.size = 200
    
    self.rect = self.image.get_rect()
    self.x = width
    self.y = random.randint(0, height - self.rect.height)
    self.rect.x = self.x
    self.rect.y = self.y
    self.frozen = False
    self.frozenTimer = 0
    self.mask = pygame.mask.from_surface(self.image)


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
    global SCORE
    if self.frozen:
      self.Health -= damage*2
      self.frozen = False
      self.frozenTimer = 0
      Asteroid_oof.play()
    else:
      self.Health -= damage
      Asteroid_oof.play()
    
    if self.Health < 1:
      Asteroid_kill.play()
      SCORE += self.S
      Explosions.add(Explode(self.rect.centerx, self.rect.centery,self.size))
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

class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed=5):
        super().__init__()
        self.image = pygame.image.load("sprites/Boss 1/Orb.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Normalize direction
        length = math.hypot(dx, dy)
        if length == 0:
            self.dx, self.dy = 1, 0
        else:
            self.dx = dx / length
            self.dy = dy / length
        self.speed = speed
        self.Health = 1
        self.angle = math.atan2(self.dy, self.dx)
        # Rotate the image to point in the direction of travel
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += int(self.dx * self.speed)
        self.rect.y += int(self.dy * self.speed)
        # Remove if out of screen
        if (self.rect.x < -self.rect.width or self.rect.x > width or
            self.rect.y < -self.rect.height or self.rect.y > height):
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.Oimage = pygame.image.load("sprites/Boss 1/Missile.png")
        self.image = pygame.transform.scale(self.Oimage, (50, 50))  # Scale down the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3,9)
        self.Health = 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Calculate the angle to the player
        dx = SHIP.rect.x - self.rect.x
        dy = SHIP.rect.y - self.rect.y
        angle = math.atan2(dy, dx)
        
        # Rotate the image to point towards the player
        self.image = pygame.transform.rotate(self.Oimage, -math.degrees(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Move the missile towards the player
        self.rect.x += int(self.speed * math.cos(angle))
        self.rect.y += int(self.speed * math.sin(angle))
        
        if self.rect.x < -self.rect.width or self.rect.y < -self.rect.height or self.rect.y > height:
            self.kill()

    def damage(self, damage):
        global SCORE
        self.Health -= damage
        if self.Health < 1:
            Asteroid_kill.play()
            Explosions.add(Explode(self.rect.centerx, self.rect.centery, 50))
            self.kill()


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
    self.mask = pygame.mask.from_surface(self.image)
    
    

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

 

class BOSS1(pygame.sprite.Sprite):
  global ASTEROIDSPAWN
  def __init__(self):
    super().__init__()
    self.Oimage = pygame.image.load("sprites/Boss 1/Boss 1.png")
    self.Simage = pygame.image.load("sprites/Boss 1/Hatch.png")
    self.image = pygame.transform.scale(self.Oimage, (int(135*0.75), int(220*0.75)))
    self.rect = self.image.get_rect()
    self.rect.x = width
    self.rect.y = height // 2 - self.rect.height // 2
    self.speed = 5
    self.Health = 3000
    self.max_health = 3000
    self.Bar_Length = 150
    self.mask = pygame.mask.from_surface(self.image)
    self.action = 0
    self.movingTimer = 60
    self.actionTimer = 60
    self.moving = 0
    self.TIMER = 0
    self.DESPERATION = 1
    self.orb_attack_active = False
    self.orb_attack_count = 0
    self.orb_attack_timer = 0

  def orb_attack(self):
    """Handles the orb attack: 5 bursts of 5 orbs over 15 seconds."""
    self.orb_attack_timer += 1
    # Every 3 seconds (approx 240 frames at 80 FPS), spawn 5 orbs
    if self.orb_attack_timer % (FPS * 3 // 5) == 0 and self.orb_attack_count < 8:
      # Spawn orbs at the boss's left side, at varying angles to the left
      centerx = self.rect.left  # left edge of boss
      centery = self.rect.centery
      # Angles: spread from -30 to +30 degrees (all going left)
      for i in range(5):

        offset = random.randint(-1*i, 1*i)
        angle_deg = -30 + i * 15  # -30, -15, 0, 15, 30
        angle_rad = math.radians(angle_deg)
        dx = math.cos(angle_rad) * -1  # negative x for leftward
        dy = math.sin(angle_rad)
        Orbs.add(Orb(centerx, centery, dx, dy, speed=6))
      self.orb_attack_count += 1
    if self.orb_attack_count >= 5:
      self.orb_attack_active = False
      self.orb_attack_count = 0
      self.orb_attack_timer = 0

  def update(self):
    self.TIMER += 1
    if self.TIMER > 2 * FPS:
      self.TIMER = 0
    if self.rect.x > width - self.rect.width - 50:
      self.rect.x = width - self.rect.width - 50
      self.rect.x -= self.speed

    self.draw_health()

    if self.movingTimer > 0:
      self.movingTimer -= 1
    else:
      self.moving = random.randint(1, 4)
      self.movingTimer = 50

    if self.moving == 1:
      self.move("up")
    elif self.moving == 2:
      self.move("down")
    elif self.moving == 3:
      self.move("mid")

    # ATTACKS
    if self.actionTimer > 0:
      self.actionTimer -= 1
    else:
      if self.DESPERATION == 1:
        #self.action = random.randint(0, 3)
        self.action = 3
      elif self.DESPERATION == 2:
        self.action = random.randint(0, 3)

      self.TIMER = 0

      if self.action == 1:
        self.actionTimer = 50
      elif self.action == 2:
        self.actionTimer = 100
      elif self.action == 3:
        # Start orb attack: 5 bursts over 15 seconds
        self.orb_attack_active = True
        self.orb_attack_count = 0
        self.orb_attack_timer = 0
        self.actionTimer = FPS * 10 # 15 seconds

    if self.action == 1:
      if self.TIMER in [0, 50, 100]:
        self.shoot(1)
    elif self.action == 2:
      self.shoot(2)

    # Call orb attack if active
    if self.orb_attack_active:
      self.orb_attack()

  def draw_health(self):
    health = (self.Health / self.max_health) * self.Bar_Length * 2
    pygame.draw.rect(screen, (0, 0, 0), (width // 2 - self.Bar_Length - 5, 10, self.Bar_Length * 2 + 10, 30))
    pygame.draw.rect(screen, (255, 0, 0), (width // 2 - self.Bar_Length, 20, self.Bar_Length * 2, 10))
    pygame.draw.rect(screen, (0, 255, 0), (width // 2 - self.Bar_Length, 20, health, 10))

  def damage(self, damage):
    global ASTEROIDSPAWN
    global BOSSCOUNT
    self.Health -= damage
    if self.Health < 1:
      self.kill()
      ASTEROIDSPAWN = True
      BOSSCOUNT -= 1

  def shoot(self, type):
    if type == 1:
      self.image = pygame.transform.scale(self.Simage, (int(135*0.75), int(220*0.75)))
      self.image = pygame.transform.scale(self.Oimage, (int(135*0.75), int(220*0.75)))
      for i in range(self.DESPERATION * 5):
        Missiles.add(Missile(self.rect.centerx, self.rect.centery + (i - 1) * 50))
    elif type == 2:
      pass

  def move(self, direction):
    if direction == "start" and self.rect.x > width - self.rect.width - 50:
      self.rect.x -= self.speed
    if direction == "up" and self.rect.y > 20:
      self.rect.y -= self.speed
    if direction == "down" and self.rect.y < 380 - self.rect.height:
      self.rect.y += self.speed
    if direction == "mid" and self.rect.y != 200 - self.rect.height // 2:
      if self.rect.y > 200 - self.rect.height // 2:
        self.rect.y -= self.speed
      if self.rect.y < 200 - self.rect.height // 2:
        self.rect.y += self.speed

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

def CHANGE_SOUND(num):
  pygame.mixer.music.stop()
  if num == 0:
    pygame.mixer.music.load('background.wav')
  elif num == 1:
    pygame.mixer.music.load('BOSSFIGHT1.mp3')
  pygame.mixer.music.play(-1)
  


pygame.mixer.init()

# Load sounds
sound_group = []

pew_sound = pygame.mixer.Sound('pew.wav')
Asteroid_oof = pygame.mixer.Sound('damage.mp3')
Asteroid_kill = pygame.mixer.Sound('kill.mp3')
# Set volume for individual sounds
pew_sound.set_volume(0.5)  # Set to 50% volume
Asteroid_oof.set_volume(0.8)  # Set to 80% volume
Asteroid_kill.set_volume(0.5)  # Full volume



Player_Damage = pygame.mixer.Sound('Crunch.wav')

sound_group.append(pew_sound)
sound_group.append(Player_Damage)
sound_group.append(Asteroid_kill)
sound_group.append(Asteroid_oof)

CHANGE_SOUND(0)

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
Explosions = pygame.sprite.Group()
Missiles = pygame.sprite.Group()
Orbs = pygame.sprite.Group()

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
Ammo = [10,10]
BulletCooldown = [500,500]
# Create a clock object to control the frame rate
FPS = 80
Shake = 0
clock = pygame.time.Clock()
FSIZE = 56
Score_Font = pygame.font.SysFont(None, 40)  # or pygame.font.Font("path/to/font.ttf", font_size)


SCORE = 0

MUSIC = 1

MC = True

BOSSCOUNT = 0

Timer2 = -1.0

Boss = pygame.sprite.Group()
# Loop
print("Done")

while running:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  Timer2 += 1.0 / FPS
  if Timer2 > 1.0:
    Timer2 = -1.0
        

  
  if Start and ASTEROIDSPAWN:
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
  if keys[pygame.K_8]:
    #Missiles.add(Missile(width, random.randint(0, height - 100)))
    SCORE = 51
  if keys[pygame.K_9]:
      # Spawn five orbs in different directions
      Orbs.add(Orb(width // 2, height // 2, -1, 0, speed=5))      # West
      Orbs.add(Orb(width // 2, height // 2, -1, -1, speed=5))     # North West
      Orbs.add(Orb(width // 2, height // 2, -2, -1, speed=5))     # North West West
      Orbs.add(Orb(width // 2, height // 2, -1, 1, speed=5))      # South West
      Orbs.add(Orb(width // 2, height // 2, -2, 1, speed=5))      # South West West
  if keys[pygame.K_m]: 
     if MC:
       MC = False
       if MUSIC == 0:
          CHANGE_SOUND(0)
          MUSIC = 1

       else:
          CHANGE_SOUND(1)
          MUSIC = 0
          Boss.add(BOSS1())
          ASTEROIDSPAWN = False

  else:
    MC = True     
      
  if SCORE > 50 and BOSSCOUNT < 1:
    CHANGE_SOUND(1)
    MUSIC = 0
    Boss.add(BOSS1())
    ASTEROIDSPAWN = False
    BOSSCOUNT += 5 


  if keys[pygame.K_0]:
    Start = True
  if keys[pygame.K_1]:
    BulletType = 1
  elif keys[pygame.K_2] and Ammo[0] > 1:
    BulletType = 2 

  if keys[pygame.K_SPACE] and cooldown <= 0:
    
    Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y + 40,Bullet_Images,BulletType))
    Bullets.add(Bullet(SHIP.rect.x + 25, SHIP.rect.y,Bullet_Images,BulletType))
    pew_sound.play()

    if BulletType == 1:
      cooldown = 15
    elif BulletType == 2:  
      Ammo[0] -= 2
      cooldown = 30
      if Ammo[0] < 1:
        BulletType =1

  if Ammo[0] < 1:
    BulletCooldown[0] -= 1
  if BulletCooldown[0] < 1:
    BulletCooldown[0] = 500
    Ammo[0] = Ammo[1]

  # game things

  # make the background

  screen.blit(BACKGROUND, (0, 0))
  SHIP.tick(INV)
  Player.update()
  Asteroids.update()
  Bullets.update()
  Boss.update()
  Explosions.update()
  Missiles.update()
  Orbs.update()

  for i in Player:
    if pygame.sprite.spritecollideany(i, Asteroids) and INV < 1:
      Shake = 10
      Health -= 1
      INV = 40
      Player_Damage.play()

  for i in Player:
    if pygame.sprite.spritecollideany(i, Missiles) and INV < 1:
      Shake = 10
      Health -= 1
      INV = 40
      Player_Damage.play()
  for i in Player:
    if pygame.sprite.spritecollideany(i, Orbs) and INV < 1:
      Shake = 10
      Health -= 1
      INV = 40
      Player_Damage.play()    

  for i in Asteroids:
    for j in Bullets:
      if pygame.sprite.collide_mask(i, j):
        if j.active:
          if j.type == 1:
            i.damage(j.damage)
            j.collide()
          else:
            i.damage(j.damage)
            i.frozen = True
            i.frozenTimer = 400
            j.collide()
             
  for i in Missiles:
    for j in Bullets:
      if pygame.sprite.collide_mask(i, j):
        if j.active:
          if j.type == 1:
            i.damage(j.damage)
            #j.collide()
          else:
            i.damage(j.damage)
            i.frozen = True
            i.frozenTimer = 400
            #j.collide()          
        

  for boss in Boss:
    for j in Bullets:
      if pygame.sprite.collide_mask(boss, j):
        if j.active:
          boss.damage(j.damage)
          j.collide()

        else:
          pass
  for i in Bullets:
    if pygame.sprite.spritecollideany(i, Asteroids, pygame.sprite.collide_mask) or pygame.sprite.spritecollideany(i, Boss, pygame.sprite.collide_mask):
      i.active = False
      
  
  Player.draw(screen)
  Asteroids.draw(screen)
  Bullets.draw(screen)
  Boss.draw(screen)
  Explosions.draw(screen)
  Missiles.draw(screen)
  Orbs.draw(screen)

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
    Bx += 55
    BNUM += 1
    

  # ... other code ...

  font = pygame.font.SysFont(None, 15)
  if Ammo[0] < 1:
    font = pygame.font.SysFont(None, 12)
    text = font.render("RELOADING...", True, (255, 255, 255))
    screen.blit(text, (250- text.get_width(), 40))  
  else:
    font = pygame.font.SysFont(None, 15)
    text = font.render(f"{Ammo[0]}/{Ammo[1]}", True, (255, 255, 255))
    screen.blit(text, (230- text.get_width(), 40))  

  # Render the text onto the screen
  
   
  
  if BulletType == 2:
    pygame.draw.rect(screen, (255, 255, 255), (190, 5, 55, 50), 2)
  else:
    pygame.draw.rect(screen, (255, 255, 255), (135, 5, 55, 50), 2)
    
  if Ammo[0] < 1:
    #pygame.draw.rect(screen, (255, 255, 255), (195, 50, , 5),1)
    pygame.draw.rect(screen, (255, 255, 255), (200, 50,BulletCooldown[0]/12, 5),0)

  # score text
  font_str = len(str(SCORE))
  Score_text = Score_Font.render(f"Score: {SCORE}",True,(255,255,255))
  screen.blit(Score_text, (680-(20*font_str),10))

  
  # Update the display
  pygame.display.flip()
  clock.tick(FPS)
# Quit Pygame
pygame.quit()
