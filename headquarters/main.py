import pygame
from sys import exit

class Conquerors():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        infoObject = pygame.display.Info()
        self.x = infoObject.current_w
        self.y = infoObject.current_h
        # self.x = 1000
        # self.y = 1000
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.x,self.y))
        self.init_assets()

        self.pawns_red = [Pawn(self.screen, self.x, self.y, id, 8, self.image_pawn_red, 0) for id in range(8)]
        self.pawns_blue = [Pawn(self.screen, self.x, self.y, id, 8, self.image_pawn_blue, self.y - self.y/8 ) for id in range(8)]

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

    def play_step(self):
        mouseclick = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

        self.update_UI()

        for pawn in self.pawns_red:
            pawn.move_with_mouse()
            pawn.draw_pawn()
            

        for pawn in self.pawns_blue:
            pawn.move_with_mouse()
            pawn.draw_pawn()

        
        pygame.display.update()
        self.clock.tick(60)

class Pawn():
    def __init__(self, screen, x_res, y_res, pawn_id, in_row, image, side):
        self.x_res = x_res
        self.y_res = y_res
        self.screen = screen
        self.pawn_id = pawn_id
        self.x = (self.x_res - self.y_res)/2 + pawn_id * y_res / in_row
        self.y = side
        self.image_pawn = image
        self.load_assets()

    def load_assets(self):
        self.image_pawn = pygame.transform.scale(self.image_pawn, (self.y_res / 8, self.y_res / 8))

    def update_pawn(self):
        self.pawn_rect = self.image_pawn.get_rect(topleft = (self.x, self.y))
            
    def move_with_mouse(self):
        if pygame.mouse.get_pressed()[0] and self.pawn_rect.collidepoint(pygame.mouse.get_pos()):
            self.pawn_rect = self.image_pawn.get_rect(center = pygame.mouse.get_pos())
        else:
            self.update_pawn()

        
    def draw_pawn(self):
        self.screen.blit(self.image_pawn, self.pawn_rect)

class SingleField():
    def __init__(self):
        pass



game = Conquerors()
