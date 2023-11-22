import pygame
from enum import Enum
from random import choice
import os
import sys
import threading
if __name__ =='__main__':
    import client
else:
    from pyg import client
class Game_Type(Enum):
    GAME_TYPE_AI = 1,
    GAME_TYPE_PVP = 2,
    GAME_TYPE_QUIT = 3

class Button:
    def __init__(self, x, y, width, hight, size, font, text, mode):
        self.x = x
        self.y = y
        self.img = font.render(text, True, (255,0,0))
        self.mode = mode
        print("button mode", mode)
    def hover_over(self, mouse_pos):
        if mouse_pos[0] >= self.x - self.img.get_width() // 2 and mouse_pos[0] <= self.x + self.img.get_width() // 2:
            if mouse_pos[1] >= self.y - self.img.get_height() // 2 and mouse_pos[1] <= self.y + self.img.get_height() // 2:
                print("in range")
                return True
    def click(self, mouse_pos):
        if self.hover_over(mouse_pos):
            return self.mode


    def display(self, screen):
        screen.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

class Game:
    def __init__(self, width, height, multiplier):
        self.current_dir = ""# os.path.dirname(os.path.abspath(__file__)) + "/"
        # pygame stuff
        self.multiplier = multiplier or 1
        self.WIDTH, self.HEIGHT = 800 * self.multiplier, 450 * self.multiplier
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("i cant take this anymore")

        self.font = pygame.font.Font("font/font.otf", int(36 * self.multiplier))
        # game board
        self.local_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.current_player = 1
        
        # game images
        self.total = 300 * self.multiplier
        self.cell = self.total // 3
        self.board = None
        self.board_empty = None
        self.board_grid = None
        self.cross = None
        self.dot = None
        self.x_start = (self.WIDTH // 2 - self.total // 2)# * self.multiplier
        self.y_start = (self.HEIGHT // 2 - self.total // 2)# * self.multiplier

        # sounds
        self.crosses = [ pygame.mixer.Sound(self.current_dir + "audio/Cross_1.mp3"), pygame.mixer.Sound(self.current_dir + "audio/Cross_2.mp3") ]
        self.circles = [ pygame.mixer.Sound(self.current_dir + "audio/Circle_1.mp3"), pygame.mixer.Sound(self.current_dir + "audio/Circle_2.mp3") ]
        self.impact = pygame.mixer.Sound(self.current_dir + "audio/impact_game_won.mp3")
        self.bgm = pygame.mixer.music.load(self.current_dir + "audio/bgm.mp3")
        pygame.mixer.music.set_volume(0.8)

    def setup_board(self):
        #load images
        self.board = pygame.image.load("graphics/board.png")
        size = self.board.get_size()
        self.board = pygame.transform.scale(self.board, (size[0] * self.multiplier, size[1] * self.multiplier)) 
        self.board_empty = pygame.image.load("graphics/board_e.png")
        size = self.board_empty.get_size()
        self.board_empty = pygame.transform.scale(self.board_empty, (size[0] * self.multiplier, size[1] * self.multiplier)) 
        self.board_grid = pygame.image.load("graphics/board_grid.png")
        size = self.board_grid.get_size()
        self.board_grid = pygame.transform.scale(self.board_grid, (size[0] * self.multiplier, size[1] * self.multiplier)) 
        self.cross = pygame.image.load("graphics/cross.png")
        size = self.cross.get_size()
        self.cross = pygame.transform.scale(self.cross, (size[0] * self.multiplier, size[1] * self.multiplier)) 
        self.dot = pygame.image.load("graphics/dot.png")
        size = self.dot.get_size()
        self.dot = pygame.transform.scale(self.dot, (size[0] * self.multiplier, size[1] * self.multiplier)) 


    def update_screen(self, x_off = 0, y_off = 0, winning_player = None):
        for x in range(3):
            for y in range(3):
                if self.local_board[y][x] == 0:
                    pass
                elif self.local_board[y][x] == 1:
                    rect = self.cross.get_rect()
                    rect.x, rect.y = (self.x_start + x_off + self.cell * x), (self.y_start + y_off + self.cell * y)
                    self.screen.blit(self.cross, rect)
                elif self.local_board[y][x] == 2:
                    rect = self.dot.get_rect()
                    rect.x, rect.y = (self.x_start + x_off + self.cell * x), (self.y_start + y_off + self.cell * y)
                    self.screen.blit(self.dot, rect)
        if not winning_player:
            if self.current_player == 1:
                self.screen.blit(self.cross,(10 * self.multiplier, 10 * self.multiplier))
            elif self.current_player == 2:
                self.screen.blit(self.dot, (10 * self.multiplier, 10 * self.multiplier))

    def get_cell(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            print("x, y: ", mpos)
            for x in range(3):
                for y in range(3):
                    if mpos[0] >= (self.x_start + self.cell * x) and mpos[0] <= (self.x_start + self.cell * x + self.cell):
                        if mpos[1] >= (self.y_start + self.cell * y) and mpos[1] <= (self.y_start + self.cell * y + self.cell):
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
                choice(self.crosses).play()
                self.current_player = 2
            else:
                choice(self.circles).play()
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
                    quit()
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

            self.screen.blit(text_a, (self.WIDTH // 2 - text_a.get_width() // 2, self.HEIGHT // 2 - (36 * self.multiplier)))
            self.screen.blit(text_p, (self.WIDTH // 2 - text_p.get_width() // 2, self.HEIGHT // 2 + (36 * self.multiplier)))
            self.screen.blit(text_q, (self.WIDTH // 2 - text_p.get_width() // 2, self.HEIGHT // 2 + (108 * self.multiplier)))

            pygame.display.flip()

    # button menu
    def game_menu1(self):                                # Set up fonts
        menu_buttons = []
        # (self, x, y, width, hight, size, font, text, mode):
        button_a = Button(self.WIDTH // 2, self.HEIGHT // 2 - 75 * self.multiplier, 0, 0, 0, self.font, "AI mode", Game_Type.GAME_TYPE_AI)
        menu_buttons.append(button_a)
        button_p = Button(self.WIDTH // 2, self.HEIGHT // 2 + 0 * self.multiplier, 0, 0, 0, self.font, "PvP", Game_Type.GAME_TYPE_PVP)
        menu_buttons.append(button_p)
        button_q = Button(self.WIDTH // 2, self.HEIGHT // 2 + 75 * self.multiplier, 0, 0, 0, self.font, "Quit", Game_Type.GAME_TYPE_QUIT)
        menu_buttons.append(button_q)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
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
                if event.type == pygame.MOUSEBUTTONUP:
                    mpos = pygame.mouse.get_pos()
                    for button in menu_buttons:
                        mode = button.click(mpos)
                        if mode:
                            return mode

            self.screen.blit(self.board_empty, (0,0))
            for button in menu_buttons:
                button.display(self.screen)

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
        print("PvP")
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
        print("AI")
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
    
    def game_online(self):
        conn = client.TicTacToeClient('139.162.200.195', 5555)
        def cust_ev():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    conn.close_conn()
                    quit()
                pos = self.get_cell(event)
                if pos:
                    conn.send(pos)
        print("online")
        self.local_board = conn.return_board()
        self.current_player = conn.return_player_nuber()
        bg_rect = self.board.get_rect()
        game_on = True
        winning_player = 0
        while game_on:
            cust_ev()
            self.local_board = conn.return_board()
            game_on = conn.ongoing
            self.screen.blit(self.board, bg_rect)
            self.update_screen()
            pygame.display.flip()
            game_on = conn.ongoing
            if conn.wp != 0:
                break
        print(f"player {conn.wp} won!")
        self.winning_player_screen(int(conn.wp))
        return winning_player




    def winning_player_screen(self, winning_player):
        if winning_player > 2:
            text = self.font.render(f"Draw", True, (255,0,0))
        elif winning_player == 2 or winning_player == 1:
            text = self.font.render(f"player {winning_player} won", True, (255,0,0))
        bg_rect = self.board.get_rect()
        self.impact.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("quitting winning screen")
                        return
            self.screen.blit(self.board_empty, bg_rect)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT - (50 * self.multiplier)  ))
            self.screen.blit(self.board_grid, (0, -50))
            self.update_screen(0, -50, winning_player)
            pygame.display.flip()
            

    def main(self):
        app_on = True
        pygame.mixer.music.play(-1)
        self.setup_board()
        while app_on:
            print(f"ai: {Game_Type.GAME_TYPE_AI}, pvp: {Game_Type.GAME_TYPE_PVP}, quit: {Game_Type.GAME_TYPE_QUIT}") 
            mode = self.game_menu1()
            print(f"mode: {mode}")
            
            if mode == Game_Type.GAME_TYPE_AI:
                self.game_online() # temp online,, should be ai
            elif mode == Game_Type.GAME_TYPE_PVP:
                self.game_pvp()
            elif mode == Game_Type.GAME_TYPE_QUIT:
                app_on = False
                break
            else:
                print(f"invalid mode {mode}")
                app_on = False
        pygame.quit()
        quit()
       
if __name__ == '__main__':
    pygame.init()
    game = Game(800, 450)
    game.main()
