import pygame
from assets import (spritesheet, art_assets, sound_assets)
import random
"""
This is the main code for Gnome: Makizushi by LHermannCoding. Credit to Clear 
Code and Coding with Russ for their helpful YouTube tutorials on masks, game 
state management, and more.

"""
# Macro Constants:
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
BG_COLOR_TUTORIAL = (175, 111, 149)
BG_COLOR_MAIN = (143, 103, 75)
BLACK = (0,0,0)
BROWN = (46, 32, 6)
font_small, font_medium, font_large = 27, 36, 48

# Game Constants:
origin = (0,0)
title_gnome_x, title_gnome_y = 880, 135
title_gnome_arrival_pos = 580
title_gnome_exit_pos_1 = -60
title_gnome_exit_pos_2 = -360
gnome_start_x, gnome_start_y = 440, 220
gnome_counter_x, gnome_counter_y = 697, 234
start_pos = (350, 315)
nori_pos = (600, 358)
rice_pos = (285, 460)
crab_pos = (306, 335)
shrimp_pos = (45,-20)
tamago_pos = (280,-20)
tuna_pos = (120,170)
salmon_pos = (776,455)
unagi_pos = (90,310)
plate_pos = (516,544)
trashcan_pos = (883,310)
counter_pos = (572,127)
counter_offset = (572,147)
coins_pos = (824,649)
gnome_placard_pos = (646,616)
placard_profile_pos = (640,619)
win_pos = (188, 440)
again_pos = (100, 510)
plate_max = 3
arrival_pos_customer = 25
arrival_pos_placard = 616
departure_pos_customer = -90
departure_pos_placard = 800
min_customers = 2
max_customers = 4
min_overlap = 0
max_overlap = 2
ending_profit = 200
max_profit = 900
RAND_CYCLE = 400

# Tutorial-Specific Constants
tutorial_placard_x, tutorial_placard_y = 0, -438
tut_placard_arrive_pos = 0
tut_placard_exit_pos = -600
tut_1_gnome_pos = (620,450)
tut_2_gnome_pos = (720,282)
tut_3_gnome_pos = (448,450)
tut_4_gnome_pos = (688,448)
tut_5_gnome_pos = (690,200)
tut_1_arrow_pos = (577,480)
tut_2_arrow_pos = (726,382)
tut_3_arrow_pos = (395,474)
tut_4_arrow_pos = (780,474)
tut_5_arrow_pos_1 = (620,222)
tut_5_arrow_pos_2 = (800,222)
green_arrow_pos = (190, 630)
tut_msg1_pos = (57,116)
tut_msg2_pos = (57,176)
tut_msg3_pos = (57,236)
tut_msg4_pos = (57,296)
stage_plate = 1
stage_nori = 2
stage_rice = 3
stage_protein = 4
stage_serve = 5

# Dynamic Constants:
animation_timer = 0
win_animation_timer = 0
payment_max = 2500
customer_wait_start = 0 
customer_wait_end = 2520

class Gnome(pygame.sprite.Sprite):
    """
    Sprite class for the main character of the game.
    """
    def __init__(self):
        super().__init__()
        self.movex = 0
        self.movey = 0
        self.steps = 3
        self.previous_pos = (0,0)
        self.money = 0
        self.plate = None
        self.frame = 0
        self.images = []
        self.game_state = 'main_game'
        gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet.png").convert_alpha()
        gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)
        for x in range(0,4):
            self.images.append(gnome_sheet.get_image(x, 96, 96, BLACK, scale = 1))
        self.image = self.images[1]
        self.placard_profile = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def control(self, x, y):
        """
        Monitor how many groups of steps the sprite will take in each direction.
        """
        self.movex += x
        self.movey += y
        
    def update(self):     
        """
        Move gnome based on control function's input and monitor sprite
        collision detection.
        """   
        offset_x = origin[0] - gnomelius.rect.left
        offset_y = origin[1] - gnomelius.rect.top
        
        if self.game_state == 'tutorial':
            current_mask = tutorial_base_mask
        elif self.game_state == 'main_game':
            current_mask = kitchen_base_mask
        elif self.game_state == 'end_game':
            current_mask = end_base_mask
            
        if self.mask.overlap_area(current_mask, (offset_x,offset_y)) <= max_overlap:
            self.previous_pos = (self.rect.center) # Teleport to previous pos if max overlap achieved
        if self.mask.overlap_area(current_mask, (offset_x,offset_y)) > min_overlap:
            self.rect.center = self.previous_pos # Save previous pos upon any overlap
            
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        
        if self.game_state == "end_game":
            global win_animation_timer
            current = win_animation_timer // 15
            if current == 0:
                self.frame = 0
            elif current == 1:
                self.frame = 2
            elif current == 2:
                self.frame = 1
            elif current == 3:
                self.frame = 3
            win_animation_timer += 1
            if win_animation_timer >= 59:
                win_animation_timer = 0
        else:
            if self.movex < 0:
                self.frame = 2        
            if self.movex > 0:
                self.frame = 3        
            if self.movey < 0:
                self.frame = 0       
            if self.movey > 0:
                self.frame = 1
                
        self.image = self.images[self.frame]
        self.placard_profile = self.image
    
    def update_plate(self, action):
        """
        Update gnome spritesheet based on plate contents.
        """
        gnome_spritesheet = None
        if action == "pick_up" and self.plate != None:
            gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_plate.png").convert_alpha()
            self.plate = Plate()
        elif action == "add_nori" and len(self.plate.contains) == 0:
            gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_nori.png").convert_alpha()        
        elif action == "add_rice" and len(self.plate.contains) == 1:
            gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_rice.png").convert_alpha() 
        elif len(self.plate.contains) == 2: 
            if action == "add_tuna":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_tuna.png").convert_alpha() 
            elif action == "add_salmon":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_salmon.png").convert_alpha()
            elif action == "add_unagi":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_unagi.png").convert_alpha()
            elif action == "add_crab":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_crab.png").convert_alpha() 
            elif action == "add_shrimp":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_shrimp.png").convert_alpha() 
            elif action == "add_tamago":
                gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_tamago.png").convert_alpha() 
        elif action == "put_down":
            gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet.png").convert_alpha()
            self.plate = None
        elif action == "empty_items":
            gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet_plate.png").convert_alpha()
        if gnome_spritesheet != None:
            self.images = []
            gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)
            for x in range(0,4):
                self.images.append(gnome_sheet.get_image(x, 96, 96, BLACK, scale = 1))
            self.image = self.images[self.frame]

class Storage():
    """
    Class for the storage boxes that hold ingredients.
    """
    def __init__(self,type):
        self.type = type
        self.image = None
        if type == "unagi":
            self.image = pygame.image.load("assets/art_assets/storage/unagi_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = unagi_pos)
        elif type == "salmon":
            self.image = pygame.image.load("assets/art_assets/storage/salmon_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = salmon_pos)
        elif type == "crab":
            self.image = pygame.image.load("assets/art_assets/storage/crab_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = crab_pos)
        elif type == "shrimp":
            self.image = pygame.image.load("assets/art_assets/storage/shrimp_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = shrimp_pos)
        elif type == "tamago":
            self.image = pygame.image.load("assets/art_assets/storage/tamago_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = tamago_pos)
        elif type == "tuna":
            self.image = pygame.image.load("assets/art_assets/storage/tuna_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = tuna_pos)
        elif type == "rice":
            self.image = pygame.image.load("assets/art_assets/storage/rice_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = rice_pos)
        elif type == "nori":
            self.image = pygame.image.load("assets/art_assets/storage/nori_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = nori_pos)
        elif type == "plate":
            self.image = pygame.image.load("assets/art_assets/storage/plate_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = plate_pos)

class Plate():
    """
    Class for monitoring the ingredients (if any) that are currently on 
    the gnome's plate.
    """
    def __init__(self):
        self.contains = []

    def add_item(self,item):
        """
        Attempt to add items to plate (if possible).
        """
        if item == "nori" and len(self.contains) == 0:
            self.contains.append("nori")
        elif item == "rice" and len(self.contains) == 1:
            self.contains.append("rice")
        elif len(self.contains) == 2:
            if item == "tuna":
                self.contains.append("tuna")
            elif item == "salmon":
                self.contains.append("salmon")
            elif item == "unagi":
                self.contains.append("unagi")
            elif item == "crab":
                self.contains.append("crab")
            elif item == "shrimp":
                self.contains.append("shrimp")
            elif item == "tamago":
                self.contains.append("tamago")
    
class Customer():
    def __init__(self, id, line_pos, request):
        self.id = id
        self.line_pos = line_pos
        self.payment = 60
        self.payment_timer = payment_max
        self.wait_timer = customer_wait_start
        self.request = request
        self.timer_loc_x = 0
        self.timer_loc_y = 691
        if request == "tuna":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_tuna.png").convert_alpha()
        elif request == "salmon":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_salmon.png").convert_alpha()
        elif request == "unagi":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_unagi.png").convert_alpha()
        elif request == "crab":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_crab.png").convert_alpha()
        elif request == "shrimp":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_shrimp.png").convert_alpha()
        elif request == "tamago":
            placard_text = pygame.image.load("assets/art_assets/text/profile_text_tamago.png").convert_alpha()
        self.placard_text = placard_text
        
        if id == "horace":
            temp_sheet = pygame.image.load("assets/art_assets/customers/horace/spritesheet_horace.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/horace/horace_profile_timer.png").convert_alpha()
        elif id == "jeb":
            temp_sheet = pygame.image.load("assets/art_assets/customers/jeb/spritesheet_jeb.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/jeb/jeb_profile_timer.png").convert_alpha()
        elif id == "jordan":
            temp_sheet = pygame.image.load("assets/art_assets/customers/jordan/spritesheet_jordan.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/jordan/jordan_profile_timer.png").convert_alpha()
        elif id == "mickey":
            temp_sheet = pygame.image.load("assets/art_assets/customers/mickey/spritesheet_mickey.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/mickey/mickey_profile_timer.png").convert_alpha()
        elif id == "pickles":
            temp_sheet = pygame.image.load("assets/art_assets/customers/pickles/spritesheet_pickles.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/pickles/pickles_profile_timer.png").convert_alpha()
        elif id == "tom":
            temp_sheet = pygame.image.load("assets/art_assets/customers/tom/spritesheet_tom.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/tom/tom_profile_timer.png").convert_alpha()
        elif id == "stel":
            temp_sheet = pygame.image.load("assets/art_assets/customers/stel/spritesheet_stel.png").convert_alpha()
            placard_profile = pygame.image.load("assets/art_assets/customers/stel/stel_profile_timer.png").convert_alpha()
        self.placard_profile = placard_profile
        self.person_animation = []
        customer_spritesheet = spritesheet.SpriteSheet(temp_sheet)
        for x in range(0,2):
            self.person_animation.append(customer_spritesheet.get_image(x, 96, 96, BLACK, scale = 1))
        self.person = self.person_animation[1]
        
        # Math for figuring out blitting pos for customers in relativity to others in line.
        self.person_pos_x = (80 * line_pos) + 500
        self.person_pos_y = -205
        self.placard_pos_x = (160 * line_pos) - 154
        self.placard_pos_y = 1080
    
    def payment_calculation(self):
        """
        Calculate how much will be paid out for fulfillment or order based on 
        time spent waiting for dish.
        """
        self.payment = max(20, int(self.payment * (self.payment_timer / payment_max)))
    
    def update_timer(self):
        """
        Function regarding waittime for customers that updates internal clock
        and moves timer mark appropriately.
        """
        self.payment_timer -= 1
        self.wait_timer += 1
        self.timer_loc_x = ((self.line_pos - 1) * 160) + 17 + (self.wait_timer // 20)
        screen.blit(timer_mark, (self.timer_loc_x, self.timer_loc_y))
        

class Customer_Group():
    def __init__(self):
        self.attendance = {}
        self.arrival_order = []
        self.absent_names = ["horace", "jeb", "jordan", "mickey", "pickles", "tom", "stel"]
        self.sushi_options = ["salmon", "tuna", "unagi", "crab", "shrimp", "tamago"]
        self.owed_payment = 0
        
    def add_order(self, ingredient = None, customer = None):
        """
        Adds order to queue. Returns line position of added order (when
        there is enough space in line), and False otherwise.
        
        Note: blitting of order placard art asset done in game loop.
        """
        line_pos = 1
        while self.attendance.get(line_pos, -1) != -1:
            line_pos += 1
        if line_pos <= 4:
            if not ingredient:
                sushi_choice = random.choice(self.sushi_options)
            else:
                sushi_choice = ingredient
            if not customer:
                customer_name = random.choice(self.absent_names)
            else:
                customer_name = customer
            self.attendance[line_pos] = Customer(customer_name, line_pos, sushi_choice)
            self.arrival_order.append(line_pos)
            self.absent_names.remove(customer_name)
            return line_pos
        return False
    
    def fulfill_order(self,dish):
        """
        Fulfills order and removes it from queue. Returns line position of 
        fulfilled order if submitted, and False otherwise.
        
        Note: removal of person and placard art asset done in game loop.
        """
        for idx, pos in enumerate(self.arrival_order):
            if self.attendance.get(pos, -1) != -1:
                if self.attendance[pos].request == dish:
                    self.absent_names.append(self.attendance[pos].id)
                    self.attendance[pos].payment_calculation()
                    self.owed_payment += self.attendance[pos].payment
                    del self.arrival_order[idx]
                    return pos
        return False
        
class Level():
    """
    Class for containing and switching between the different game states 
    (title screen, core gameplay, help screen, etc.)
    """
    def __init__(self):
        self.state = 'title'
        self.swap_delay = False
        self.tutorial_stage = 0
        self.main_adding_in_pos = {1: False, 2: False, 3: False, 4: False}
        self.main_removing_in_pos = {1: False, 2: False, 3: False, 4: False}
        
    def title(self):
        """
        Game state for title screen.
        """     
        global animation_timer
        global title_gnome_x
        global title_gnome_y
        screen.blit(title_bg, origin)  
        begin = False
        if title_gnome_x >= title_gnome_arrival_pos:
            title_gnome_x -= 3
        elif animation_timer <= 150:
            animation_timer += 4
            
        if animation_timer >= 50:
            s = screen.blit(start_button, start_pos)
        g = screen.blit(title_gnome, (title_gnome_x, title_gnome_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                if animation_timer >= 100:
                    pos = pygame.mouse.get_pos()
                    if s.collidepoint(pos):
                        begin = True
                        break         
                    elif g.collidepoint(pos):
                        pygame.mixer.Sound.play(gnome_oop)
            # Gnome movement kept even in title screen to avoid input bug on keys when game state swaps.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, -gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, gnomelius.steps)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, -gnomelius.steps)
                if event.key == pygame.K_SPACE and animation_timer >= 100:
                    begin = True
        if begin:
            pygame.mouse.set_visible(False)
            position = customers.add_order("salmon", "jeb")
            self.main_adding_in_pos[position] = True
            gnomelius.game_state = "tutorial"
            self.state = "tutorial"
            pygame.mixer.music.load("assets/sound_assets/mii_channel.wav")
            pygame.mixer.music.play(-1)    
                    
        pygame.display.update()
         
    def tutorial(self):
        """
        Game state for tutorial screen.
        """
        global title_gnome_x
        global title_gnome_y
        global tutorial_placard_x
        global tutorial_placard_y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, -gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, gnomelius.steps)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, -gnomelius.steps)       
                elif event.key == pygame.K_SPACE:
                    complete = False
                    if pygame.Rect.colliderect(gnomelius.rect,plate_zone.rect) and self.tutorial_stage == stage_plate:
                        if not gnomelius.plate:
                            gnomelius.plate = Plate()
                            gnomelius.update_plate("pick_up")
                            self.tutorial_stage = stage_nori
                            complete = True
                    elif gnomelius.plate != None:
                        if pygame.Rect.colliderect(gnomelius.rect,nori_zone.rect) and self.tutorial_stage == stage_nori:
                            gnomelius.update_plate("add_nori")
                            gnomelius.plate.add_item("nori")
                            self.tutorial_stage = stage_rice
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,rice_zone.rect) and self.tutorial_stage == stage_rice:
                            gnomelius.update_plate("add_rice")
                            gnomelius.plate.add_item("rice")
                            self.tutorial_stage = stage_protein
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,salmon_zone.rect) and self.tutorial_stage == stage_protein:
                            gnomelius.update_plate("add_salmon")
                            gnomelius.plate.add_item("salmon")
                            self.tutorial_stage = stage_serve
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,counter_rect) and self.tutorial_stage == stage_serve:
                            removal = customers.fulfill_order(gnomelius.plate.contains[2])
                            if removal:
                                customers.attendance[removal].person = customers.attendance[removal].person_animation[0]
                                pygame.mixer.Sound.play(temp_serve)
                                pygame.mixer.music.load("assets/sound_assets/flyday_chinatown.wav")
                                pygame.mixer.music.play(-1)
                                gnomelius.money = min(gnomelius.money + customers.owed_payment, 999)
                                customers.owed_payment = 0 
                                self.main_removing_in_pos[removal] = True
                                gnomelius.game_state = "main_game"
                                self.state = "main_game"
                            gnomelius.update_plate("put_down")                        
                    if complete:
                        pygame.mixer.Sound.play(temp_ding)
                    else:
                        pygame.mixer.Sound.play(temp_reject)

            
        screen.fill(BG_COLOR_TUTORIAL)
        screen.blit(kitchen_base, origin)
        screen.blit(nori_zone.image, nori_pos)
        screen.blit(rice_zone.image, rice_pos)
        screen.blit(salmon_zone.image, salmon_pos)
        screen.blit(plate_zone.image, plate_pos)
        screen.blit(trashcan, trashcan_pos)
        screen.blit(counter, counter_pos)
        screen.blit(gnomelius.placard_profile, placard_profile_pos)
        screen.blit(gnome_placard, gnome_placard_pos)
        update_display_coins(gnomelius)
        
        for add_pos, add_bool in self.main_adding_in_pos.items():
            if add_bool == True:
                still_adding = 0
                if customers.attendance[add_pos].person_pos_y < arrival_pos_customer:
                    customers.attendance[add_pos].person_pos_y += 1
                else:
                    still_adding += 1
                if customers.attendance[add_pos].placard_pos_y > arrival_pos_placard:
                    customers.attendance[add_pos].placard_pos_y -= 2
                else:
                    still_adding += 1
                if still_adding == 2 or self.main_removing_in_pos[add_pos]:
                    self.main_adding_in_pos[add_pos] = False
        
        for customer in customers.attendance.values():
            customer.payment_timer -= 1
            screen.blit(customer.person, (customer.person_pos_x, customer.person_pos_y))
            screen.blit(customer.placard_profile, (customer.placard_pos_x, customer.placard_pos_y))
            screen.blit(customer.placard_text, (customer.placard_pos_x, customer.placard_pos_y))
            
        if tutorial_placard_y <= tut_placard_arrive_pos and title_gnome_x <= title_gnome_exit_pos_1:
            tutorial_placard_y += 8
        elif self.tutorial_stage == 0 and title_gnome_x <= title_gnome_exit_pos_2:
            self.tutorial_stage = 1
        screen.blit(tutorial_placard, (tutorial_placard_x, tutorial_placard_y))
        if self.tutorial_stage == stage_plate:
            add_tutorial_message("Welcome! Please begin", tut_msg1_pos)
            add_tutorial_message("by grabbing a plate.", tut_msg2_pos)
            add_tutorial_message("(use spacebar for actions)", tut_msg3_pos)
            screen.blit(tutorial_gnome,tut_1_gnome_pos)
            screen.blit(tutorial_arrow_1,tut_1_arrow_pos)
        elif self.tutorial_stage == stage_nori:
            add_tutorial_message("Nice! Next, please add a base", tut_msg1_pos)
            add_tutorial_message("of nori to your plate.", tut_msg2_pos)
            add_tutorial_message("(use spacebar for actions)", tut_msg3_pos)
            screen.blit(tutorial_gnome,tut_2_gnome_pos)
            screen.blit(tutorial_arrow_2,tut_2_arrow_pos)
        elif self.tutorial_stage == stage_rice:
            add_tutorial_message("Great! Now put some rice", tut_msg1_pos)
            add_tutorial_message("on top of your plated nori.", tut_msg2_pos)
            add_tutorial_message("(use spacebar for actions)", tut_msg3_pos)
            screen.blit(tutorial_gnome,tut_3_gnome_pos)
            screen.blit(tutorial_arrow_3,tut_3_arrow_pos)
        elif self.tutorial_stage == stage_protein:
            add_tutorial_message("Once you have a base of", tut_msg1_pos)
            add_tutorial_message("nori and rice, finish your", tut_msg2_pos)
            add_tutorial_message("dish with desired protein.", tut_msg3_pos)
            add_tutorial_message("(use spacebar for actions)", tut_msg4_pos)
            screen.blit(tutorial_gnome,tut_4_gnome_pos)
            screen.blit(tutorial_arrow_4,tut_4_arrow_pos)
            screen.blit(green_arrow, green_arrow_pos)
        elif self.tutorial_stage == stage_serve:
            add_tutorial_message("Excellent! You have finished", tut_msg1_pos)
            add_tutorial_message("the dish. Bring the plate to", tut_msg2_pos)
            add_tutorial_message("the counter and serve!", tut_msg3_pos)
            add_tutorial_message("(use spacebar for actions)", tut_msg4_pos)
            screen.blit(tutorial_gnome,tut_5_gnome_pos)
            screen.blit(tutorial_arrow_5,tut_5_arrow_pos_1)
            screen.blit(tutorial_arrow_5,tut_5_arrow_pos_2)
            screen.blit(green_arrow, green_arrow_pos)
        
        gnomelius.update()
        gnome_group.draw(screen)
        if title_gnome_x >= title_gnome_exit_pos_2:
            title_gnome_x -= 10
            screen.blit(title_gnome, (title_gnome_x,title_gnome_y))
        pygame.display.update()
        
    def main_game(self):
        """
        Game state for main game.
        """
        global tutorial_placard_x
        global tutorial_placard_y
        global ending_profit
        global customer_wait_end
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, -gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, gnomelius.steps)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, -gnomelius.steps)       
                elif event.key == pygame.K_SPACE:
                    complete = False
                    if pygame.Rect.colliderect(gnomelius.rect,plate_zone.rect):
                        if not gnomelius.plate:
                            gnomelius.plate = Plate()
                            gnomelius.update_plate("pick_up")
                            complete = True
                    elif gnomelius.plate != None:
                        if pygame.Rect.colliderect(gnomelius.rect,nori_zone.rect):
                            gnomelius.update_plate("add_nori")
                            gnomelius.plate.add_item("nori")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,rice_zone.rect):
                            gnomelius.update_plate("add_rice")
                            gnomelius.plate.add_item("rice")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,tuna_zone.rect):
                            gnomelius.update_plate("add_tuna")
                            gnomelius.plate.add_item("tuna")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,salmon_zone.rect):
                            gnomelius.update_plate("add_salmon")
                            gnomelius.plate.add_item("salmon")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,unagi_zone.rect):
                            gnomelius.update_plate("add_unagi")
                            gnomelius.plate.add_item("unagi")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,crab_zone.rect):
                            gnomelius.update_plate("add_crab")
                            gnomelius.plate.add_item("crab")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,shrimp_zone.rect):
                            gnomelius.update_plate("add_shrimp")
                            gnomelius.plate.add_item("shrimp")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,tamago_zone.rect):
                            gnomelius.update_plate("add_tamago")
                            gnomelius.plate.add_item("tamago")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,trashcan_rect):
                            gnomelius.update_plate("empty_items")
                            gnomelius.plate = Plate()
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,counter_rect):
                            if len(gnomelius.plate.contains) == plate_max:
                                removal = customers.fulfill_order(gnomelius.plate.contains[2])
                                if removal:
                                    customers.attendance[removal].person = customers.attendance[removal].person_animation[0]
                                    pygame.mixer.Sound.play(temp_serve)
                                    self.main_removing_in_pos[removal] = True 
                                    gnomelius.money = min(gnomelius.money + customers.owed_payment, ending_profit)
                                    customers.owed_payment = 0 
                                else:
                                    pygame.mixer.Sound.play(wrong_order)
                                gnomelius.update_plate("put_down")                        
                    if complete :
                        pygame.mixer.Sound.play(temp_ding)
                    else:
                        pygame.mixer.Sound.play(temp_reject)

        screen.fill(BG_COLOR_MAIN)
        screen.blit(kitchen_base, origin)
        screen.blit(nori_zone.image, nori_pos)
        screen.blit(rice_zone.image, rice_pos)
        screen.blit(tuna_zone.image, tuna_pos)
        screen.blit(salmon_zone.image, salmon_pos)
        screen.blit(unagi_zone.image, unagi_pos)
        screen.blit(crab_zone.image, crab_pos)
        screen.blit(shrimp_zone.image, shrimp_pos)
        screen.blit(tamago_zone.image, tamago_pos)
        screen.blit(plate_zone.image, plate_pos)
        screen.blit(trashcan, trashcan_pos)
        screen.blit(counter, counter_pos)
        screen.blit(gnomelius.placard_profile, placard_profile_pos)
        screen.blit(gnome_placard, gnome_placard_pos)
        update_display_coins(gnomelius)
         
        num_customers = len(customers.attendance)
        if num_customers < min_customers:
            position = customers.add_order()
            self.main_adding_in_pos[position] = True
        if num_customers < max_customers:
            temp_rand = random.randint(1, RAND_CYCLE)
            if temp_rand == RAND_CYCLE:
                position = customers.add_order()
                if position:
                    self.main_adding_in_pos[position] = True
            
        for add_pos, add_bool in self.main_adding_in_pos.items():
            if add_bool == True:
                still_adding = 0
                if customers.attendance[add_pos].person_pos_y < arrival_pos_customer:
                    customers.attendance[add_pos].person_pos_y += 1
                else:
                    still_adding += 1
                if customers.attendance[add_pos].placard_pos_y > arrival_pos_placard:
                    customers.attendance[add_pos].placard_pos_y -= 2
                else:
                    still_adding += 1
                if still_adding == 2 or self.main_removing_in_pos[add_pos]:
                    self.main_adding_in_pos[add_pos] = False
        for removal_pos, removal_bool in self.main_removing_in_pos.items():
            still_removing = 0
            if removal_bool:
                if customers.attendance[removal_pos].person_pos_y > departure_pos_customer:
                    customers.attendance[removal_pos].person_pos_y -= 1
                else:
                    still_removing += 1
                if customers.attendance[removal_pos].placard_pos_y < departure_pos_placard:
                    customers.attendance[removal_pos].placard_pos_y += 1
                else:
                    still_removing += 1
                if still_removing == 2:
                    self.main_removing_in_pos[removal_pos] = False
                    del customers.attendance[removal_pos]
        
        for customer in customers.attendance.values():
            screen.blit(customer.person, (customer.person_pos_x, customer.person_pos_y))
            screen.blit(customer.placard_profile, (customer.placard_pos_x, customer.placard_pos_y))
            screen.blit(customer.placard_text, (customer.placard_pos_x, customer.placard_pos_y))
            if customer.wait_timer < customer_wait_end and self.main_adding_in_pos[customer.line_pos] == False and self.main_removing_in_pos[customer.line_pos] == False:
                customer.update_timer()
            elif customer.wait_timer == customer_wait_end:
                customer.wait_timer += 1
                pygame.mixer.Sound.play(lost_order)
                leave = customers.fulfill_order(customer.request)
                customers.owed_payment = 0 
                customers.attendance[leave].person = customers.attendance[leave].person_animation[0]
                self.main_removing_in_pos[leave] = True 
        
        if tutorial_placard_y >= tut_placard_exit_pos:
            tutorial_placard_y -= 5
            screen.blit(tutorial_placard, (tutorial_placard_x, tutorial_placard_y))
            
        if gnomelius.money >= ending_profit:
            if ending_profit < max_profit:
                ending_profit += 100
            gnomelius.game_state = 'end_game'
            self.state = 'end_game'
            
        gnomelius.update()
        gnome_group.draw(screen) 
        pygame.display.update()
        
    def end_game(self):
        """
        Game state for end game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, -gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, gnomelius.steps)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gnomelius.control(gnomelius.steps, 0)
                elif event.key == pygame.K_RIGHT:
                    gnomelius.control(-gnomelius.steps, 0)
                elif event.key == pygame.K_UP:
                    gnomelius.control(0, gnomelius.steps)
                elif event.key == pygame.K_DOWN:
                    gnomelius.control(0, -gnomelius.steps)
                elif event.key == pygame.K_SPACE:
                    gnomelius.money = 0
                    gnomelius.rect.x = gnome_counter_x
                    gnomelius.rect.y = gnome_counter_y
                    gnomelius.game_state = "main_game"
                    self.state = "main_game"
                    
        screen.fill(BG_COLOR_MAIN)
        screen.blit(end_base, origin)
        screen.blit(gnomelius.placard_profile, placard_profile_pos)
        screen.blit(gnome_placard, gnome_placard_pos)
        update_display_coins(gnomelius)
        update_display_win(gnomelius)
        
        gnomelius.update()
        gnome_group.draw(screen)
        pygame.display.update()
        
    def level_manager(self):
        """
        Lead function for managing all game states.
        """
        if self.state == 'title':
            self.title()
        if self.state == 'tutorial':
            self.tutorial()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'end_game':
            self.end_game()

# Pygame setup basics:
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
level = Level()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('A Gnome Game')
pygame.mouse.set_visible(True)

# Art asset loading and rectangle creation.
gnome_spritesheet = pygame.image.load("assets/art_assets/gnome/gnomesheet.png").convert_alpha()
gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)
start_button = pygame.image.load("assets/art_assets/buttons/start.png").convert_alpha()
start_rect = start_button.get_rect(topleft = trashcan_pos)
title_bg = pygame.image.load("assets/art_assets/screens/title_background.png").convert_alpha()
title_gnome = pygame.image.load("assets/art_assets/gnome/title_gnome.png").convert_alpha()
tutorial_gnome = pygame.image.load("assets/art_assets/gnome/tutorial_gnome.png").convert_alpha()
tutorial_placard = pygame.image.load("assets/art_assets/screens/tutorial_placard.png").convert_alpha()
tutorial_arrow_1 = pygame.image.load("assets/art_assets/arrows/arrow_down.png").convert_alpha()
tutorial_arrow_2 = pygame.image.load("assets/art_assets/arrows/arrow_left.png").convert_alpha()
tutorial_arrow_3 = pygame.image.load("assets/art_assets/arrows/arrow_left.png").convert_alpha()
tutorial_arrow_4 = pygame.image.load("assets/art_assets/arrows/arrow_right.png").convert_alpha()
tutorial_arrow_5 = pygame.image.load("assets/art_assets/arrows/arrow_up.png").convert_alpha()
green_arrow = pygame.image.load("assets/art_assets/arrows/arrow_left_green.png").convert_alpha()
tutorial_base = pygame.image.load("assets/art_assets/screens/kitchen_mask_tutorial.png").convert_alpha()
tutorial_base_mask = pygame.mask.from_surface(tutorial_base)
kitchen_base = pygame.image.load("assets/art_assets/screens/kitchen_mask.png").convert_alpha()
kitchen_base_mask = pygame.mask.from_surface(kitchen_base)
end_base = pygame.image.load("assets/art_assets/screens/end_screen_mask.png").convert_alpha()
end_base_mask = pygame.mask.from_surface(end_base)
trashcan = pygame.image.load("assets/art_assets/storage/trashcan.png").convert_alpha()
trashcan_rect = trashcan.get_rect(topleft = trashcan_pos)          
counter = pygame.image.load("assets/art_assets/storage/counter.png").convert_alpha()
counter_rect = counter.get_rect(topleft = counter_offset)
timer_mark = pygame.image.load("assets/art_assets/buttons/timer_mark.png").convert_alpha()

# Create the main gnome player sprite:
gnomelius = Gnome()
gnomelius.rect.x, gnomelius.rect.y = gnome_start_x, gnome_start_y # Beginning pos in kitchen center.
gnome_group = pygame.sprite.Group() 
gnome_group.add(gnomelius)
gnome_placard = pygame.image.load("assets/art_assets/gnome/gnomelius_placard.png").convert_alpha()
gnome_placard_rect = gnome_placard.get_rect(topleft = gnome_placard_pos)

# Initialize customers instance:
customers = Customer_Group()

# Initialize ingredient box instances:
nori_zone = Storage("nori")
rice_zone = Storage("rice")
tuna_zone = Storage("tuna")
salmon_zone = Storage("salmon")
unagi_zone = Storage("unagi")
crab_zone = Storage("crab")
shrimp_zone = Storage("shrimp")
tamago_zone = Storage("tamago")
plate_zone = Storage("plate")

# Load in initial audio:
temp_ding = pygame.mixer.Sound("assets/sound_assets/temp_ding.wav")
temp_reject = pygame.mixer.Sound("assets/sound_assets/temp_reject.wav")
temp_serve = pygame.mixer.Sound("assets/sound_assets/temp_serve.wav")
gnome_oop = pygame.mixer.Sound("assets/sound_assets/gnome_oop.wav")
wrong_order = pygame.mixer.Sound("assets/sound_assets/wrong_order.wav")
lost_order = pygame.mixer.Sound("assets/sound_assets/lost_order.wav")

# Universal text functions:
coinfont = pygame.font.Font("assets/art_assets/text/font.ttf", font_small)
winfont = pygame.font.Font("assets/art_assets/text/font.ttf", font_large)
msgfont = pygame.font.Font("assets/art_assets/text/font.ttf", font_medium)

def update_display_coins(gnome):
    coins = coinfont.render('$' + str(gnome.money) + " / $" + str(ending_profit), True, BROWN)
    screen.blit(coins, coins_pos)
def update_display_win(gnome):
    win = winfont.render('SUCCESS! You made ' + '$' + str(gnome.money) + ' in profit.', True, BLACK)
    again = winfont.render('Press spacebar to head back into the kitchen!', True, BLACK)
    screen.blit(win, win_pos)
    screen.blit(again, again_pos)
def add_tutorial_message(message, message_pos):
    message = msgfont.render(message, True, BLACK)
    screen.blit(message, message_pos)
    
# Game loop:
while True:
    level.level_manager()
    clock.tick(60)