import pygame
from pygame.locals import *
import sys
import random
import pickle



pygame.init()

info = pygame.display.Info() # 1536 864
WIDTH, HEIGHT = info.current_w, info.current_h - 50 # 1536 814
DISPLAY_SURFACE = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

background = pygame.image.load("bg.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

pygame.display.set_caption('Horse Racing')
clock = pygame.time.Clock()
font = pygame.font.Font("DejaVuSans.ttf", 25)
alt_font = pygame.font.Font("KoushikiSans/KoushikiSans-Regular.ttf", 30)

GAME_TIME = 600000

finish_line = WIDTH - 150
race_length = finish_line - 150

# ================================================================================
# Utilities

def scale(img, base_scale):
    width, height = img.get_size()
    scale = base_scale / max(width, height)
    new_size = (int(width * scale), int(height * scale))
    return pygame.transform.smoothscale(img, new_size)


def generateSteps():
    step_weights = [random.uniform(0.5, 1.5) for _ in range(10)]
    total_weights = sum(step_weights)
    plan = [int(weight / total_weights * race_length) for weight in step_weights]

    diff = race_length - sum(plan)
    for i in range(diff):
        plan[i % 10] += 1

    plan[-1] = race_length - sum(plan[:-1])
    return plan


# ================================================================================
# Horse Class


class Horse:
    def __init__(self, image, y_pos, team):
        self.team = team
        self.image = scale(image,100)
        self.x = 100
        self.y = y_pos
        self.steps = generateSteps()
        self.index = 0
        self.finished = False


    def move(self) -> None:
        if self.finished:
            return

        self.x += self.steps[self.index]
        self.index += 1

        if self.index >= len(self.steps):
            self.finished = True


    def draw(self) -> None:
        # draw track line
        pygame.draw.line(
            DISPLAY_SURFACE,
            (100, 100, 100),
            (100, self.y + 50),
            (finish_line + 50, self.y + 50)
            )
        # draw horse
        DISPLAY_SURFACE.blit(self.image, (self.x, self.y))

# ================================================================================
# Game Class

class Game:
    with open("Questions.pkl","rb") as f:
        questions = pickle.load(f)

    # --------------------------------------------------------------------------------
    # initializing
    def __init__(self):
        self._horses:list[Horse] = [Horse(pygame.image.load(f"hors{i+1}.png").convert_alpha(), 320 + 100 * i, h) for i,h in enumerate(self._getTeamNames(4),0)]
        self._winner:list[Horse] | Horse = None
        self._frozen_time = 0
        self._banner_pos = WIDTH
        self._current_question = None

    @property
    def horses(self) -> list[Horse]:
        return self._horses

    @property
    def winner(self) -> Horse | list[Horse]:
        return self._winner
    @winner.setter
    def winner(self,horse) -> None:
        self._winner = horse

    @property
    def frozen_time(self) -> int:
        return self._frozen_time
    @frozen_time.setter
    def frozen_time(self,val) -> None:
        self._frozen_time = val


    # --------------------------------------------------------------------------------
    # Ultility method
    def _getTeamNames(self, num:int) -> list[str]:
        names = []
        current = ""
        while len(names) < num:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if current.strip():
                            names.append(current.strip())
                            current = ""
                    elif event.key == K_BACKSPACE:
                        current = current[:-1]
                    else:
                        current += event.unicode

        # draw input screen
            DISPLAY_SURFACE.fill((0, 0, 0))
            prompt = alt_font.render(f"Input Horse's team {len(names) + 1 if len(names) < 4 else 4}:", True, (255, 255, 255))
            input_text = alt_font.render(current, True, (255, 215, 0))
            DISPLAY_SURFACE.blit(prompt, (100, HEIGHT // 2 - 40))
            DISPLAY_SURFACE.blit(input_text, (100, HEIGHT // 2))
            pygame.display.flip()
            clock.tick(30)
        return names


    def resetQuestion(self) -> None:
        if self._current_question in self.questions:
            self.questions.remove(self._current_question)

    # --------------------------------------------------------------------------------
    # drawing methods
    def drawTimer(self) -> None:
        now = pygame.time.get_ticks()
        if not self._winner:
            main_timer = max(0, GAME_TIME - now)
        else:
            main_timer = max(0, GAME_TIME - (self.frozen_time if self.frozen_time else now)) # miliseconds

        if not self._winner:
            if not self.questions or now >= GAME_TIME:
                self.frozen_time = now
                highest_val = max(h.x for h in self._horses)
                self._winners = [h for h in self._horses if h.x == highest_val]
                self._winner = self._winners if len(self._winners) > 1 else self._winners[0]

        main_min = main_timer // 60000
        main_sec = (main_timer % 60000) // 1000

        timer_txt = alt_font.render(f"{main_min:02}:{main_sec:02}", True, (255,255,255))
        DISPLAY_SURFACE.blit(timer_txt, (WIDTH-230, 37))


    def drawWinningBanner(self) -> None:
        img = pygame.image.load("tie.jpg" if isinstance(self._winner,list) else "1st.jpg").convert_alpha()
        img = scale(img,200)
        img.set_colorkey((0,0,0))

        banner = pygame.Surface((WIDTH,300), SRCALPHA)
        banner.fill((0,0,0,180))

        text = ""
        name_list = []
        if isinstance(self._winner,list):
            for horse in self._winner:
                name_list.append(horse.team)
            text = ", ".join(name_list) + " Tied!"
        else:
            text = f"{self._winner.team} Wins!"

        text = alt_font.render(text, True, (255, 215, 0))
        text_rect = text.get_rect(center= (WIDTH//2, 150))
        img_rect = img.get_rect(center= (WIDTH//2, 150))
        text_rect.y += 100
        img_rect.y -= 30

        banner.blit(img,img_rect)
        banner.blit(text,text_rect)

        DISPLAY_SURFACE.blit(banner, (self._banner_pos, HEIGHT//2 - 150))
        self._banner_pos = max(0,self._banner_pos - 20)


    def drawQuestion(self) -> None:
        if self.questions and not self.winner:
            if self._current_question not in self.questions:
                self._current_question = random.choice(self.questions)

            qdata = self._current_question  # store the dict for easier access
            question_txt = font.render(qdata["q"], True, (255,255,255))
            DISPLAY_SURFACE.blit(question_txt, (200, 70))

            for i, option in enumerate(qdata["options"]):
                option_txt = font.render(option, True, (255,255,255))
                col = i % 2
                row = i // 2
                DISPLAY_SURFACE.blit(option_txt,(220 + col*300, 120 + row*50))


    def drawHorses(self) -> None:
        for horse in self.horses:
            horse.draw()


# ================================================================================
# Setup

GameSystem = Game()
running = True
current_question = None

# ================================================================================
# # Main Loop

while running: #main loop
    DISPLAY_SURFACE.blit(background,(0,0))

    GameSystem.drawHorses()
    GameSystem.drawTimer()
    GameSystem.drawQuestion()

    if GameSystem._winner: # display OUT OF TIME/OUT OF QUESTION if either conditions are met
        alt_message = "OUT OF TIME" if pygame.time.get_ticks() > GAME_TIME else ("OUT OF QUESTIONS" if not GameSystem.questions else None)
        if alt_message:
            alt_wintext = alt_font.render(alt_message, True, (255,0,0))
            DISPLAY_SURFACE.blit(alt_wintext, (250, 150))

    for event in pygame.event.get():
        if event.type == QUIT: # X check
            running = False

        #-----------------------------------------------------------------------------
        elif event.type == pygame.VIDEORESIZE:
            # update width and height
            WIDTH, HEIGHT = event.w, event.h
            DISPLAY_SURFACE = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            # rescale background
            background = pygame.transform.smoothscale(
                pygame.image.load("bg.png").convert(),
                (WIDTH, HEIGHT)
            )
        #-----------------------------------------------------------------------------

        if not GameSystem.winner and GameSystem.questions and pygame.time.get_ticks() < GAME_TIME:
            if event.type == KEYDOWN:
                # skipping question
                if event.key == K_SPACE:
                    GameSystem.resetQuestion()

                # assigning move keys
                mapping = {
                    K_1: GameSystem.horses[0],
                    K_2: GameSystem.horses[1],
                    K_3: GameSystem.horses[2],
                    K_4: GameSystem.horses[3],
                }
                horse = mapping.get(event.key)

                # move
                if horse and not horse.finished:
                    horse.move()
                    GameSystem.resetQuestion()

                    # if winner is determined -> stops timer, move horse past finish line
                    if horse.finished:
                        frozen_time = pygame.time.get_ticks()
                        horse.x = finish_line
                        GameSystem.winner = horse
    if GameSystem._winner: # draws a winning banner for the winner
        GameSystem.drawWinningBanner()

    pygame.display.flip()
    clock.tick(60) # 60 FPS


# ================================================================================
pygame.quit()
sys.exit()
