import pygame
import spritesheet
import random

from sys import exit

# Constants:
nori_pos = (162,265)
rice_pos = (324,450)
tuna_pos = (410,500)
salmon_pos = (806,455)
unagi_pos = (370,70)
plate_pos = (168,160)
plate_offset = (168,174)
trashcan_pos = (883,310)
counter_pos = (572,127)
counter_offset = (572,187)

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
        gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet.png").convert_alpha()
        gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)
        for x in range(0,4):
            self.images.append(gnome_sheet.get_image(x, 96, 96, BLACK, scale = 1))
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        #self.rect = self.rect.inflate(-10,-45)
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
        offset_x = kitchen_pos[0] - gnomelius.rect.left
        offset_y = kitchen_pos[1] - gnomelius.rect.top
        
        if self.mask.overlap_area(kitchen_base_mask, (offset_x,offset_y)) <= 60:
            self.previous_pos = (self.rect.center)
        if self.mask.overlap_area(kitchen_base_mask, (offset_x,offset_y)) > 0:
            self.rect.center = self.previous_pos
            
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
         
        if self.movex < 0:
            self.frame = 2
            self.image = self.images[self.frame]
            
        if self.movex > 0:
            self.frame = 3
            self.image = self.images[self.frame]
            
        if self.movey < 0:
            self.frame = 0
            self.image = self.images[self.frame]   
            
        if self.movey > 0:
            self.frame = 1
            self.image = self.images[self.frame]
    
    def update_plate(self, action):
        """
        Update gnome spritesheet based on plate contents.
        """
        gnome_spritesheet = None
        facing_dir = 1
        #print((self.plate.contains))
        if action == "pick_up" and self.plate != None:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_plate.png").convert_alpha()
            self.plate = Plate()
        elif action == "add_nori" and len(self.plate.contains) == 0:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_nori.png").convert_alpha() 
            facing_dir = 3       
        elif action == "add_rice" and len(self.plate.contains) == 1:
            gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_rice.png").convert_alpha() 
            facing_dir = 3  
        elif len(self.plate.contains) == 2: 
            if action == "add_tuna":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_tuna.png").convert_alpha() 
            elif action == "add_salmon":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_salmon.png").convert_alpha()
            elif action == "add_unagi":
                gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet_unagi.png").convert_alpha() 
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
            self.image = self.images[facing_dir]
            
            
class Storage():
    """
    Class for the storage boxes that hold ingredients.
    """
    def __init__(self,type):
        self.type = type
        self.image = None
        if type == "unagi":
            self.image = pygame.image.load("art_assets/storage/unagi_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = unagi_pos)
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w * 0.7, self.rect.h * 0.7))
            self.rect = self.image.get_rect(topleft = unagi_pos)
        elif type == "salmon":
            self.image = pygame.image.load("art_assets/storage/salmon_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = salmon_pos)
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(topleft = salmon_pos)
        elif type == "tuna":
            self.image = pygame.image.load("art_assets/storage/tuna_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = tuna_pos)
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w * 0.7, self.rect.h * 0.7))
            self.rect = self.image.get_rect(topleft = tuna_pos)
        elif type == "rice":
            self.image = pygame.image.load("art_assets/storage/rice_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = rice_pos)
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w * 0.6, self.rect.h * 0.6))
            self.rect = self.image.get_rect(topleft = rice_pos)
        elif type == "nori":
            self.image = pygame.image.load("art_assets/storage/nori_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = nori_pos)
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w, self.rect.h))
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w * 0.8, self.rect.h * 0.8))
            self.rect = self.image.get_rect(topleft = nori_pos)
        elif type == "plate":
            self.image = pygame.image.load("art_assets/storage/plate_box.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = plate_pos)
            self.image = pygame.transform.smoothscale(self.image,(self.rect.w * 0.8, self.rect.h))
    
    
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
    
    
class Customer():
    def __init__(self, id, line_pos, request, payment):
        self.id = id
        self.line_pos = line_pos
        self.payment = payment
        self.request = request
        if request == "tuna":
            placard_text = pygame.image.load("art_assets/text/profile_text_tuna.png").convert_alpha()
        elif request == "salmon":
            placard_text = pygame.image.load("art_assets/text/profile_text_salmon.png").convert_alpha()
        elif request == "unagi":
            placard_text = pygame.image.load("art_assets/text/profile_text_unagi.png").convert_alpha()
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


class Customer_Group():
    def __init__(self):
        self.attendance = {}
        self.absent_names = ["horace", "jeb", "jordan", "mickey", "pickles", "tom"]
        self.sushi_options = ["salmon", "tuna", "unagi"]
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
            payment = random.randrange(15,55,5)
            self.attendance[line_pos] = Customer(customer_name, line_pos, sushi_choice, payment)
            self.absent_names.remove(customer_name)
            return line_pos
        return False
    
    def fulfill_order(self,dish):
        """
        Fulfills order and removes it from queue. Returns line position of 
        fulfilled order if submitted, and False otherwise.
        
        Note: removal of person and placard art asset done in game loop.
        """
        line_pos = 1
        for _ in range(4):
            if self.attendance.get(line_pos, -1) != -1:
                if self.attendance[line_pos].request == dish:
                    self.absent_names.append(self.attendance[line_pos].id)
                    self.owed_payment += self.attendance[line_pos].payment
                    return line_pos
            line_pos += 1
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'
                pygame.mixer.music.play()
        screen.fill((240,240,240))
        screen.blit(start_button, (380, 300))  
        pygame.display.update()
         
    def main_game(self):
        #offset_x = kitchen_pos[0] - gnomelius.rect.left
        #offset_y = kitchen_pos[1] - gnomelius.rect.top
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
                    if pygame.Rect.colliderect(gnomelius.rect,plate_box.rect):
                        gnomelius.plate = Plate()
                        gnomelius.update_plate("pick_up")
                        complete = True
                    elif gnomelius.plate != None:
                        if pygame.Rect.colliderect(gnomelius.rect,nori_box.rect):
                            gnomelius.update_plate("add_nori")
                            gnomelius.plate.add_item("nori")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,rice_box.rect):
                            gnomelius.update_plate("add_rice")
                            gnomelius.plate.add_item("rice")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,tuna_box.rect):
                            gnomelius.update_plate("add_tuna")
                            gnomelius.plate.add_item("tuna")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,salmon_box.rect):
                            gnomelius.update_plate("add_salmon")
                            gnomelius.plate.add_item("salmon")
                            complete = True
                        elif pygame.Rect.colliderect(gnomelius.rect,unagi_box.rect):
                            gnomelius.update_plate("add_unagi")
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
                                gnomelius.update_plate("empty_items")
                                gnomelius.plate = Plate()                          
                    if dominant_sound:
                        if complete :
                            pygame.mixer.Sound.play(temp_ding)
                        elif not complete:
                            pygame.mixer.Sound.play(temp_reject)

            
        screen.fill(BACKGROUND_COLOR)
        screen.blit(kitchen_base, kitchen_pos)
        screen.blit(nori_box.image, nori_pos)
        screen.blit(rice_box.image, rice_pos)
        screen.blit(tuna_box.image, tuna_pos)
        screen.blit(salmon_box.image, salmon_pos)
        screen.blit(unagi_box.image, unagi_pos)
        screen.blit(plate_box.image, plate_offset)
        screen.blit(trashcan, trashcan_pos)
        screen.blit(counter, counter_pos)
        
        num_customers = len(customers.attendance)
        if num_customers == 0:
            position = customers.add_order()
            self.main_adding_in_pos[position] = True
        if num_customers < 4:
            temp_rand = random.randint(1, 600)
            if temp_rand == 600:
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
            screen.blit(customer.person, (customer.person_pos_x, customer.person_pos_y))
            screen.blit(customer.placard_profile, (customer.placard_pos_x, customer.placard_pos_y))
            screen.blit(customer.placard_text, (customer.placard_pos_x, customer.placard_pos_y))
            
        gnomelius.update()
        gnome_group.draw(screen)
        pygame.display.update()
        
    def level_manager(self):
        if self.state == 'title':
            self.title()
        if self.state == 'main_game':
            self.main_game()
        
# Define Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
BACKGROUND_COLOR = (183,168,153)
BLACK = (0,0,0)

# Pygame Setup
pygame.init()
clock = pygame.time.Clock()
level = Level()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('A Gnome Game')
#pygame.mouse.set_visible(False)

# Base asset loading.
gnome_spritesheet = pygame.image.load("art_assets/gnome/gnomesheet.png").convert_alpha()
gnome_sheet = spritesheet.SpriteSheet(gnome_spritesheet)

start_button = pygame.image.load("art_assets/startbutton.png")
kitchen = kitchen_base = pygame.image.load("art_assets/kitchen_mask_old.png").convert_alpha()
kitchen_base = pygame.image.load("art_assets/kitchen_mask.png").convert_alpha()
kitchen_base_mask = pygame.mask.from_surface(kitchen_base)
kitchen_pos = (0,0)

trashcan = pygame.image.load("art_assets/trashcan.png").convert_alpha()
trashcan_rect = trashcan.get_rect(topleft = trashcan_pos)
                    
counter = pygame.image.load("art_assets/counter.png").convert_alpha()
counter_rect = counter.get_rect(topleft = counter_pos)

# Create the main gnome.
gnomelius = Gnome()
gnomelius.rect.x, gnomelius.rect.y = 440, 220
gnome_group = pygame.sprite.Group() 
gnome_group.add(gnomelius)

# Initialize the customers.
customers = Customer_Group()

# Create the ingredient boxes.
nori_box = Storage("nori")
rice_box = Storage("rice")
tuna_box = Storage("tuna")
salmon_box = Storage("salmon")
unagi_box = Storage("unagi")
plate_box = Storage("plate")

pygame.mixer.music.load("sound_assets/blue_bird.wav")
#pygame.mixer.music.play()

# Temp audio sound
temp_ding = pygame.mixer.Sound("sound_assets/temp_ding.wav")
temp_reject = pygame.mixer.Sound("sound_assets/temp_reject.wav")
temp_serve = pygame.mixer.Sound("sound_assets/temp_serve.wav")

# Begin game
while True:
    level.level_manager()
    clock.tick(60)