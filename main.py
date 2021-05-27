import pygame, sys, random, math
pygame.init()

clock = pygame.time.Clock()

# Player attributes
playerX = 320
playerY = 600
score = 0

# Enemy attributes
enemyX = random.randint(0, 636)
enemyY = 20
delta_enemy_x = 0.5
delta_enemy_y = 0.5

# Enemy bullet
enemyBulletX = 0
enemyBulletY = 10
deltaEnBulletX = 0
deltaEnBulletY = 3
enemy_bullet_state = "ready"

# Bullet attributes
bulletX = 0
bulletY = 600
deltaBulletX = 0
deltaBulletY = 5
bullet_state = "ready"

# Coordinate System
deltaX = 0
playerVelocity = 2

# Import pictures + sounds
background = pygame.image.load('background.jpeg')
mainMenubkg = pygame.image.load('mainmenu.png')
playerImg = pygame.image.load('spaceship.png')
enemyImg = pygame.image.load('ufo.png')
bulletImg = pygame.image.load('bullet.png')
grave = pygame.image.load('grave.png')
enemyBullet = pygame.image.load('laser.png')

bkgMusic = pygame.mixer.music.load('sb_indreams.mp3')

# Fonts
font1 = pygame.font.SysFont('comicsans', 45)
font2 = pygame.font.SysFont('comicsans', 35)
font3 = pygame.font.SysFont('conicsans', 30)

# Game window
screen = pygame.display.set_mode([700, 700])

# Gets random x coordinate
def getRandCoord():
    enemyX = random.randint(0,636)
    return enemyX

# Fire bullet
def fireBullet(x, y):
    global playerX, playerY, bulletX, bulletY, bullet_state

    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Drawing text to the screen
def draw_text(text, font, color, screen, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    screen.blit(textobj, textrect)

# Collision detection
def isCollision(enemyX, enemyY, playerX, playerY):
    dist = math.sqrt(math.pow(enemyX-playerX, 2) + math.pow(enemyY-playerY, 2))

    if dist < 27:
        return True
    else:
        return False

# Enemy function
def enemy(enemyX, enemyY):
    screen.blit(enemyImg, (enemyX, enemyY))

# Player function
def player(playerX, playerY):
    screen.blit(playerImg, (playerX, playerY))

def dead():
    global running

    while running:
        screen.fill((214, 50, 21))
        draw_text('You have died...', font3, (0,0,0), screen, 270, 350)
        screen.blit(grave, (280, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    pygame.quit()
    sys.exit()

def isCollisionBullet(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))

    if dist < 27:
        return True
    else:
        return False

def enemyFire(x,y):
    global enemyX, enemyY, enemyBulletX, enemyBulletY, enemy_bullet_state

    enemy_bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

lives = 3
playerHealth = "X "

# Main game running
running = True
def runGame():
    global deltaX, deltaY, playerVelX, playerVelY, delta_enemy_x, delta_enemy_y
    global playerX, playerY, bulletX, bulletY, bullet_state
    global enemyX, enemyY, playerHealth, enemyHealth
    global running, lives, score

    while running:
        screen.fill([0, 0, 0])
        screen.blit(background, (0,0))
        draw_text('Health: ' + playerHealth * lives, font3, (255,255,255), screen, 5, 0)
        draw_text('Score: ' + str(score), font3, (255,255,255), screen, 550, 0)

        # Player movement mechanism
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    deltaX = -1
                if event.key == pygame.K_RIGHT:
                    deltaX = 1
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletX = playerX
                        fireBullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    deltaX = 0

            # if event.type == enemy_fire_event:
            #     enemyFire(enemyBulletX, enemyBulletY)

        # Bullet movement
        if bullet_state is "fire":
            fireBullet(bulletX, bulletY)
            bulletY -= deltaBulletY

        if bulletY <= 0:
            bulletY = 600
            bullet_state = "ready"

        if enemy_bullet_state is "fire":
            fireBullet(enemyBulletX, enemyBulletY)
            bulletY += deltaEnBulletY

        # Update enemy y position
        enemyY += delta_enemy_y
        enemyX += delta_enemy_x

        # Update player x position
        playerX += deltaX

        collision = isCollision(enemyX, enemyY, playerX, playerY)
        collisionBullet = isCollisionBullet(enemyX, enemyY, bulletX, bulletY)

        if collisionBullet:
            print("You have destroyed an enemy spaceship!")

            enemyX = random.randint(0, 636)
            enemyY = 0
            bullet_state = "ready"
            bulletY = 600

            score += 100

        if collision:
            print("You have been hit by the enemy!")

            # Reset enemy position
            enemyX = random.randint(0, 636)
            enemyY = 0

            lives -= 1

            if lives == 0:
                dead()

        if enemyY >= 636:
            lives -= 1

            if lives == 0:
                dead()

            enemyX = random.randint(0, 636)
            enemyY = 0

        # Boundaries (Collision)
        if playerX <= 0:
            playerX = 0
        elif playerX >= 636:
            playerX = 636

        if enemyX <= 0 or enemyX >= 636:
            delta_enemy_x *= -1

        player(playerX, playerY)
        enemy(enemyX, enemyY)
        pygame.display.flip()

    pygame.quit()

click = False

def mainMenu():
    global running, click

    while running:
        pygame.mixer.music.play()
        screen.fill([0, 0, 0])
        screen.blit(mainMenubkg, (0,0))
        draw_text('Main Menu', font2, (255,255,255), screen, 275, 220)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(260, 290, 200, 50)
        button2 = pygame.Rect(260, 400, 200, 50)

        if button1.collidepoint((mx,my)):
            if click:
                runGame()
        if button2.collidepoint((mx,my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, (255,255,255), button1)
        draw_text('Start Game', font2, (0,0,0), screen, 292, 303)

        pygame.draw.rect(screen, (255, 255, 255), button2)
        draw_text('Quit Game', font2, (0, 0, 0), screen, 292, 413)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
mainMenu()