#Written By Michael Lam (began on May 9 2020 finished on June 12 2020)
#video game project
import pygame, os, random, time
from pygame.locals import *

WINDOWWIDTH = 750
WINDOWHEIGHT = 600

#High score variables
FILENAME = "highscore.txt"
MAXSCORES=10 #max num of scores displayed 

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
MENUCOLOUR = (100,0,155)

#Framrate
FRAMERATE = 60

#stat constants
NEWENEMY = 2 #initial enemy spawn rate
NEWWAVE = 5  #time until new wave begins
SPAWNRANGE = 20 #max number for random sprite generation
MIN = 0 #minimum number for random sprite generaton

#list of spawn speeds
SPAWNSPEEDS = [2, 1.75, 1.50, 1.25, 1, 0.75, 0.50, 0.25] 

def createlist(name):
    """This function accepts a file name and reads it into a list of integers."""
    #in_file
    #entire_list
    in_file=open(name,'r')
    entire_list= in_file.readlines()
    in_file.close()

    for x in range (len(entire_list)):
        entire_list[x]=int(entire_list[x].strip())
    return entire_list

def delete(name, maxval):
    """This function accepts a file name and rewrites the file excluding extra values (only as many as the max value)"""
    #entire_list - the file read into a list
    #outfile - the new file to be created
    entire_list=createlist(name)

    outfile=open(name,'w')
    for x in range(maxval):
        outfile.write(str(entire_list[x])+'\n')
    outfile.close()    

def addnum(name, current):
    """This function takes a file name and rewrites the file with a new value in order"""
    #entire_list - the file read into a list
    #current - the current score
    #outfile - the new file to be created
    entire_list=createlist(name)
        
    outfile=open(name,'w')
    for x in range(len(entire_list)):
        if current<entire_list[x]:
            outfile.write(str(entire_list[x])+'\n')
                
    outfile.write(str(current)+'\n')
    
    for x in range(len(entire_list)):
        if current>entire_list[x]:
            outfile.write(str(entire_list[x])+'\n')
    outfile.close()

def display_scores(windowSurface, name, current):
    """Displays the current high scores"""
    windowSurface.fill(MENUCOLOUR)
    entire_list=createlist(name) #list of score read in from txt file

    #text strings to blit
    title = "High Scores"
    subtitle = "Click the mouse to continue"
    playerscore = "Your score was: " +str(current)
    #font
    basicFont = pygame.font.Font("EarthBound.ttf", 60)

    #y coordinate for displaying text
    height = 50

    #drawing text
    drawText(title, basicFont, windowSurface, WINDOWWIDTH//2-80, 10, YELLOW)
    drawText(subtitle, basicFont, windowSurface, WINDOWWIDTH//2-180, WINDOWHEIGHT-100, YELLOW)
    drawText(playerscore, basicFont, windowSurface, WINDOWWIDTH//2-125, WINDOWHEIGHT-180, YELLOW)
    for i in range(len(entire_list)):
        drawText(str(entire_list[i]), basicFont, windowSurface, WINDOWWIDTH//2-30, height, YELLOW)
        height += 30
    pygame.display.update()
    
    #checks if the player would like to continue (restarts at the menu)
    check = True
    while check:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check=False         
       
def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    image = image.convert()        #For faster screen updating
    #image = image.convert_alpha()   #Not as fast as .convert(), but works with transparent backgrounds
    return image

def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def titlescreen(windowSurface):
    """ Displays the title screen"""
    windowSurface.fill((100,0,100))
    #load font
    basicFont = pygame.font.Font("EarthBound.ttf", 150)
    secondFont = pygame.font.Font("year_is_199x.ttf", 50)

    #text strings
    title = "ZomBie battle"
    subtext = "Press 'spacebar' to continue"

    #x and y coordinates
    width = 200
    height = 170
    
    #draw text
    drawText(title, basicFont, windowSurface, width-50, height, YELLOW)
    drawText(subtext, secondFont, windowSurface, width+60, height+200, YELLOW)
    pygame.display.update()

    #checking if the user has pressed the space bar to continue
    check = True
    while check:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            elif event.type == KEYDOWN:
                # update the choice of the player
                if event.key == K_SPACE:
                    check=False         

def display_menu(windowSurface):
    """ Displays the menu so the user can choose the level of difficulty """
    windowSurface.fill(MENUCOLOUR)
    #loading fonts
    firstFont = pygame.font.Font("EarthBound.ttf", 100)
    secondFont = pygame.font.Font("year_is_199x.ttf", 70)
    
    #text strings to be displayed
    title = "Choose Your Difficulty"
    menutext = ['1. Normal', '2. Difficult', '3. Controls/Instructions']
    #y coordinate for text
    height = 230

    #drawing text
    drawText(title, firstFont, windowSurface, 130, 130, YELLOW)
    for i in range(len(menutext)):
        drawText(menutext[i], secondFont, windowSurface, 130, height, YELLOW)
        height += 70
    pygame.display.update()
    
def instructions(windowSurface):
    """displays the controls and instrucitons of the game"""
    windowSurface.fill(MENUCOLOUR)
    #load fonts
    firstFont = pygame.font.Font("EarthBound.ttf", 100)
    secondFont = pygame.font.Font("apple_kid.ttf", 30)
    height = 100 #height of the text

    #image of the kid (Ness)
    kidimage = load_image("ness peace.gif")
    
    #strings to be displayed
    title = "Instructions"
    subtitle = "Press 'spacebar' to return"
    
    #draw title
    drawText(title, firstFont, windowSurface, 50, 10, YELLOW)
    #draw instruction text
    menutext = ["You are a kid that happens to posses a magical power.",
                "However, you can only manage to conjure some kind of projectile roughly around",
                "your mid section.",
                "Luckily, you wake up in the middle of a zombie apocalypse!",
                "And it just so happens that the zombies' only weakness is magical projectiles!",
                "Your goal is to destroy as many zombies as you can before you become lunch.",
                "Good luck!",
                "",
                "Controls:",
                "'w' 'a' 's' 'd' or the arrow keys are used to move around",
                "'spacebar' shoots your projectile",
                "'esc' instantly quits the game but your score won't save",
                "'m' mutes audio"]
    for i in range(len(menutext)):
        drawText(menutext[i], secondFont, windowSurface, 50, height, YELLOW)
        height += 30
    #draw subtitle text    
    drawText(subtitle, secondFont, windowSurface, 240, 550, YELLOW)

    #blit the kids image
    windowSurface.blit(kidimage,(WINDOWWIDTH-60, 60))

    #update display
    pygame.display.update()

    
def chooselevel(windowSurface):
    """ Allows the user to choose the level.  Based on the choice, 2 variables are
    set: lives of the player and speed of the player.  These 2 stats are returned as a list. """

    #load menu screen music
    pygame.mixer.stop()
    pygame.mixer.music.load('Zombie Paper.mp3')
    
    #start Background Music
    pygame.mixer.music.play(-1, 0.0)
    musicPlaying = True
    
    levelnotchosen=True #true when player is choosing difficulty
    while levelnotchosen:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            elif event.type == KEYDOWN:
                # update the choice of the player
                if event.key == ord('1'):
                    health = 5
                    movespeed = 2
                    lives = 3
                    levelnotchosen=False
                elif event.key == ord('2'):
                    health = 3
                    movespeed = 2
                    lives = 1
                    levelnotchosen=False
                elif event.key == ord('3'):
                    instructions(windowSurface)
                #goes back to main menu   
                elif event.key == K_SPACE:
                    display_menu(windowSurface)
                    check=False    

                #music toggle
                #unfourtunatly not connected to self.musicPlaying in Game class because this has to be called before the game is created
                #therefore, the mute will not carrry over but still is functional
                elif event.key == ord('m'):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)    
                    musicPlaying = not musicPlaying
                                            
    stats = [lives, movespeed, health]
    return stats    

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        #sprite image and rect
        self.image = pygame.Surface((7,7))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        
        #position of the player
        self.rect.centery = y
        self.rect.centerx = x

        #speed of projectile
        self.speed = 10

        #direction player faces
        self.dir = direction
        
    #projectle movement    
    def update(self):
        #direction of projectile
        if self.dir == 'left':
            self.rect.left -=self.speed
        elif self.dir == 'right':
            self.rect.left +=self.speed
        elif self.dir == 'up':
            self.rect.top -=self.speed
        elif self.dir == 'down':
            self.rect.top +=self.speed
        
        #kill/remove projectile if it goes off screen
        if self.rect.top < 0:
            self.kill()
        elif self.rect.bottom >WINDOWHEIGHT:
            self.kill()
        elif self.rect.right >WINDOWWIDTH:
            self.kill()
        elif self.rect.left < 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__ (self, images1, images2, images3, lives, movespeed, hitpoints, time):
        pygame.sprite.Sprite.__init__(self)
        #load images organized by direction player faces
        self.imagesfront = images1
        self.imagesback = images2
        self.imagesside = images3

        #default image of player used to get rect
        self.image = self.imagesfront[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH//2
        self.rect.centery = WINDOWHEIGHT//4

        #player stats variables
        self.hp = hitpoints
        self.lives = lives
        self.movespeed = movespeed
        
        #Direction player faces (initially down)
        self.dir = 'down'

        #index for images
        self.index = 0

        #time for image to change
        self.startimagetime = time
        self.next = 0.15
        
        # set up movement variables
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        
    def update(self):
        #update player movement and images        
        self.endimagetime = time.time() #time used to check if player images need to change
        
        # allows for movement of the player 
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.top += self.movespeed
            #update the player's image
            if self.endimagetime - self.startimagetime > self.next:
                self.startimagetime = time.time()
                self.index +=1       
        elif self.moveUp and self.rect.top > 0:
            self.rect.top -= self.movespeed
            #update the player's image
            if self.endimagetime - self.startimagetime > self.next:
                self.startimagetime = time.time()
                self.index +=1        
        elif self.moveLeft and self.rect.left > 0:
            self.rect.left -= self.movespeed
            #update the player's image
            if self.endimagetime - self.startimagetime > self.next:
                self.startimagetime = time.time()
                self.index +=1        
        elif self.moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.right += self.movespeed
            #update the player's image
            if self.endimagetime - self.startimagetime > self.next:
                self.startimagetime = time.time()
                self.index +=1
                
        #checks if the index is larger than the lenght image list and resets back to first image
        if self.index >= len(self.imagesfront):
            #we will make the index to 0 again
            self.index = 0

        #checks direction player is facing to determine which images to diaplay
        if self.dir == 'down':
            #updates the image that will be displayed based on direction
            self.image = self.imagesfront[self.index]  
        elif self.dir =='up':       
            self.image = self.imagesback[self.index]
        elif self.dir == 'left':    
            self.image = self.imagesside[self.index]
        elif self.dir =='right':     
            self.image = pygame.transform.flip(self.imagesside[self.index],True, False) #same images as walking left but flipped
            
class Enemy(pygame.sprite.Sprite):
    def __init__ (self, image):#, movespeed, hitpoints, score): (stat variables that were to be used in the future if I return to this project)
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        
        #random spawning
        self.toporsides=random.randrange(0,2) #random variable to determine if enemies will spawn on top/bottom or sides of screen
        if self.toporsides == 1:
            #random spawning for sides
            self.rect.centery = random.randrange(200, WINDOWHEIGHT-300)
            self.randnum = random.randrange(0,2)
            if self.randnum == 1:
                self.rect.centerx = -10
            else:
                self.rect.centerx = WINDOWWIDTH + 10
        else:
            #random spawning for top/bottom
            self.rect.centerx = random.randrange(300, WINDOWWIDTH)
            self.randnum = random.randrange(0,2)
            if self.randnum == 1:
                self.rect.centery = -10
            else:
                self.rect.centery = WINDOWWIDTH + 10
                        
        #zombie stats variables
        self.movespeed = 1

    def update(self, x, y):
        # allows for movement of the enemy
        
        #player position
        self.targetx = x
        self.targety = y
        
        #movement in the x direction
        if self.rect.centerx - self.targetx >0:
            self.rect.right -= self.movespeed
        elif self.rect.centerx - self.targetx < 0:
            self.rect.right += self.movespeed
            
        #movement in the y direction
        if self.rect.centery - self. targety >0:
            self.rect.top -= self.movespeed
        elif self.rect.centery - self. targety <0:
            self.rect.top += self.movespeed

       
class Game():
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self, stats):
        """ Constructor. Create all our attributes and initialize
        the game. The stats provided customize the game. """

        #Set to true when all food/lives are gone
        self.game_over = False

        #Controls when new enemy is added
        self.startenemytime = time.time()

        #Controls enemy spawn rate
        self.startspawntime = time.time()

        #Controls player animation
        self.startimagetime = time.time()

        #Set up all sprites group
        self.all_sprites = pygame.sprite.Group()

        #Projectile group
        self.bullets = pygame.sprite.Group()

        #High score variables
        self.hits = 0
        self.scores =[] #list to be read in of all high scores from txt file
        
        #Enemy spawn rate variables
        self.newenemy = NEWENEMY
        self.spawn = 0 #counter used to increase spawn rate using SPAWNSPEED which is a list of incremental speeds (ex SPAWNSPEED[self.spawn])
        
        #Load background image
        self.bg1 = load_image('background test5.png')
    
        #Load player images
        self.imagesfront = []
        self.imagesfront.append(load_image('ness front.gif'))
        self.imagesfront.append(load_image('ness front 2.gif'))

        self.imagesback = []
        self.imagesback.append(load_image('ness back.gif'))
        self.imagesback.append(pygame.transform.flip(self.imagesback[0],True, False))

        self.imagesside = []
        self.imagesside.append(load_image('ness west.gif'))
        self.imagesside.append(load_image('ness west 2.gif'))
    
        #Instantiate player and add to all sprites
        self.player = Player(self.imagesfront, self.imagesback, self.imagesside, stats[0], stats[1], stats[2],self.startimagetime)
        self.all_sprites.add(self.player)

        #Enemy sprite group
        self.enemies = pygame.sprite.Group()
        
        #Enemy variables
        self.newenemy = NEWENEMY
        
        #enemy images
        self.Enemyimage = load_image('zombie.gif')
        self.Enemyimage_2 = load_image('ghost.gif')
        self.Enemyimage_3 = load_image('master.gif')
        
        #normal enemy base score
        self.score = 10
        #extra points for master enemy
        self.boss = False #determines whether or not a special enemy has spawned
        self.extrascore = 50
        
        #Set up music and sound for main game screen
        self.playerhit = pygame.mixer.Sound('bump.wav')
        self.enemyhit = pygame.mixer.Sound('enemyhit.wav')
        pygame.mixer.music.load('Battle Against Belch.mp3')
        #self.gameOverSound = pygame.mixer.Sound('A Bad Dream.mp3')

        #start Background Music
        pygame.mixer.music.play(-1, 0.0)
        self.musicPlaying = True
    
    
    def process_events(self, windowSurface):
        """ Respond to keyboard and mouse clicks"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            elif event.type == KEYDOWN:
                # update the direction of the player
                if event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveLeft = True
                    self.player.moveRight = False
                    self.player.moveUp = False
                    self.player.moveDown = False                    
                    #player direction variable used to determine direction to shoot projectiles
                    self.player.dir = 'left'
                    
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveLeft = False
                    self.player.moveRight = True
                    self.player.moveUp = False
                    self.player.moveDown = False
                    #player direction variable used to determine direction to shoot projectiles
                    self.player.dir = 'right'
                    
                    
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.moveLeft = False
                    self.player.moveRight = False
                    self.player.moveUp = True
                    self.player.moveDown = False
                    #player direction variable used to determine direction to shoot projectiles
                    self.player.dir = 'up'
                    
                    
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.moveLeft = False
                    self.player.moveRight = False
                    self.player.moveUp = False
                    self.player.moveDown = True
                    #player direction variable used to determine direction to shoot projectiles
                    self.player.dir = 'down'
                    
                elif event.key == K_SPACE:
                    #add a projectile to all_sprites group and bullets group
                    abullet = Projectile(self.player.rect.centerx, self.player.rect.centery, self.player.dir)
                    self.all_sprites.add(abullet)
                    self.bullets.add(abullet)
                
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    os._exit(1)
                # the player has stopped moving
                elif event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveLeft = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveRight = False
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.moveUp = False
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.moveDown=False      
                
                #music and sound toggle
                elif event.key == ord('m'):
                    if self.musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)    
                    self.musicPlaying = not self.musicPlaying

            elif event.type == pygame.MOUSEBUTTONDOWN:
                #the user clicks to restart the game
                if self.game_over:
                    #display menu, choose level and start new game
                    display_scores(windowSurface,FILENAME,self.hits)
                    display_menu(windowSurface)
                    stats = chooselevel(windowSurface)
                    self.__init__(stats)    

    def run_logic(self, windowSurface):
        """ Check for collisions and check if time to add new enemies and increase spawn rate"""
        
        if not self.game_over:
            
            # check for collisions and remove hp it there is one
            enemy_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for anenemy in enemy_hit_list:
                self.player.hp -=1
                
                #play hit sound if there's a collision
                if self.musicPlaying:      
                    self.playerhit.play()

            #Check for bullet collisions
            bullet_hit_list = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for anenemy in bullet_hit_list:
                if self.boss:
                    self.hits += self.extrascore
                else:
                    self.hits += self.score

                #play hit sound if there's a collision
                if self.musicPlaying:      
                    self.enemyhit.play()
            
            #Check if it is time to add another enemy 
            endenemytime = time.time()
            if endenemytime - self.startenemytime >= self.newenemy:
                # add new enemy
                ransprites = random.randrange(0,SPAWNRANGE)
                if ransprites > SPAWNRANGE//4:
                    self.startenemytime = time.time()
                    anenemy = Enemy(self.Enemyimage)
                    self.enemies.add(anenemy)
                    self.all_sprites.add(anenemy)
                    self.boss = False
                elif ransprites == MIN:
                    self.startenemytime = time.time()
                    anenemy = Enemy(self.Enemyimage_3)
                    self.enemies.add(anenemy)
                    self.all_sprites.add(anenemy)
                    self.boss = True
                else:
                    self.startenemytime = time.time()
                    anenemy = Enemy(self.Enemyimage_2)
                    self.enemies.add(anenemy)
                    self.all_sprites.add(anenemy)
                    self.boss = False

            #Check if it's time to increase spawn rate
            if self.newenemy != SPAWNSPEEDS[len(SPAWNSPEEDS)-1]:
                newwavetime = time.time()
                if newwavetime - self.startspawntime >= NEWWAVE:
                    #increase spawn rate
                    self.startspawntime = time.time()
                    self.newenemy = SPAWNSPEEDS[self.spawn]
                    self.spawn+=1

            #Update all classes with movement
            self.player.update()
            self.bullets.update()
            self.enemies.update(self.player.rect.centerx,self.player.rect.centery)
            
            #Check if the player has hit the boundries of the buildings
            #top building
            if self.player.rect.top <70 and self.player.rect.centerx < 340:
                self.player.moveUp = False     
            elif self.player.rect.top < 70 and self.player.rect.left < 340:
                self.player.moveLeft = False
            
            #bottom left building    
            elif self.player.rect.bottom > WINDOWHEIGHT-175 and self.player.rect.centerx < 260:
                self.player.moveDown=False     
            elif self.player.rect.bottom > WINDOWHEIGHT-175 and self.player.rect.left < 260:
                self.player.moveLeft = False 
            elif self.player.rect.bottom > WINDOWHEIGHT-230 and self.player.rect.centerx < 60:
                self.player.moveDown=False
            elif self.player.rect.bottom > WINDOWHEIGHT-230 and self.player.rect.left < 60:
                self.player.moveLeft = False

            #Game over when hp is 0
            if self.player.hp<=0:
                self.game_over = True
                if self.musicPlaying:
                    #play game over music
                    pygame.mixer.stop()
                    pygame.mixer.music.load('A Bad Dream.mp3')
                    pygame.mixer.music.play(-1, 0.0)


    def display_frame(self, windowSurface):
        """Update the screen """
        # draw the black background onto the surface
        windowSurface.blit(self.bg1,(0,0))
        if self.game_over:
            #restarts game if user clicks screen
            x = WINDOWWIDTH // 4
            y = WINDOWHEIGHT // 2 - 40
            basicFont = pygame.font.Font("EarthBound.ttf", 60)
            drawText("GAME OVER, CLICK TO RESTART", basicFont, windowSurface, x ,y, (100,0,155))
                
            #highscore file writting
            self.scores=createlist(FILENAME)
            if len(self.scores)==MAXSCORES:
                for ascore in self.scores:
                    if self.hits>ascore:
                        addnum(FILENAME,self.hits)
                        delete(FILENAME,MAXSCORES)
            else:
                addnum(FILENAME,self.hits)
                
        else:
            #Draw health points(HP) and current score
            displayhealth = "HP:" + str(self.player.hp)
            score = "SCORE: "+str(self.hits)
            basicFont = pygame.font.Font('debugme.ttf', 100)
            basicFont2 = pygame.font.Font('apple_kid.ttf', 40)
            drawText(displayhealth, basicFont, windowSurface, WINDOWWIDTH-110 ,WINDOWHEIGHT-38, (255,0,0))
            drawText(score, basicFont2, windowSurface, 10, WINDOWHEIGHT-40, (255,255,0))
            
            # draw the sprites
            self.all_sprites.draw(windowSurface)
    
        # draw the window onto the screen  
        pygame.display.update()

def main():    
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()

    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Zombie Battle')
    
    #Title screen
    titlescreen(windowSurface)
    
    #Display menu, choose difficulty, Instansiate the game
    display_menu(windowSurface)
    stats = chooselevel(windowSurface)
    game = Game(stats)
    
    # run the game loop
    while True:
        # Process events (keystrokes, mouse clicks, etc)
        game.process_events (windowSurface)

        # process collisions and add food if necessary
        game.run_logic(windowSurface)
        
        # display the player and all the food
        game.display_frame(windowSurface)   

        #Update the clock    
        mainClock.tick(FRAMERATE)

main()

