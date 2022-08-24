from dataclasses import Field
from tokenize import Single
import pygame
from sys import exit

class Conquerors():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        infoObject = pygame.display.Info()
        # self.x = infoObject.current_w
        # self.y = infoObject.current_h
        self.x = 1000
        self.y = 1000
        self.screen = pygame.display.set_mode((self.x,self.y))
        self.current_selected = -1
        self.start_field = False
        self.init_assets()
        self.in_row = 8

        self.pawns = []
        id = 0
        for y_pos in range(2):
            for x_pos in range(8):
                if y_pos:
                    image = self.image_pawn_red
                else:
                    image = self.image_pawn_blue
                self.pawns.append(Pawn(self.screen, self.x, self.y, x_pos, y_pos * (self.y - self.y/self.in_row), self.in_row, image, id ))
                id += 1


        self.fields = []
        for y in range(8):
            for x in range(8):
                self.fields.append(SingleField(self.screen, self.x, self.y, x, y, self.in_row))


        # Game loop
        while True:
            self.play_step()
    

    def init_assets(self):
        #loading
        self.image_square = pygame.image.load('graphics/square.png').convert()
        self.image_pawn_red = pygame.image.load('graphics/pawn_red.png').convert()
        self.image_pawn_blue = pygame.image.load('graphics/pawn_blue.png').convert()
        

        #scaling
        self.image_square = pygame.transform.scale(self.image_square, (self.y, self.y))


    def update_UI(self):
        #Rects
        square_rect = self.image_square.get_rect(center = (self.x / 2, self.y / 2))

        #Drawing
        self.screen.blit(self.image_square, square_rect)
    
    def field_next_to_pawn(self, field):
        indent = self.x / self.in_row
        allowed_moves = [
            (self.start_field.x, self.start_field.y),#start
            (self.start_field.x, self.start_field.y + indent),#down
            (self.start_field.x, self.start_field.y - indent),#up
            (self.start_field.x + indent, self.start_field.y), #left
            (self.start_field.x - indent, self.start_field.y), #right
        ]

        if field.get_pos_tuple() in allowed_moves:
            return True
        else:
            return False


    def play_step(self):
        mousebuttonup = False
        mousebuttondown = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                print('up')
                mousebuttonup = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('down')
                mousebuttondown = True

        #self.update_UI()
        
        for field in self.fields:
            field.draw_field()

#====== MOUSE MOVE PAWN ==============
        ignore_next_move = False
        if mousebuttondown and self.current_selected != -1:
            self.current_selected = -1
            ignore_next_move = True
            self.start_field = False 
        for pawn in self.pawns:
            current_selected = pawn.select(mousebuttondown,self.current_selected )
            if current_selected == pawn.id and not ignore_next_move:
                self.current_selected = current_selected
                for field in self.fields:
                    if field.field_rect.collidepoint(pygame.mouse.get_pos()) and not self.start_field:
                        self.start_field = field
                        print(field.x)
                    if field.field_rect.collidepoint(pygame.mouse.get_pos()) and self.field_next_to_pawn(field):
                        pawn.pawn_rect = pawn.image_pawn.get_rect(topleft = (field.x, field.y))
#======================================    
            
            pawn.draw_pawn()


        pygame.display.update()
        self.clock.tick(60)

class Pawn():
    def __init__(self, screen, x_res, y_res, x_pos, y_pos, in_row, image, id):
        self.x_res = x_res
        self.y_res = y_res
        self.screen = screen
        self.x_pos = x_pos
        self.x = (self.x_res - self.y_res)/2 + x_pos * y_res / in_row
        self.y = y_pos
        self.id = id
        self.previous_location = (self.x, self.y)
        self.image_pawn = image
        self.load_assets()
        self.pawn_rect = self.image_pawn.get_rect(topleft = (self.x, self.y))

    def load_assets(self):
        self.image_pawn = pygame.transform.scale(self.image_pawn, (self.y_res / 8, self.y_res / 8))

    def update_pawn(self):
        self.pawn_rect = self.image_pawn.get_rect(topleft = (self.x, self.y))
            
    def select(self, mousebuttondown, current_selected):
        if current_selected == self.id or (current_selected == -1 and mousebuttondown and self.pawn_rect.collidepoint(pygame.mouse.get_pos())):
            return self.id
        return -1,
    
    def move_pawn(self):
        pass

    def draw_pawn(self):
        self.screen.blit(self.image_pawn, self.pawn_rect)

class SingleField():
    def __init__(self,screen, x_res, y_res, x_pos, y_pos, in_row):
        self.level = 0
        self.screen = screen
        self.x_res = x_res
        self.y_res = y_res
        self.x = x_pos * x_res/in_row
        self.y = y_pos * y_res/in_row
        self.load_assets()
        self.field_rect = self.image_field.get_rect(topleft = (self.x, self.y))

    def load_assets(self):
        self.image_field = pygame.image.load('graphics/squares/single_square_small.png')
        self.image_field = pygame.transform.scale(self.image_field, (self.y_res / 8, self.y_res / 8))

    def update_field(self):
        self.field_rect = self.image_field.get_rect(topleft = (self.x, self.y))

    def draw_field(self):
        self.screen.blit(self.image_field, self.field_rect)

    def get_pos_tuple(self):
        return (self.x, self.y)
    
game = Conquerors()
