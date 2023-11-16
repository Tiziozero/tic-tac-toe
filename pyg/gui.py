import pygame
from enum import Enum
if __name__ != '__main__':
    from local_ai import ai_logic
    from local_pvp import pvp_logic


class Game_Type(Enum):
    GAME_TYPE_AI = 1
    GAME_TYPE_PVP = 2
    GAME_TYPE_QUIT = 3


class Game:
    def __init__(self, width, height):
        # pygame stuff
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("i cant take this anymore")
        self.font = pygame.font.Font(None, 36)
        # game board
        self.local_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.current_player = 1
        
        # game images
        self.total = 300
        self.board = None
        self.board_empty = None
        self.board_grid = None
        self.cross = None
        self.dot = None
        self.x_start = self.WIDTH // 2- self.total // 2
        self.y_start = self.HEIGHT // 2 - self.total // 2


    def setup_board(self):
        #load images
        self.board = pygame.image.load("graphics/board.png")
        self.board_empty = pygame.image.load("graphics/board_e.png")
        self.board_grid = pygame.image.load("graphics/board_grid.png")
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
                            return x, y
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            try:
                x, y = self.get_cell(event)
                self.game_logic((x, y))
            except:
                pass
    def check_win( self, board ):
        for row in board:
            if row[0] == row[1] == row[2]:
                if row[0] != 0:
                    return row[0], False

        if board[0][0] == board[1][1] == board[2][2]:
            if board[1][1] != 0:
                return board[1][1], False
        if board[0][2] == board[1][1] == board[2][0]:
            if board[1][1] != 0:
                return board[1][1], False

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] != 0:
                    return board[0][col], False

        for row in board:
            for element in row:
                if element == 0:
                    return 0,  True

        return 3, False

    def game_logic(self,pos):
        if self.local_board[pos[1]][pos[0]] == 0:
            self.local_board[pos[1]][pos[0]] = self.current_player
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
            print(f"Current player: {self.current_player}")
        else:
            print("not valid cell")

    def game_menu(self):                                # Set up fonts

        text_a = self.font.render("Press A for AI mode", True, (255, 255, 255))
        text_p = self.font.render("Press P for PvP", True, (255, 255, 255))
        text_q = self.font.render("Press Q to quit", True, (255, 255, 255))


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
                    elif event.key == pygame.K_q:
                        print("Quitting game")
                        return Game_Type.GAME_TYPE_QUIT

            self.screen.blit(self.board_empty, (0,0))

            self.screen.blit(text_a, (self.WIDTH // 2 - text_a.get_width() // 2, self.HEIGHT // 2 - 36))
            self.screen.blit(text_p, (self.WIDTH // 2 - text_p.get_width() // 2, self.HEIGHT // 2 + 36))
            self.screen.blit(text_q, (self.WIDTH // 2 - text_p.get_width() // 2, self.HEIGHT // 2 + 108))

            pygame.display.flip()
    # minmax ai
    def miniMax(self,board, depth, p1) :  
        score = self.check_win(board)
        if score[0] == 2:
            return 1
        elif score[0] == 1:
            return -1
        Found = False
        for r in range(3) : 
            for c in range(3) : 
                if (board[r][c] == 0) :
                    Found = True
        if not Found:
            return 0
        if p1:      
            best = -float("inf") 
            for r in range(3):          
                for c in range(3): 
                    if (board[r][c]== 0): 
                        board[r][c] = 2  
                        best = max(best, self.miniMax(board, depth + 1, not p1)) 
                        board[r][c] = 0
            return best 
        else : 
            best = float("inf") 
            for r in range(3):          
                for c in range(3): 
                    if (board[r][c] == 0):   
                        board[r][c] = 1
                        best = min(best, self.miniMax(board, depth + 1, not p1))
                        board[r][c] = 0
            return best

    def AI(self, board):  
        bestVal = -float("inf") 
        bestMove = ("banana", "1234")  
      
        for r in range(3):      
            for c in range(3): 
                if (board[r][c] == 0):   
                    board[r][c] = 2 
                    moveVal = self.miniMax(board, 0, False)  
                    board[r][c] = 0 
                    if (moveVal > bestVal):                 
                        bestMove = (r, c) 
                        bestVal = moveVal 
        board[bestMove[0]][bestMove[1]] = 2
        return board


    def game_pvp(self):
        self.local_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.current_player = 1
        bg_rect = self.board.get_rect()
        game_on = True
        winning_player = 0
        while game_on:
            self.events()
            winning_player, game_on = self.check_win(self.local_board)
            if not game_on:
                break
            self.screen.blit(self.board, bg_rect)
            self.update_screen()
            pygame.display.flip()
        print(f"player {winning_player} won!")
        self.winning_player_screen(winning_player)
        return winning_player

    def game_ai(self):
        self.local_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.current_player = 1
        bg_rect = self.board.get_rect()
        game_on = True
        winning_player = 0
        while game_on:
            self.events()
            winning_player, game_on = self.check_win(self.local_board)
            if not game_on:
                break
            if self.current_player == 2:
                self.local_board = self.AI(self.local_board) 
                winning_player, game_on = self.check_win(self.local_board)
                self.current_player = 1
                if not game_on:
                    break
            self.screen.blit(self.board, bg_rect)
            self.update_screen()
            pygame.display.flip()
        print(f"player {winning_player} won!")
        self.winning_player_screen(winning_player)
        return winning_player
    
    def winning_player_screen(self, winning_player):
        text = self.font.render(f"player {winning_player} won... bearly", True, (255,0,0))
        bg_rect = self.board.get_rect()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("quitting winning screen")
                        return
            self.screen.blit(self.board_empty, bg_rect)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 ))
            pygame.display.flip()
            

    def main(self):
        app_on = True
        while app_on:
            self.setup_board()
            mode = self.game_menu()
            
            if mode == Game_Type.GAME_TYPE_AI:
                self.game_ai()
            elif mode == Game_Type.GAME_TYPE_PVP:
                self.game_pvp()
            elif mode == Game_Type.GAME_TYPE_QUIT:
                app_on = False
                break
        pygame.quit()
        quit()
       
if __name__ == '__main__':
    pygame.init()
    game = Game(800, 450)
    game.main()
