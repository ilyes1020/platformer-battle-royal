import pygame
import pgzrun
from pgzhelper import *
from time import *

"""
Run Joystick.py to play with the joystick

"""


#constantes
WIDTH = 1024
HEIGHT = 640
ICON = 'images/image_part_0010.png' #nécessite d'ouvrir le dossier dans VSC

game_over = False
running= False
can_jump = True
goblin1_moving = True
fly1_moving = True
goblin2_moving = True
attacking = False
au_sol = True
a_droite = True
a_gauche = True
win = False
menu = True
coeurs = 3
actual_level = 0

cooldown_attack_tracker = 0

map_speed = 8

clock = pygame.time.Clock()

musics = ["ff7_music","ffix_fight","ffx_fight","op_fight","dbs_fight ost","ff7_fight","ff7_boss","ff7_lost","ff7_victory","dbz_menu"]

music.set_volume(0.75)
music.play(musics[9])


#animation
base = "image_part_0010","image_part_0011","image_part_0012","image_part_0013"
vol = "image_part_007","image_part_008","image_part_009"
course = "image_part_001","image_part_002", "image_part_003", "image_part_004", "image_part_005","image_part_006"
fight_joueur1 = "image_part_0024","image_part_0025","image_part_0026", "image_part_0027"
hit_joueur1="image_part_0028","image_part_0029","image_part_0030"


course_goblin = "image_part_0014","image_part_0015","image_part_0016","image_part_0017","image_part_0018","image_part_0019"
fight_goblin = "image_part_0020","image_part_0021", "image_part_0022", "image_part_0023"
hit_goblin = "image_part_0031","image_part_0032", "image_part_0033"

course_fly = "image_part_0034","image_part_0035", "image_part_0036"
hit_fly = "image_part_0037","image_part_0038", "image_part_0039"

#carte
carte = Actor("carte.png")

carte.topleft = 0,0


#Rect
ROUGE = 200, 0, 0
sol = Rect((0, 0), (2877, 16))
sol.x = 0
sol.y = 512

ciel = Rect((0, 0), (15400, 16))
ciel.x = 0
ciel.y= 0

cube1 = Rect((0,0), (64, 16))
cube1.x = 1344
cube1.y = 448

cube2 = cube1.copy()
cube2.x = 1408
cube2.y = 384

cube3 = Rect((0,0), (160, 16))
cube3.x = 1472
cube3.y = 320

cube4 = cube3.copy()
cube4.x = 1632
cube4.y = 320

cube5 = cube1.copy()
cube5.x = 1792
cube5.y = 384

cube6 = cube1.copy()
cube6.x = 1856
cube6.y = 448

cube7 = Rect((0,0), (190, 16))
cube7.x = 4930
cube7.y = 448

cube8 = cube7.copy()
cube8.x = 5375
cube8.y = 448

cube9 = cube1.copy()
cube9.x = 4994
cube9.y = 384

cube10 = cube1.copy()
cube10.x = 5442
cube10.y = 384

cube11 = Rect((0,0), (128, 16))
cube11.x = 5184
cube11.y = 576

platform1 = cube7.copy()
platform1.x = 3070
platform1.y = 512

platform2 = platform1.copy()
platform2.x = 3460
platform2.y = 512

platform3 = platform1.copy()
platform3.x = 3840
platform3.y = 512

platform4 = platform1.copy()
platform4.x = 10752
platform4.y= 322

platform5 = platform1.copy()
platform5.x = 11074
platform5.y = 322

platform6 = platform1.copy()
platform6.x= 11968
platform6.y= 256

platform7 = platform1.copy()
platform7.x= 13184
platform7.y= 320

platform8 = platform1.copy()
platform8.x= 13570
platform8.y= 256

platform9 = platform1.copy()
platform9.x= 13952
platform9.y= 320

sol1 = Rect((0, 0), (960, 16))
sol1.x =4226
sol1.y= 512

sol2 = Rect((0, 0), (3390, 16))
sol2.x = 5312
sol2.y = 512

sol3 = Rect((0, 0), (1724, 16))
sol3.x = 8900
sol3.y = 512

sol4 = Rect((0,0),(1324, 16))
sol4.x= 11394
sol4.y = 512

sol5 = Rect((0,0),(2366, 16))
sol5.x=13010
sol5.y=512

sol6 = Rect((0,0),(268, 16))
sol6.x=12732
sol6.y=576

game_over_image = Actor("game_over")
game_over_image.center = (WIDTH / 2, HEIGHT / 4)

menu_image = Actor("menu")
menu_image.topleft = 0,0

victory_image = Actor("victory_image")
victory_image.center = (WIDTH / 2, HEIGHT / 4)
#Joueur 1

joueur1 = Actor("image_part_0010")

joueur1_animation = []

joueur1.images = joueur1_animation

joueur1.fps = 8

joueur1.x = 200

joueur1.bottom = sol.y + 1

#Coeurs
coeur1 = Actor("hearts_hud")
coeur2 = Actor("hearts_hud")
coeur3 = Actor("hearts_hud")

coeur1.x = 50


coeur2.left = coeur1.right + 20
coeur3.left = coeur2.right + 20

#Goblin1

goblin1 = Actor ("image_part_0014")

goblin1_animation = []

goblin1.images = goblin1_animation

goblin1.fps = 8

goblin1.x = 600

goblin1.bottom = sol.y + 1

#fly1

fly1 = Actor ("image_part_0034")

fly1_animation = []

fly1.images = fly1_animation

fly1.fps = 8

fly1.x = 1400

fly1.y = 256


#Goblin2

goblin2 = Actor ("image_part_0014")

goblin2_animation = []

goblin2.images = goblin2_animation

goblin2.fps = 8

goblin2.x = 1200

goblin2.bottom = sol.y + 1

#murs

mur1 = Actor("murs")

mur1.x = 2560

mur1.bottom= sol.y + 1

mur2 = Actor("murs")

mur2.x = 0

mur2.bottom= sol.y + 1


#fonction qui fait tomber le perso
def fall(gravity):
    can_jump = False
    joueur1.y = joueur1.y + gravity
    joueur1_animation[0:]= vol

#fonction qui fait sauter le perso
def jump(jump_height):
    joueur1.y = joueur1.y - jump_height

#fonction qui déplace le perso sur la droite
def right(player_speed):
    joueur1.x= joueur1.x + player_speed
    joueur1_animation[0:]= course
    joueur1.flip_x = False

def joueur1_base():

    global attacking
    joueur1_animation[0:]= base

#fonction qui déplace le perso sur la gauche
def left(player_speed):
    joueur1.x= joueur1.x - player_speed
    joueur1_animation[0:]= course
    joueur1.flip_x = True

def attack():
    joueur1_animation[0:]= fight_joueur1

    cooldown_attack_maker()

def goblin1_right(npc_speed):
    goblin1_animation[0:]= course_goblin
    goblin1.flip_x = False
    goblin1.x = goblin1.x + npc_speed

def goblin1_left(npc_speed):
    goblin1_animation[0:]= course_goblin
    goblin1.flip_x = True
    goblin1.x = goblin1.x - npc_speed

def goblin2_right(npc_speed):
    goblin2_animation[0:]= course_goblin
    goblin2.flip_x = False
    goblin2.x = goblin2.x + npc_speed

def goblin2_left(npc_speed):
    goblin2_animation[0:]= course_goblin
    goblin2.flip_x = True
    goblin2.x = goblin2.x - npc_speed

def fly1_right(npc_speed):
    fly1_animation[0:]= course_fly
    fly1.flip_x = True
    fly1.x = fly1.x + npc_speed

def fly1_left(npc_speed):
    fly1_animation[0:]= course_fly
    fly1.flip_x = False
    fly1.x = fly1.x - npc_speed

#fonction pour monter le cooldown d'attaque
def cooldown_attack_maker():
    global cooldown_attack_tracker
    cooldown_attack_tracker += clock.get_time()
    if cooldown_attack_tracker >=450:
        cooldown_attack_tracker = 450

#fonction pour baisser le cooldown
def cooldown_attack_inverser():
    global cooldown_attack_tracker
    cooldown_attack_tracker -= clock.get_time()
    if cooldown_attack_tracker < 0:
        cooldown_attack_tracker = 0

temps =0
def joueur1_hit():
    global temps
    global coeurs
    joueur1_animation[0:]= hit_joueur1
    temps2=time()
    if temps2-temps >1:
        sounds.minecraft_hit.play()
        temps = temps2
        coeurs -=1


goblin1_hit_counter = 3
def goblin1_death():
    global goblin1_hit_counter
    global temps
    goblin1_animation[0:]= hit_goblin
    temps2=time()
    if temps2-temps >1:
        sounds.sword_hit.play()
        temps = temps2
        goblin1_hit_counter -= 1

goblin2_hit_counter = 3
def goblin2_death():
    global goblin2_hit_counter
    global temps
    goblin2_animation[0:]= hit_goblin
    temps2=time()
    if temps2-temps >1:
        sounds.sword_hit.play()
        temps = temps2
        goblin2_hit_counter -= 1

fly1_hit_counter = 3
def fly1_death():
    global fly1_hit_counter
    global temps
    fly1_animation[0:]= hit_fly
    temps2=time()
    if temps2-temps >1:
        sounds.sword_hit.play()
        temps = temps2
        fly1_hit_counter -= 1

def reset_normal():
    global coeurs
    global cooldown_attack_tracker
    global goblin1_hit_counter
    global goblin2_hit_counter
    global fly1_hit_counter
    global game_over
    global actual_level
    joueur1.x = 200
    joueur1.bottom = sol.y + 1
    goblin1.x = 600
    goblin1.bottom = sol.y + 1
    goblin2.x = 1200
    goblin2.bottom = sol.y + 1
    fly1.x = 1400
    mur1.x = 2560
    mur2.x = 0
    actual_level = 0
    coeurs = 3
    cooldown_attack_tracker = 0
    goblin1_hit_counter = 3
    goblin2_hit_counter = 3
    fly1_hit_counter = 3
    carte.topleft = 0,0
    music.play(musics[actual_level])

def game_over_screen():
    global running
    running = False

def win_screen():
    global running
    running = False

def draw():
    global actual_level
    global game_over
    global menu
    screen.clear()
    nom_du_jeu = pygame.display.set_caption('Platformer Battle Royal')
    if game_over == False and win == False:
        carte.draw()
        goblin1.draw()
        goblin2.draw()
        fly1.draw()
        joueur1.draw()
        mur1.draw()
        mur2.draw()
    if coeurs >= 1 and (game_over == False and win == False):
        coeur1.draw()
    if coeurs >= 2 and (game_over == False and win == False):
        coeur2.draw()
    if coeurs >= 3 and (game_over == False and win == False):
        coeur3.draw()


    #dessiner les contoures des rects
    #screen.draw.rect(sol, ROUGE)
    #screen.draw.rect(sol1, ROUGE)
    #screen.draw.rect(sol2, ROUGE)
    #screen.draw.rect(sol3, ROUGE)
    #screen.draw.rect(sol4, ROUGE)
    #screen.draw.rect(sol5, ROUGE)
    #screen.draw.rect(sol6, ROUGE)
    #screen.draw.rect(ciel, ROUGE)
    #screen.draw.rect(cube1, ROUGE)
    #screen.draw.rect(cube2, ROUGE)
    #screen.draw.rect(cube3, ROUGE)
    #screen.draw.rect(cube4, ROUGE)
    #screen.draw.rect(cube5, ROUGE)
    #screen.draw.rect(cube6, ROUGE)
    #screen.draw.rect(cube7, ROUGE)
    #screen.draw.rect(cube8, ROUGE)
    #screen.draw.rect(cube9, ROUGE)
    #screen.draw.rect(cube10, ROUGE)
    #screen.draw.rect(cube11, ROUGE)
    #screen.draw.rect(platform1, ROUGE)
    #screen.draw.rect(platform2, ROUGE)
    #screen.draw.rect(platform3,ROUGE)
    #screen.draw.rect(platform4,ROUGE)
    #screen.draw.rect(platform5,ROUGE)
    #screen.draw.rect(platform6,ROUGE)
    #screen.draw.rect(platform7,ROUGE)
    #screen.draw.rect(platform8,ROUGE)
    #screen.draw.rect(platform9,ROUGE)




    if menu == True:
        menu_image.draw()
        screen.draw.text("PLATFORMER BATTLE ROYALE", center=(WIDTH / 2, HEIGHT /4), fontsize=80, color="black", fontname="ff_police")
        screen.draw.text("USE THE JOYSTICK OR ARROWS TO MOVE", center=(WIDTH / 2, HEIGHT /2), fontsize=30, color="black", fontname="ff_police")
        screen.draw.text("PRESS THE BUTTON OR SPACE TO ATTACK", center=(WIDTH / 2, HEIGHT *5/8), fontsize=30, color="black", fontname="ff_police")
        screen.draw.text("PRESS THE JOYSTICK OR ENTER TO BEGIN", center=(WIDTH / 2, HEIGHT * 3/4), fontsize=30, color="black", fontname="ff_police")
        screen.draw.text("MADE BY ILYES ROUIBI", bottomright=(1008,624), fontsize=25, color="black", fontname="ff_police")

    if game_over == True:
        game_over_image.draw()
        screen.draw.text("YOU LOST ALL YOUR LIVES", center=(WIDTH / 2, HEIGHT /2), fontsize=30, color="red", fontname="ff_police")
        screen.draw.text("TRY AGAIN", center=(WIDTH / 2, HEIGHT *5/8), fontsize=30, color="red", fontname="ff_police")
        screen.draw.text("PRESS THE JOYSTICK OR ENTER TO RETURN TO MAIN MENU", center=(WIDTH / 2, HEIGHT * 3/4), fontsize=30, color="red", fontname="ff_police")

    if win == True:
        victory_image.draw()
        screen.draw.text("WELL DONE", center=(WIDTH / 2, HEIGHT /2), fontsize=30, fontname="ff_police")
        screen.draw.text("YOU BEAT THEM ALL", center=(WIDTH / 2, HEIGHT *5/8), fontsize=30, fontname="ff_police")
        screen.draw.text("PRESS THE JOYSTICK OR ENTER TO RETURN TO MAIN MENU", center=(WIDTH / 2, HEIGHT * 3/4), fontsize=30, fontname="ff_police")

    if actual_level == 1 and abs(joueur1.left-carte.left) < 2576:
        screen.draw.text("LEVEL ONE COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")
    if actual_level == 2 and abs(joueur1.left-carte.left) < 5968:
        screen.draw.text("LEVEL TWO COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")
    if actual_level == 3 and abs(joueur1.left-carte.left) < 9168:
        screen.draw.text("LEVEL THREE COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")
    if actual_level == 4 and abs(joueur1.left-carte.left) < 10128:
        screen.draw.text("LEVEL FOUR COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")
    if actual_level == 5 and abs(joueur1.left-carte.left) < 12432:
        screen.draw.text("LEVEL FIVE COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")
    if actual_level == 6 and abs(joueur1.left-carte.left) < 13840:
        screen.draw.text("LEVEL SIX COMPLETED", center=(WIDTH / 2, HEIGHT / 4), fontsize=60, color="purple",fontname="ff_police")

jumping = False
def update():
    global game_over
    global running
    global can_jump
    global goblin1_moving
    global goblin2_moving
    global fly1_moving
    global au_sol
    global a_droite
    global a_gauche
    global attacking
    global coeurs
    global goblin1_hit_counter
    global goblin2_hit_counter
    global fly1_hit_counter
    global win
    global actual_level
    global menu



    if running == True:

        if joueur1.right > mur2.left and joueur1.left < mur2.left -30:
            music.play(musics[actual_level])

        if game_over == True:
            game_over_screen()

        if win == True:
            win_screen()

    #pour le cooldown
        clock.tick(60)
    #pour que les rects se déplacent avec la carte
        sol.left = carte.left
        sol1.left = carte.left + 4226
        sol2.left = carte.left + 5312
        sol3.left = carte.left + 8900
        sol4.left = carte.left + 11394
        sol5.left = carte.left + 13010
        sol6.left = carte.left + 12732
        ciel.left = carte.left
        cube1.left = carte.left + 1344 + 16
        cube2.left = carte.left + 1408 + 16
        cube3.left = carte.left + 1472 + 16
        cube4.left = carte.left + 1632 - 16
        cube5.left = carte.left + 1792 - 16
        cube6.left = carte.left + 1856 - 16
        cube7.left = carte.left + 4930
        cube8.left = carte.left + 5375
        cube9.left = carte.left + 4994
        cube10.left = carte.left + 5442
        cube11.left = carte.left + 5184

        platform1.left = carte. left + 3073
        platform2.left = carte. left + 3460
        platform3.left = carte. left + 3840
        platform4.left = carte. left + 10752
        platform5.left = carte. left + 11074
        platform6.left = carte. left + 11968
        platform7.left = carte. left + 13184
        platform8.left = carte. left + 13570
        platform9.left = carte. left + 13952

        if actual_level == 0:
            mur1.left = carte.left + 2560

        if actual_level == 1:
            mur1.left = carte.left + 5952

        if actual_level == 2:
            mur1.left = carte.left + 9152

        if actual_level == 3:
            mur1.left = carte.left + 10112

        if actual_level == 4:
            mur1.left = carte.left + 12416

        if actual_level == 5:
            mur1.left = carte.left + 13824

        if actual_level == 6:
            mur1.left = carte.left + 15360


        if actual_level == 0:
            mur2.left = carte.left + 0

        if actual_level == 1:
            mur2.left = carte.left + 2560

        if actual_level == 2:
            mur2.left = carte.left + 5952

        if actual_level == 3:
            mur2.left = carte.left + 9152

        if actual_level == 4:
            mur2.left = carte.left + 10112

        if actual_level == 5:
            mur2.left = carte.left + 12416

        if actual_level == 6:
            mur2.left = carte.left + 13824


    #pour tuer le goblin1, on le touche 3 fois
        if joueur1.colliderect(goblin1) == True and attacking == True:
            goblin1_death()
            goblin1.animate()

    #pour tuer le goblin2, on le touche 3 fois
        if joueur1.colliderect(goblin2) == True and attacking == True:
            goblin2_death()
            goblin2.animate()

    #pour tuer le fly1, on le touche 3 fois
        if joueur1.colliderect(fly1) == True and attacking == True:
            fly1_death()
            fly1.animate()

    #mouvement du goblin1
        if goblin1_moving == True:
            goblin1_right(4)
            goblin1.animate()

        if goblin1_moving == False:
            goblin1_left(4)
            goblin1.animate()

        if abs(carte.left - goblin1.left)<1500:
            goblin1_move1()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left)<1500:
            goblin1_hit_counter +=5
            goblin1.left = carte.left + 5000


        if abs(carte.left - goblin1.left) > 3500 and abs(carte.left - goblin1.left)< 6500:
            goblin1_move2()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 3500 and abs(carte.left - goblin1.left)< 6500 :
            goblin1_hit_counter +=7
            goblin1.left = carte.left + 7000

        if abs(carte.left - goblin1.left) > 6500 and abs(carte.left - goblin1.left)< 7600:
            goblin1_move3()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 6500 and abs(carte.left - goblin1.left)< 7600 :
            goblin1_hit_counter +=7
            goblin1.left = carte.left + 9500

            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - goblin1.left) > 7600 and abs(carte.left - goblin1.left)< 10100:
            goblin1_move4()


        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 7600 and abs(carte.left - goblin1.left)< 10100:
            goblin1_hit_counter +=9
            goblin1.left = carte.left + 11100
            goblin1.bottom = 320

        if abs(carte.left - goblin1.left) > 10100 and abs(carte.left - goblin1.left)< 11300:
            goblin1_move5()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 10100 and abs(carte.left - goblin1.left)< 11300:
            goblin1_hit_counter +=10
            goblin1.left = carte.left + 12800
            goblin1.bottom = 576

        if abs(carte.left - goblin1.left) > 11300 and abs(carte.left - goblin1.left)< 13000:
            goblin1_move6()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 11300 and abs(carte.left - goblin1.left)< 13000:
            goblin1_hit_counter +=12
            goblin1.left = carte.left + 14000
            goblin1.bottom = 320
            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - goblin1.left) > 13000 and abs(carte.left - goblin1.left)< 14200:
            goblin1_move7()

        if goblin1_hit_counter == 0 and abs(carte.left - goblin1.left) > 13000 and abs(carte.left - goblin1.left)< 14200:
            goblin1.left = carte.left + 20000

        if abs(carte.left - goblin1.left) > 18000:
            goblin1.left = carte.left + 20000
    #mouvement du goblin2
        if goblin2_moving == True:
            goblin2_right(4)
            goblin2.animate()

        if goblin2_moving == False:
            goblin2_left(4)
            goblin2.animate()

        if abs(carte.left - goblin2.left)<1500:
            goblin2_move1()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left)<1500:
            goblin2_hit_counter +=5
            goblin2.left = carte.left + 5000

        if abs(carte.left - goblin2.left) > 3500 and abs(carte.left - goblin2.left)< 6500:
            goblin2_move2()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 3500 and abs(carte.left - goblin2.left)< 6500:
            goblin2_hit_counter +=7
            goblin2.left = carte.left + 8100
            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - goblin2.left) > 6500 and abs(carte.left - goblin2.left)< 8400:
            goblin2_move3()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 6500 and abs(carte.left - goblin2.left)< 8400:
            goblin2_hit_counter +=7
            goblin2.left = carte.left + 9500

        if abs(carte.left - goblin2.left) > 8400 and abs(carte.left - goblin2.left)< 10100:
            goblin2_move4()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 8400 and abs(carte.left - goblin2.left)< 10100:
            goblin2_hit_counter +=9
            goblin2.left = carte.left + 12000

        if abs(carte.left - goblin2.left) > 10100 and abs(carte.left - goblin2.left)< 12300:
            goblin2_move5()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 10100 and abs(carte.left - goblin2.left)< 12300:
            goblin2_hit_counter +=10
            goblin2.left = carte.left + 13600
            goblin2.bottom = 256

            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - goblin2.left) > 12300 and abs(carte.left - goblin2.left)< 13800:
            goblin2_move6()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 12300 and abs(carte.left - goblin2.left)< 13800:
            goblin2_hit_counter +=12
            goblin2.left = carte.left + 15000
            goblin2.bottom = 512

        if abs(carte.left - goblin2.left) > 13800 and abs(carte.left - goblin2.left)< 15100:
            goblin2_move7()

        if goblin2_hit_counter == 0 and abs(carte.left - goblin2.left) > 13800 and abs(carte.left - goblin2.left)< 15100:
            goblin2.left = carte.left + 20000

        if abs(carte.left - goblin2.left) > 18000:
            goblin2.left = carte.left + 20000

        #mouvement du fly1
        if fly1_moving == True:
            fly1_right(4)
            fly1.animate()

        if fly1_moving == False:
            fly1_left(4)
            fly1.animate()

        if abs(carte.left - fly1.left)<2200:
            fly1_move1()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left)<2200:
            fly1_hit_counter +=3
            fly1.left = carte.left + 5000

        if abs(carte.left - fly1.left) > 3500 and abs(carte.left - fly1.left)< 6500:
            fly1_move2()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 3500 and abs(carte.left - fly1.left)< 6500:
            fly1_hit_counter +=4
            fly1.left = carte.left + 8100

        if abs(carte.left - fly1.left) > 6500 and abs(carte.left - fly1.left)< 9100:
            fly1_move3()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 6500 and abs(carte.left - fly1.left)< 9100:
            fly1_hit_counter +=5
            fly1.left = carte.left + 9500
            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - fly1.left) > 9100 and abs(carte.left - fly1.left)< 10100:
            fly1_move4()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 9100 and abs(carte.left - fly1.left)< 10100:
            fly1_hit_counter +=6
            fly1.left = carte.left + 11000

        if abs(carte.left - fly1.left) > 10100 and abs(carte.left - fly1.left)< 11500:
            fly1_move5()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 10100 and abs(carte.left - fly1.left)< 11500:
            fly1_hit_counter +=7
            fly1.left = carte.left + 12900
            #redonner un coeur
            if coeurs<3:
                coeurs += 1

        if abs(carte.left - fly1.left) > 11500 and abs(carte.left - fly1.left)< 13500:
            fly1_move6()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 11500 and abs(carte.left - fly1.left)< 13500:
            fly1_hit_counter +=8
            fly1.left = carte.left + 14100

        if abs(carte.left - fly1.left) > 13500 and abs(carte.left - fly1.left)< 14500:
            fly1_move7()

        if fly1_hit_counter == 0 and abs(carte.left - fly1.left) > 13500 and abs(carte.left - fly1.left)< 14500:
            fly1.left = carte.left + 20000

        if abs(carte.left - fly1.left) > 18000:
            fly1.left = carte.left + 20000

    #pour passer les "niveaux"
        if abs(carte.left - fly1.left) > 2600 and abs(carte.left - fly1.left) < 6000 and abs(carte.left - goblin1.left) > 2600 and abs(carte.left - goblin1.left) < 6000 and abs(carte.left - goblin2.left) > 2600 and abs(carte.left - goblin2.left) < 6000:
            actual_level =1
        if abs(carte.left - fly1.left) > 6000 and abs(carte.left - fly1.left) < 9200 and abs(carte.left - goblin1.left) > 6000 and abs(carte.left - goblin1.left) < 9200 and abs(carte.left - goblin2.left) > 6000 and abs(carte.left - goblin2.left) < 9200:
            actual_level =2
        if abs(carte.left - fly1.left) > 9200 and abs(carte.left - fly1.left) < 10160 and abs(carte.left - goblin1.left) > 9200 and abs(carte.left - goblin1.left) < 10160 and abs(carte.left - goblin2.left) > 9200 and abs(carte.left - goblin2.left) < 10160:
            actual_level =3
        if abs(carte.left - fly1.left) > 10160 and abs(carte.left - fly1.left) < 12480 and abs(carte.left - goblin1.left) > 10160 and abs(carte.left - goblin1.left) < 12480 and abs(carte.left - goblin2.left) > 10160 and abs(carte.left - goblin2.left) < 12480:
            actual_level =4
        if abs(carte.left - fly1.left) > 12480 and abs(carte.left - fly1.left) < 13840 and abs(carte.left - goblin1.left) > 12480 and abs(carte.left - goblin1.left) < 13840 and abs(carte.left - goblin2.left) > 12480 and abs(carte.left - goblin2.left) < 13840:
            actual_level =5
        if abs(carte.left - fly1.left) > 13840 and abs(carte.left - fly1.left) < 15360 and abs(carte.left - goblin1.left) > 13840 and abs(carte.left - goblin1.left) < 15360 and abs(carte.left - goblin2.left) > 13840 and abs(carte.left - goblin2.left) < 15360:
            actual_level =6
        if abs(carte.left - fly1.left) > 18000 and abs(carte.left - goblin1.left) > 18000 and abs(carte.left - goblin2.left) > 18000:
            actual_level =7
    #pour gagner

        if actual_level == 7:
            win = True
            music.play(musics[8])
            actual_level = 8

    #pour pas etre gliché
        if joueur1.bottom > sol.y and joueur1.colliderect(sol) == True:
            joueur1.bottom = sol.y + 1
        if joueur1.bottom > sol1.y and joueur1.colliderect(sol1) == True:
            joueur1.bottom = sol1.y + 1
        if joueur1.bottom > sol2.y and joueur1.colliderect(sol2) == True:
            joueur1.bottom = sol2.y + 1
        if joueur1.bottom > sol3.y and joueur1.colliderect(sol3) == True:
            joueur1.bottom = sol3.y + 1
        if joueur1.bottom > sol4.y and joueur1.colliderect(sol4) == True:
            joueur1.bottom = sol4.y + 1
        if joueur1.bottom > sol5.y and joueur1.colliderect(sol5) == True:
            joueur1.bottom = sol5.y + 1
        if joueur1.bottom > sol6.y and joueur1.colliderect(sol6) == True:
            joueur1.bottom = sol6.y + 1
        if joueur1.bottom > cube1.y and joueur1.colliderect(cube1) == True:
            joueur1.bottom = cube1.y + 1
        if joueur1.bottom > cube2.y and joueur1.colliderect(cube2) == True:
            joueur1.bottom = cube2.y + 1
        if joueur1.bottom > cube3.y and joueur1.colliderect(cube3) == True:
            joueur1.bottom = cube3.y + 1
        if joueur1.bottom > cube4.y and joueur1.colliderect(cube4) == True:
            joueur1.bottom = cube4.y + 1
        if joueur1.bottom > cube5.y and joueur1.colliderect(cube5) == True:
            joueur1.bottom = cube5.y + 1
        if joueur1.bottom > cube6.y and joueur1.colliderect(cube6)== True:
            joueur1.bottom = cube6.y + 1
        if joueur1.bottom > cube7.y and joueur1.colliderect(cube7)== True:
            joueur1.bottom = cube7.y + 1
        if joueur1.bottom > cube8.y and joueur1.colliderect(cube8)== True:
            joueur1.bottom = cube8.y + 1
        if joueur1.bottom > cube9.y and joueur1.colliderect(cube9)== True:
            joueur1.bottom = cube9.y + 1
        if joueur1.bottom > cube10.y and joueur1.colliderect(cube10)== True:
            joueur1.bottom = cube10.y + 1
        if joueur1.bottom > cube11.y and joueur1.colliderect(cube11)== True:
            joueur1.bottom = cube11.y + 1
        if joueur1.bottom > platform1.y and joueur1.colliderect(platform1)== True:
            joueur1.bottom = platform1.y + 1
        if joueur1.bottom > platform2.y and joueur1.colliderect(platform2)== True:
            joueur1.bottom = platform2.y + 1
        if joueur1.bottom > platform3.y and joueur1.colliderect(platform3)== True:
            joueur1.bottom = platform3.y + 1
        if joueur1.bottom > platform4.y and joueur1.colliderect(platform4)== True:
            joueur1.bottom = platform4.y + 1
        if joueur1.bottom > platform5.y and joueur1.colliderect(platform5)== True:
            joueur1.bottom = platform5.y + 1
        if joueur1.bottom > platform6.y and joueur1.colliderect(platform6)== True:
            joueur1.bottom = platform6.y + 1
        if joueur1.bottom > platform7.y and joueur1.colliderect(platform7)== True:
            joueur1.bottom = platform7.y + 1
        if joueur1.bottom > platform8.y and joueur1.colliderect(platform8)== True:
            joueur1.bottom = platform8.y + 1
        if joueur1.bottom > platform9.y and joueur1.colliderect(platform9)== True:
            joueur1.bottom = platform9.y + 1
    #animation d'attack
        if keyboard.space == False:
            cooldown_attack_inverser()

        if cooldown_attack_tracker > 400 or cooldown_attack_tracker ==0:
            attacking = False

        if keyboard.space == True and cooldown_attack_tracker <= 400:
            attacking = True
            attack()
            joueur1.animate()

    #que faire si on touche le goblin1
        if joueur1.colliderect(goblin1) == True and attacking == False:
            joueur1_hit()
            joueur1.animate()

    #que faire si on touche le goblin2
        if joueur1.colliderect(goblin2) == True and attacking == False:
            joueur1_hit()
            joueur1.animate()

    #que faire si on touche le fly1
        if joueur1.colliderect(fly1) == True and attacking == False:
            joueur1_hit()
            joueur1.animate()

    #que faire si on tombe
        if joueur1.y > 700:
            coeurs = 0



    #si on touche le goblin 3 fois, on meurt
        if coeurs <= 0:
            game_over = True
            music.play(musics[7])
            coeurs = 3


    #animation de base
        if keyboard.up == False and keyboard.left == False and keyboard.right == False and au_sol == True:
            joueur1_base()
            joueur1.animate()


    #si on appuie sur up et que c'est possible de sauter, il appelle la fonction jump
        if keyboard.up and can_jump == True:
            jump(30)

    #si on touche le ciel, il peut plus sauter et redescent
        if joueur1.colliderect(ciel) == True:
            can_jump = False
    #si on touche un autre rect après avoir toucher le ciel ou après avoir lacher la touche up, on pourra re sauter
        if au_sol == True:
            can_jump = True

        if au_sol == False and keyboard.up == False:
            can_jump = False



    #si on peut pas sauter, change d'animation
        if can_jump == False:
            joueur1_animation[0:]= vol
            joueur1.animate()


    #savoir si on touche le sol ou pas
        if joueur1.colliderect(sol) == True or joueur1.colliderect(sol1) == True or joueur1.colliderect(sol2) == True or joueur1.colliderect(sol3) == True or joueur1.colliderect(sol4) == True or joueur1.colliderect(sol5) == True or joueur1.colliderect(sol6) == True or joueur1.colliderect(cube1) == True or joueur1.colliderect(cube2) == True or joueur1.colliderect(cube3) == True or joueur1.colliderect(cube4) == True or joueur1.colliderect(cube5) == True or joueur1.colliderect(cube6) == True or joueur1.colliderect(cube7) == True or joueur1.colliderect(cube8) == True or joueur1.colliderect(cube9) == True or joueur1.colliderect(cube10) == True or joueur1.colliderect(cube11) == True or joueur1.colliderect(platform1) == True or joueur1.colliderect(platform2)==True or joueur1.colliderect(platform3) == True or joueur1.colliderect(platform4) == True or joueur1.colliderect(platform5) == True or joueur1.colliderect(platform6) == True or joueur1.colliderect(platform7) == True or joueur1.colliderect(platform8) == True or joueur1.colliderect(platform9) == True:
            au_sol= True

    #si on touche rien, on tombe
        if joueur1.colliderect(sol) == False and joueur1.colliderect(sol1) == False and joueur1.colliderect(sol2) == False and joueur1.colliderect(sol3) == False and joueur1.colliderect(sol4) == False and joueur1.colliderect(sol5) == False and joueur1.colliderect(sol6) == False and joueur1.colliderect(cube1) == False and joueur1.colliderect(cube2) == False and joueur1.colliderect(cube3) == False and joueur1.colliderect(cube4) == False and joueur1.colliderect(cube5) == False and joueur1.colliderect(cube6) == False and joueur1.colliderect(cube7) == False and joueur1.colliderect(cube8) == False and joueur1.colliderect(cube9) == False and joueur1.colliderect(cube10) == False and joueur1.colliderect(cube11) == False and joueur1.colliderect(platform1) == False and  joueur1.colliderect(platform2) == False and joueur1.colliderect(platform3) == False and joueur1.colliderect(platform4) == False and joueur1.colliderect(platform5) == False and joueur1.colliderect(platform6) == False and joueur1.colliderect(platform7) == False and joueur1.colliderect(platform8) == False and joueur1.colliderect(platform9) == False:
            au_sol = False
            fall(15)

    #si on touche la touche right et que le perso est en x > 500, c'est la map qui bouge et pas lui. Sinon, il se déplace lui mais sans la carte
        if keyboard.right:

            joueur1.animate()

            if joueur1.x >= 500 and carte.right >=1030 and a_droite == True:
                #pour déplacer les mobs avec la map
                goblin1.left = goblin1.left - map_speed
                goblin2.left = goblin2.left - map_speed
                fly1.left = fly1.left - map_speed
                carte.left = carte.left - map_speed
                joueur1_animation[0:]= course

            if joueur1.x <= 500 and a_droite == True:
                right(7)

            if joueur1.x >=500 and joueur1.x <= 874 and carte.right <=1030:
                right(7)

        if joueur1.colliderect(mur1) == True:
            a_droite = False

        if joueur1.colliderect(mur1) == False:
            a_droite = True


        if keyboard.left:


            joueur1.animate()

            if joueur1.x <= 200 and carte.left <=-10 and a_gauche == True:
                #pour déplacer les mobs avec la map
                goblin1.left = goblin1.left + map_speed
                goblin2.left = goblin2.left + map_speed
                fly1.left = fly1.left + map_speed

                carte.left = carte.left + map_speed
                joueur1_animation[0:]= course


            if joueur1.x >= 200 and a_gauche == True:
                left(7)

        if joueur1.colliderect(mur2)== True:
            a_gauche = False

        if joueur1.colliderect(mur2)== False:
            a_gauche = True


#mouvement des mobs
def goblin1_move1():
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=300:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=850:
        goblin1_moving = False

def goblin1_move2():
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=4300:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=4800:
        goblin1_moving = False

def goblin1_move3():
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=6800:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=7500:
        goblin1_moving = False

def goblin1_move4():
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=9408:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=10048:
        goblin1_moving = False

def goblin1_move5():    #changer le y
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=11072:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=11200:
        goblin1_moving = False

def goblin1_move6():    #changer le y
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=12736:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=12950:
        goblin1_moving = False

def goblin1_move7():    #changer le y
    global goblin1_moving
    if abs(carte.left - goblin1.left)<=13952:
        goblin1_moving = True
    if abs(carte.left - goblin1.left)>=14100:
        goblin1_moving = False

def goblin2_move1():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=700:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=1300:
        goblin2_moving = False

def goblin2_move2():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=4300:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=4800:
        goblin2_moving = False

def goblin2_move3():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=8000:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=8300:
        goblin2_moving = False

def goblin2_move4():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=9408:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=10048:
        goblin2_moving = False

def goblin2_move5():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=11968:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=12288:
        goblin2_moving = False

def goblin2_move6():       #changer le y
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=13568:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=13700:
        goblin2_moving = False

def goblin2_move7():
    global goblin2_moving
    if abs(carte.left - goblin2.left)<=14528:
        goblin2_moving = True
    if abs(carte.left - goblin2.left)>=15040:
        goblin2_moving = False

def fly1_move1():
    global fly1_moving
    if abs(carte.left - fly1.left)<=1334:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=2000:
        fly1_moving = False

def fly1_move2():
    global fly1_moving
    if abs(carte.left - fly1.left)<=4860:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=5632:
        fly1_moving = False

def fly1_move3():
    global fly1_moving
    if abs(carte.left - fly1.left)<=8576:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=9024:
        fly1_moving = False

def fly1_move4():
    global fly1_moving
    if abs(carte.left - fly1.left)<=9408:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=10048:
        fly1_moving = False

def fly1_move5():
    global fly1_moving
    if abs(carte.left - fly1.left)<=10560:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=11392:
        fly1_moving = False

def fly1_move6():
    global fly1_moving
    if abs(carte.left - fly1.left)<=12864:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=13440:
        fly1_moving = False

def fly1_move7():
    global fly1_moving
    if abs(carte.left - fly1.left)<=14080:
        fly1_moving = True
    if abs(carte.left - fly1.left)>=14400:
        fly1_moving = False

#s'il lache la touche up, il tombe
def on_key_up(key):
    global can_jump
    global menu
    global running
    global game_over
    global win

    #pour passer au menu quand on lache la touche entrée
    if key == keys.RETURN and (game_over == True or win == True):
        game_over = False
        win = False
        menu = True
        music.play(musics[9])

def on_key_down(key):
    #pour passer au menu quand on presse la touche entrée
    global menu
    global running
    if key == keys.RETURN:
        if menu == True:
            running = True
            menu = False
            reset_normal()



pgzrun.go()
