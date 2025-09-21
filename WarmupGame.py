import pygame
from pygame.locals import *
import sys
import random

pygame.init()

info = pygame.display.Info() # 1536 864
WIDTH, HEIGHT = info.current_w, info.current_h - 50 # 1536 814
DISPLAY_SURFACE = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

background = pygame.image.load("bg.png").convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

pygame.display.set_caption('Horse Racing')
clock = pygame.time.Clock()
font = pygame.font.SysFont("C:/Users/caomi/source/repos/Python/Warmupgame/[Taimienphi.vn]Font-Arial/SVN-Arial Regular.ttf", 30)
alt_font = pygame.font.Font("C:/Users/caomi/source/repos/Python/Warmupgame/KoushikiSans/KoushikiSans-Regular.ttf", 40)

GAME_TIME = 600000
frozen_time = 0


finish_line = WIDTH - 150
race_length = finish_line - 150



# --------------------------------------------------------------------------------
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


    def move(self):
        if self.finished:
            return

        self.x += self.steps[self.index]
        self.index += 1

        if self.index >= len(self.steps):
            self.finished = True


    def draw(self):
        # draw track line
        pygame.draw.line(
            DISPLAY_SURFACE,
            (100, 100, 100),
            (100, self.y + 50),
            (finish_line + 50, self.y + 50)
            )
        # draw horse
        DISPLAY_SURFACE.blit(self.image, (self.x, self.y))

# --------------------------------------------------------------------------------
# Functions

def scale(img, base_scale):
    width, height = img.get_size()
    scale = base_scale / max(width, height)
    new_size = (int(width * scale), int(height * scale))
    return pygame.transform.smoothscale(img, new_size)


# def drawFinishline():
#     pygame.draw.line(
#         DISPLAY_SURFACE,
#         (255, 255, 255),
#         (finish_line, 200),
#         (finish_line, info.current_h),
#         width = 4
#     )


def generateSteps():
    step_weights = [random.uniform(0.5, 1.5) for _ in range(10)]
    total_weights = sum(step_weights)
    plan = [int(weight / total_weights * race_length) for weight in step_weights]

    diff = race_length - sum(plan)
    for i in range(diff):
        plan[i % 10] += 1

    plan[-1] = race_length - sum(plan[:-1])
    return plan


def drawTimer():
    global winner
    global frozen_time
    now = pygame.time.get_ticks()
    if not winner:
        main_timer = max(0, GAME_TIME - now)
    else:
        main_timer = max(0, GAME_TIME - (frozen_time if frozen_time else now)) # miliseconds

    if not winner:
        if not questions or now >= GAME_TIME:
            frozen_time = now
            highest_val = max(h.x for h in horses)
            winners = [h for h in horses if h.x == highest_val]
            winner = winners if len(winners) > 1 else winners[0]

    main_min = main_timer // 60000
    main_sec = (main_timer % 60000) // 1000

    timer_txt = alt_font.render(f"{main_min:02}:{main_sec:02}", True, (255,255,255))
    DISPLAY_SURFACE.blit(timer_txt, (WIDTH-230, 37))


def drawWinningBanner(winner: Horse|list[Horse], x_pos:int):
    img = pygame.image.load("tie.jpg" if isinstance(winner,list) else "1st.jpg").convert_alpha()
    img = scale(img,200)
    img.set_colorkey((0,0,0))

    banner = pygame.Surface((WIDTH,300), SRCALPHA)
    banner.fill((0,0,0,180))

    text = ""
    name_list = []
    if isinstance(winner,list):
        for horse in winner:
            name_list.append(horse.team)
        text = ", ".join(name_list) + " Tied!"
    else:
        text = f"{winner.team} Wins!"

    text = alt_font.render(text, True, (255, 215, 0))
    text_rect = text.get_rect(center= (WIDTH//2, 150))
    img_rect = img.get_rect(center= (WIDTH//2, 150))
    text_rect.y += 100
    img_rect.y -= 30

    banner.blit(img,img_rect)
    banner.blit(text,text_rect)

    DISPLAY_SURFACE.blit(banner, (x_pos, HEIGHT//2 - 150))


def getTeamNames(num):
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
        prompt = font.render(f"Input Horse's team {len(names) + 1 if len(names) < 4 else 4}:", True, (255, 255, 255))
        input_text = font.render(current, True, (255, 215, 0))
        DISPLAY_SURFACE.blit(prompt, (100, HEIGHT // 2 - 40))
        DISPLAY_SURFACE.blit(input_text, (100, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(30)
    return names


def drawQuestion(qdata:dict):
    question_txt = font.render(qdata["q"],True,(255,255,255))
    DISPLAY_SURFACE.blit(question_txt, (200, 70))

    for i,option in enumerate(qdata["options"]):
        option_txt = font.render(option,True,(255,255,255))
        col = i % 2
        row = i // 2
        DISPLAY_SURFACE.blit(option_txt,(220 + col*300, 120 + row*50))


# --------------------------------------------------------------------------------
# Setup

team_names = getTeamNames(4)

horses = [
    Horse(pygame.image.load(f"hors{i+1}.png").convert_alpha(), 320 + 100 * i, team_names[i])
    for i in range(4)
]

# --------------------------------------------------------------------------------
# Questions

questions = [
    {
        "q": "Con vật nào là loài động vật lớn nhất trên Trái Đất?",
        "answer": "A. Cá voi xanh",
        "options": ["A. Cá voi xanh", "B. Voi", "C. Cá mập", "D. Gấu bắc cực"]
    },
    {
        "q": "Quốc gia nào có diện tích lớn nhất thế giới?",
        "answer": "C. Nga",
        "options": ["A. Hoa Kỳ", "B. Trung Quốc", "C. Nga", "D. Canada"]
    },
    {
        "q": "Thủ đô của Pháp là gì?",
        "answer": "B. Paris",
        "options": ["A. London", "B. Paris", "C. Berlin", "D. Rome"]
    },
    {
        "q": "Quốc gia nào là nơi sản xuất cà phê lớn nhất thế giới?",
        "answer": "A. Brazil",
        "options": ["A. Brazil", "B. Colombia", "C. Việt Nam", "D. Ấn Độ"]
    },
    {
        "q": "Bộ môn thể thao nào được coi là 'vua của các môn thể thao'?",
        "answer": "A. Bóng đá",
        "options": ["A. Bóng đá", "B. Bóng rổ", "C. Quần vợt", "D. Cầu lông"]
    },
    {
        "q": "Nước nào được biết tới là có tượng nữ thần tự do?",
        "answer": "C. New York",
        "options": ["A. Paris", "B. London", "C. New York", "D. Tokyo"]
    },
    {
        "q": "Ai ghi bàn nhiều nhất lịch sử bóng đá?",
        "answer": "A. Cristiano Ronaldo",
        "options": ["A. Cristiano Ronaldo", "B. Lionel Messi", "C. Josef Bican", "D. Romário"]
    },
    {
        "q": "Nam Cao là tác giả của tác phẩm nào đã được học trong sách Ngữ văn 11?",
        "answer": "C. Chí Phèo",
        "options": ["A. Lão Hạc", "B. Vợ nhặt", "C. Chí Phèo", "D. Đời thừa"]
    },
    {
        "q": "Quê của nhà văn Kim Lân là tỉnh nào?",
        "answer": "A. Bắc Ninh",
        "options": ["A. Bắc Ninh", "B. Bắc Giang", "C. Hà Nội", "D. Hải Dương"]
    },
    {
        "q": "Bức tường Berlin dùng để làm gì?",
        "answer": "B. Ngăn cách Đông và Tây Đức",
        "options": ["A. Bảo vệ người dân Đức", "B. Ngăn cách Đông và Tây Đức", "C. Ngăn quân Pháp xâm lược", "D. Là biểu tượng hòa bình"]
    },
    {
        "q": "Bức tranh 'Đêm đầy sao' do ai vẽ?",
        "answer": "C. Vincent van Gogh",
        "options": ["A. Leonardo da Vinci", "B. Pablo Picasso", "C. Vincent van Gogh", "D. Claude Monet"]
    },
    {
        "q": "Cơ quan nào có chức năng lọc máu?",
        "answer": "D. Thận",
        "options": ["A. Tim", "B. Phổi", "C. Gan", "D. Thận"]
    },
    {
        "q": "Cơ quan nào có chức năng tống máu đi khắp cơ thể?",
        "answer": "B. Tim",
        "options": ["A. Gan", "B. Tim", "C. Não", "D. Thận"]
    },
    {
        "q": "Loài động vật nào đứng để ngủ?",
        "answer": "B. Ngựa",
        "options": ["A. Bò", "B. Ngựa", "C. Voi", "D. Hươu cao cổ"]
    },
    {
        "q": "Ngày Nhà giáo Việt Nam là ngày nào?",
        "answer": "B. 20/11",
        "options": ["A. 20/10", "B. 20/11", "C. 26/3", "D. 2/9"]
    },
    {
        "q": "Ngày 20/10 là ngày gì?",
        "answer": "B. Ngày Phụ nữ Việt Nam",
        "options": ["A. Ngày Giải phóng miền Nam", "B. Ngày Phụ nữ Việt Nam", "C. Ngày Quốc tế Lao động", "D. Ngày Quốc tế Phụ nữ"]
    }
]

# --------------------------------------------------------------------------------
# Main Loop


banner_pos = WIDTH
running = True
winner = None
current_question = None

while running: #main loop
    DISPLAY_SURFACE.blit(background,(0,0))

    for horse in horses:
        horse.draw()

    drawTimer()

    if questions and not winner:
        if not current_question in questions:
            current_question = random.choice(questions)
        drawQuestion(current_question)

    if winner:
        alt_message = "OUT OF TIME" if pygame.time.get_ticks() > GAME_TIME else ("OUT OF QUESTIONS" if not questions else None)
        if alt_message:
            alt_wintext = alt_font.render(alt_message, True, (255,0,0))
            DISPLAY_SURFACE.blit(alt_wintext, (250, 150))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if not winner and questions and pygame.time.get_ticks() < GAME_TIME:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if current_question in questions:
                        questions.remove(current_question)

                mapping = {
                    K_1: horses[0],
                    K_2: horses[1],
                    K_3: horses[2],
                    K_4: horses[3],
                }
                horse = mapping.get(event.key)

                if horse and not horse.finished:
                    horse.move()
                    if current_question in questions:
                        questions.remove(current_question)

                    if horse.finished:
                        frozen_time = pygame.time.get_ticks()
                        horse.x = finish_line
                        winner = horse
    if winner:
        banner_pos = max(0,banner_pos - 20)
        drawWinningBanner(winner,banner_pos)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()