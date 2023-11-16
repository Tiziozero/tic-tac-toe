import pygame
from enum import Enum
if __name__ != '__main__':
    from local_ai import ai_logic
    from local_pvp import pvp_logic


class Game_Type(Enum):
    GAME_TYPE_AI = 1,
    GAME_TYPE_PVP = 2

class Game:
    def __init__(self, width, height):
        # pygame stuff
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("i cant take this anymore")
        self.font = pygame.font.Font(None, 36)
        # game board
        self.local_board = [[0,1,0],[1,2,1],[2,0,1]]
        
        # game images
        self.total = 300
        self.board = None
        self.cross = None
        self.dot = None
        self.x_start = self.WIDTH // 2- self.total // 2
        self.y_start = self.HEIGHT // 2 - self.total // 2


    def setup_board(self):
        #load images
        self.board = pygame.image.load("graphics/board.png")
        self.cross = pygame.image.load("graphics/cross.png")
        self.dot = pygame.image.load("graphics/dot.png")

        # resize
        original_size = self.board.get_size()
        scale_factor = 1.3072
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))

        # Scale the image
        #self.board = pygame.transform.scale(self.board, (800, 800))


    def update_screen(self):
        for x in range(3):
            for y in range(3):
                if self.local_board[y][x] == 0:
                    pass
                elif self.local_board[y][x] == 1:
                    rect = self.cross.get_rect()
                    rect.x, rect.y = self.x_start + 100 * x, self.y_start + 100 * y
                    self.screen.blit(self.cross, rect)
                elif self.local_board[y][x] == 2:
                    rect = self.dot.get_rect()
                    rect.x, rect.y = self.x_start + 100 * x, self.y_start + 100 * y
                    self.screen.blit(self.dot, rect)

    def get_cell(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            print("x, y: ", mpos)
            for x in range(3):
                for y in range(3):
                    if mpos[0] >= self.x_start + 100 * x and mpos[0] <= self.x_start + 100 * x + 100:
                        if mpos[1] >= self.y_start + 100 * y and mpos[1] <= self.y_start + 100 * y + 100:
                            print(f"x: {x}, y: {y}, cell: {self.local_board[y][x]}, m_x: {mpos[0]}, m_y: {mpos[1]}")
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.get_cell(event)
    
    def game_menu(self):                                # Set up fonts
        font = pygame.font.Font(None, 36)

        # Display text
        text_a = self.font.render("Press A for AI mode", True, (255, 255, 255))
        text_p = self.font.render("Press P for PvP", True, (255, 255, 255))

        # Main loop

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print("AI mode selected")
                        # Add your AI mode logic here
                        return Game_Type.GAME_TYPE_AI 
                    elif event.key == pygame.K_p:
                        print("PvP mode selected")
                        return Game_Type.GAME_TYPE_PVP


            self.screen.fill((0, 0, 0))

            self.screen.blit(text_a, (self.WIDTH // 2 - text_a.get_width() // 2, self.HEIGHT // 2 - 36))
            self.screen.blit(text_p, (self.WIDTH // 2 - text_p.get_width() // 2, self.HEIGHT // 2 + 36))

            pygame.display.flip()

    def game_ai(self):
        while True:
            self.events()
            
            bg_rect = self.board.get_rect()
            crect = self.cross.get_rect()
            drect = self.dot.get_rect()
            self.screen.blit(self.board, bg_rect)
            self.screen.blit(self.cross, crect)
            self.screen.blit(self.dot, drect)
            self.update_screen()
            pygame.display.flip()

    def main(self):
        self.setup_board()
        mode = self.game_menu()
        
        if mode == Game_Type.GAME_TYPE_AI:
            self.game_ai()
        elif mode == Game_Type.GAME_TYPE_PVP:
            #self.game_pvp()
            pass

        pass
       
if __name__ == '__main__':
    pygame.init()
    game = Game(800, 450)
    game.main()
