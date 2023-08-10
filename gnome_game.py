import pygame
import spritesheet
import random

from sys import exit

"""
This is the main code for Gnome: Makizushi by LHermannCoding. Credit to Clear 
Code and Coding with Russ for their helpful YouTube tutorials on masks, game 
state management, and more.

"""
# Constants:
origin = (0,0)
title_gnome_x = 880
title_gnome_y = 135
start_pos = (200, 330)
help_pos = (500, 330)
nori_pos = (616, 368)
rice_pos = (260, 450)
crab_pos = (290, 311)
shrimp_pos = (62,10)
tamago_pos = (267,0)
tuna_pos = (90,180)
salmon_pos = (776,455)
unagi_pos = (80,300)
plate_pos = (516,524)
plate_offset = (168,174)
trashcan_pos = (883,310)
counter_pos = (572,127)
counter_offset = (572,187)
coins_pos = (824,649)
gnome_placard_pos = (646,616)
placard_profile_pos = (640,619)
win_pos = (188, 500)

# Dynamic Constants:
animation_timer = 0
win_animation_timer = 0
payment_max = 2000

class Gnome(pygame.sprite.Sprite):
    """
    Sprite class for the main character of the game.
    """
    def __init__(self):
        super().__init__()
        self.movex = 0
        self.movey = 0
        self.previous_pos = (0,0)
        self.pink = False
        self.steps = 3
        self.frame = 0
        self.images = []
        self.plate = None
        self.money = 0
        self.game_state = 'main_game'
        gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet.png").convert_alpha()
        gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)
        for x in range(0,4):
            self.images.append(gnome_sheet.get_image(x, 96, 96, BLACK, scale = 1))
        self.image = self.images[1]
        self.placard_profile = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) #might need to update in update method
    
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
        
        if self.game_state == 'main_game':
            current_mask = kitchen_base_mask
        elif self.game_state == 'end_game':
            current_mask = end_base_mask
            
        if self.mask.overlap_area(current_mask, (offset_x,offset_y)) <= 60:
            self.previous_pos = (self.rect.center)
        if self.mask.overlap_area(current_mask, (offset_x,offset_y)) > 0:
            self.rect.center = self.previous_pos
            
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
        #print((self.plate.contains))
        if action == "pick_up" and self.plate != None:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_plate.png").convert_alpha()
            self.plate = Plate()
        elif action == "add_nori" and len(self.plate.contains) == 0:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_nori.png").convert_alpha()        
        elif action == "add_rice" and len(self.plate.contains) == 1:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_rice.png").convert_alpha() 
        elif len(self.plate.contains) == 2: 
            if action == "add_tuna":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_tuna.png").convert_alpha() 
            elif action == "add_salmon":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_salmon.png").convert_alpha()
            elif action == "add_unagi":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_unagi.png").convert_alpha()
            elif action == "add_crab":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_crab.png").convert_alpha() 
            elif action == "add_shrimp":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_shrimp.png").convert_alpha() 
            elif action == "add_tamago":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_tamago.png").convert_alpha() 
        elif action == "put_down":
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet.png").convert_alpha()
            self.plate = None
        elif action == "empty_items":
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_plate.png").convert_alpha()
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
            self.image = pygame.image.load("art_assets/storage/unagi_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = unagi_pos)
        elif type == "salmon":
            self.image = pygame.image.load("art_assets/storage/salmon_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = salmon_pos)
        elif type == "crab":
            self.image = pygame.image.load("art_assets/storage/crab_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = crab_pos)
        elif type == "shrimp":
            self.image = pygame.image.load("art_assets/storage/shrimp_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = shrimp_pos)
        elif type == "tamago":
            self.image = pygame.image.load("art_assets/storage/tamago_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = tamago_pos)
        elif type == "tuna":
            self.image = pygame.image.load("art_assets/storage/tuna_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = tuna_pos)
        elif type == "rice":
            self.image = pygame.image.load("art_assets/storage/rice_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = rice_pos)
        elif type == "nori":
            self.image = pygame.image.load("art_assets/storage/nori_zone.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = nori_pos)
        elif type == "plate":
            self.image = pygame.image.load("art_assets/storage/plate_zone.png").convert_alpha()
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
        self.request = request
        if request == "tuna":
            placard_text = pygame.image.load("art_assets/text/profile_text_tuna.png").convert_alpha()
        elif request == "salmon":
            placard_text = pygame.image.load("art_assets/text/profile_text_salmon.png").convert_alpha()
        elif request == "unagi":
            placard_text = pygame.image.load("art_assets/text/profile_text_unagi.png").convert_alpha()
        elif request == "crab":
            placard_text = pygame.image.load("art_assets/text/profile_text_crab.png").convert_alpha()
        elif request == "shrimp":
            placard_text = pygame.image.load("art_assets/text/profile_text_shrimp.png").convert_alpha()
        elif request == "tamago":
            placard_text = pygame.image.load("art_assets/text/profile_text_tamago.png").convert_alpha()
        self.placard_text = placard_text
        
        if id == "horace":
            temp_sheet = pygame.image.load("art_assets/customers/horace/spritesheet_horace.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/horace/horace_profile.png").convert_alpha()
        elif id == "jeb":
            temp_sheet = pygame.image.load("art_assets/customers/jeb/spritesheet_jeb.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/jeb/jeb_profile.png").convert_alpha()
        elif id == "jordan":
            temp_sheet = pygame.image.load("art_assets/customers/jordan/spritesheet_jordan.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/jordan/jordan_profile.png").convert_alpha()
        elif id == "mickey":
            temp_sheet = pygame.image.load("art_assets/customers/mickey/spritesheet_mickey.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/mickey/mickey_profile.png").convert_alpha()
        elif id == "pickles":
            temp_sheet = pygame.image.load("art_assets/customers/pickles/spritesheet_pickles.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/pickles/pickles_profile.png").convert_alpha()
        elif id == "tom":
            temp_sheet = pygame.image.load("art_assets/customers/tom/spritesheet_tom.png").convert_alpha()
            placard_profile = pygame.image.load("art_assets/customers/tom/tom_profile.png").convert_alpha()
        self.placard_profile = placard_profile
        self.person_animation = []
        customer_spritesheet = spritesheet.SpriteSheet(temp_sheet)
        for x in range(0,2):
            self.person_animation.append(customer_spritesheet.get_image(x, 96, 96, BLACK, scale = 1))
        self.person = self.person_animation[1]
        
        self.person_pos_x = (80 * line_pos) + 500
        self.person_pos_y = -205
        
        self.placard_pos_x = (160 * line_pos) - 154
        self.placard_pos_y = 1080
    
    def payment_calculation(self):
        """
        Calculate how much will be paid out for fulfillment or order based on 
        time spent waiting for dish.
        """
        self.payment = max(10, int(self.payment * (self.payment_timer / payment_max)))


class Customer_Group():
    def __init__(self):
        self.attendance = {}
        self.arrival_order = []
        self.absent_names = ["horace", "jeb", "jordan", "mickey", "pickles", "tom"]
        self.sushi_options = ["salmon", "tuna", "unagi", "crab", "shrimp", "tamago"]
        self.owed_payment = 0
        
    def add_order(self):
        """
        Adds order to queue. Returns line position of added order (when
        there is enough space in line), and False otherwise.
        
        Note: blitting of order placard art asset done in game loop.
        """
        line_pos = 1
        while self.attendance.get(line_pos, -1) != -1:
            line_pos += 1
        if line_pos <= 4:
            customer_name = random.choice(self.absent_names)
            sushi_choice = random.choice(self.sushi_options)
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
        self.main_adding_in_pos = {1: False, 2: False, 3: False, 4: False}
        self.main_removing_in_pos = {1: False, 2: False, 3: False, 4: False}
        
    def title(self):
        global animation_timer
        global title_gnome_x
        global title_gnome_y
        screen.blit(title_bg, origin)  
        if title_gnome_x >= 580:
            title_gnome_x -= 3
        elif animation_timer <= 150:
            animation_timer += 4
            
        if animation_timer >= 50:
            s = screen.blit(start_button, start_pos)
        if animation_timer >= 100:
            h = screen.blit(help_button, help_pos)
            
        g = screen.blit(title_gnome, (title_gnome_x, title_gnome_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if animation_timer >= 100:
                    pos = pygame.mouse.get_pos()
                    if s.collidepoint(pos):
                        self.state = 'main_game'
                        pygame.mixer.music.play()             
                    elif h.collidepoint(pos):
                        print("temp for tutorial placeholder")
                    elif g.collidepoint(pos):
                        #play_sound?
                        print("temp sound placeholder honk")
        pygame.display.update()
         
         
    def main_game(self):
        global title_gnome_x
        global title_gnome_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit
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
                    dominant_sound = True
                    if pygame.Rect.colliderect(gnomelius.rect,plate_zone.rect):
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
                            gnomelius.plate.add_item("unagi")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,shrimp_zone.rect):
                            gnomelius.update_plate("add_shrimp")
                            gnomelius.plate.add_item("unagi")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,tamago_zone.rect):
                            gnomelius.update_plate("add_tamago")
                            gnomelius.plate.add_item("unagi")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,trashcan_rect):
                            gnomelius.update_plate("empty_items")
                            gnomelius.plate = Plate()
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,counter_rect):
                            if len(gnomelius.plate.contains) == 3:
                                removal = customers.fulfill_order(gnomelius.plate.contains[2])
                                if removal:
                                    customers.attendance[removal].person = customers.attendance[removal].person_animation[0]
                                    pygame.mixer.Sound.play(temp_serve)
                                    dominant_sound = False
                                    self.main_removing_in_pos[removal] = True 
                                    gnomelius.money = min(gnomelius.money + customers.owed_payment, 999)
                                    customers.owed_payment = 0 
                                gnomelius.update_plate("put_down")                        
                    if dominant_sound:
                        if complete :
                            pygame.mixer.Sound.play(temp_ding)
                        elif not complete:
                            pygame.mixer.Sound.play(temp_reject)

            
        screen.fill(BACKGROUND_COLOR)
        screen.blit(kitchen_base, origin)
        screen.blit(nori_zone.image, nori_pos)
        screen.blit(rice_zone.image, rice_pos)
        screen.blit(tuna_zone.image, tuna_pos)
        screen.blit(salmon_zone.image, salmon_pos)
        screen.blit(unagi_zone.image, unagi_pos)
        screen.blit(crab_zone.image, plate_offset)
        screen.blit(shrimp_zone.image, plate_offset)
        screen.blit(tamago_zone.image, plate_offset)
        screen.blit(plate_zone.image, plate_offset)
        screen.blit(trashcan, trashcan_pos)
        screen.blit(counter, counter_pos)
        screen.blit(gnomelius.placard_profile, placard_profile_pos)
        screen.blit(gnome_placard, gnome_placard_pos)
        update_display_coins(gnomelius)
         
        num_customers = len(customers.attendance)
        if num_customers == 0:
            position = customers.add_order()
            self.main_adding_in_pos[position] = True
        if num_customers < 4:
            temp_rand = random.randint(1, 480)
            if temp_rand == 480:
                position = customers.add_order()
                if position:
                    self.main_adding_in_pos[position] = True
            
        for add_pos, add_bool in self.main_adding_in_pos.items():
            if add_bool == True:
                still_adding = 0
                if customers.attendance[add_pos].person_pos_y < 25:
                    customers.attendance[add_pos].person_pos_y += 1
                else:
                    still_adding += 1
                if customers.attendance[add_pos].placard_pos_y > 616:
                    customers.attendance[add_pos].placard_pos_y -= 2
                else:
                    still_adding += 1
                if still_adding == 2 or self.main_removing_in_pos[add_pos]:
                    self.main_adding_in_pos[add_pos] = False
        for removal_pos, removal_bool in self.main_removing_in_pos.items():
            still_removing = 0
            if removal_bool:
                if customers.attendance[removal_pos].person_pos_y > -100:
                    customers.attendance[removal_pos].person_pos_y -= 1
                else:
                    still_removing += 1
                if customers.attendance[removal_pos].placard_pos_y < 920:
                    customers.attendance[removal_pos].placard_pos_y += 1
                else:
                    still_removing += 1
                if still_removing == 2:
                    self.main_removing_in_pos[removal_pos] = False
                    del customers.attendance[removal_pos]
        
        for customer in customers.attendance.values():
            customer.payment_timer -= 1
            screen.blit(customer.person, (customer.person_pos_x, customer.person_pos_y))
            screen.blit(customer.placard_profile, (customer.placard_pos_x, customer.placard_pos_y))
            screen.blit(customer.placard_text, (customer.placard_pos_x, customer.placard_pos_y))
            
        gnomelius.update()
        gnome_group.draw(screen)
        
        if title_gnome_x >= -360:
            title_gnome_x -= 14
            screen.blit(title_gnome, (title_gnome_x,title_gnome_y))
        pygame.display.update()
        
        if gnomelius.money >= 100:
            gnomelius.steps = 3
            gnomelius.game_state = 'end_game'
            self.state = 'end_game'
        
    def end_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit
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
                    
        screen.fill(BACKGROUND_COLOR)
        screen.blit(end_base, origin)
        screen.blit(gnomelius.placard_profile, placard_profile_pos)
        screen.blit(gnome_placard, gnome_placard_pos)
        update_display_coins(gnomelius)
        update_display_win(gnomelius)
        
        gnomelius.update()
        gnome_group.draw(screen)
        pygame.display.update()
        
        
    def level_manager(self):
        if self.state == 'title':
            self.title()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'end_game':
            self.end_game()


# Define Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
BACKGROUND_COLOR = (183,168,153)
BLACK = (0,0,0)
BROWN = (46, 32, 6)

# Pygame Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
level = Level()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('A Gnome Game')
#pygame.mouse.set_visible(False)

# Base asset loading.
gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet.png").convert_alpha()
gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)

start_button = pygame.image.load("art_assets/buttons/start.png")
start_rect = start_button.get_rect(topleft = trashcan_pos)
help_button = pygame.image.load("art_assets/buttons/help.png")
help_rect = help_button.get_rect(topleft = trashcan_pos)

title_bg = pygame.image.load("art_assets/title_background.png")
title_gnome = pygame.image.load("art_assets/title_gnome.png")

kitchen_base = pygame.image.load("art_assets/kitchen_mask.png").convert_alpha()
kitchen_base_mask = pygame.mask.from_surface(kitchen_base)

end_base = pygame.image.load("art_assets/end_screen_mask.png").convert_alpha()
end_base_mask = pygame.mask.from_surface(end_base)

trashcan = pygame.image.load("art_assets/trashcan.png").convert_alpha()
trashcan_rect = trashcan.get_rect(topleft = trashcan_pos)
                    
counter = pygame.image.load("art_assets/counter.png").convert_alpha()
counter_rect = counter.get_rect(topleft = counter_pos)

# Create the main gnome.
gnomelius = Gnome()
gnomelius.rect.x, gnomelius.rect.y = 440, 220
gnome_group = pygame.sprite.Group() 
gnome_group.add(gnomelius)
gnome_placard = pygame.image.load("art_assets/gnome/gnomelius_placard.png").convert_alpha()
gnome_placard_rect = gnome_placard.get_rect(topleft = gnome_placard_pos)

# Initialize the customers.
customers = Customer_Group()

# Create the ingredient boxes.
nori_zone = Storage("nori")
rice_zone = Storage("rice")
tuna_zone = Storage("tuna")
salmon_zone = Storage("salmon")
unagi_zone = Storage("unagi")
crab_zone = Storage("crab")
shrimp_zone = Storage("shrimp")
tamago_zone = Storage("tamago")
plate_zone = Storage("plate")

pygame.mixer.music.load("sound_assets/blue_bird.wav")
#pygame.mixer.music.play()

# Temp audio sound
temp_ding = pygame.mixer.Sound("sound_assets/temp_ding.wav")
temp_reject = pygame.mixer.Sound("sound_assets/temp_reject.wav")
temp_serve = pygame.mixer.Sound("sound_assets/temp_serve.wav")

# Universal Functions:
coinfont = pygame.font.Font("art_assets/coins_font.ttf", 27)
winfont = pygame.font.Font("art_assets/coins_font.ttf", 48)
def update_display_coins(gnome):
    coins = coinfont.render('$' + str(gnome.money), True, BROWN)
    screen.blit(coins, coins_pos)
def update_display_win(gnome):
    win = winfont.render('SUCCESS! You made ' + '$' + str(gnome.money) + ' in profit.', True, BROWN)
    screen.blit(win, win_pos)
    
# Begin game
while True:
    level.level_manager()
    clock.tick(60)