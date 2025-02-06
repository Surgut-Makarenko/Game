import sys
import pygame
import os
import random as rand
import main, test

FPS = 50
clock = pygame.time.Clock()
player = None

size = WIDTH, HEIGHT = 1550, 550
screen = pygame.display.set_mode(size)
screen.fill('white')


def lose_screen():
    intro_text = ["YOU LOSE", "",
                  "УВЫ",
                  "ВАША МИССИЯ ПРОВАЛЕНА",
                  "ПОПРОБУЙТЕ ЕЩЁ РАЗ"]

    fon = pygame.transform.scale(load_image('wsity.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#C711E0'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.coords = [pos_x, pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(star_group, all_sprites)
        self.image = star_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        pass
        if pygame.sprite.spritecollideany(self, player_group):
            pygame.mixer.music.stop()
            return star_screen()


def star_screen():
    intro_text = ["FINISH", "",
                  "Ваша миссия выполнена! ",
                  "Большая честь работать с вами.",
                  "Для того, чтобы начать заново, нажмите TAB."]
    fon = pygame.transform.scale(load_image('end.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    pygame.mixer.music.load(r"data/Project_32.wav")
    pygame.mixer.music.play(-1)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.key == pygame.K_TAB:
                    return main.main()
        pygame.display.flip()
        clock.tick(FPS)


class Evil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(evil_group, all_sprites)
        self.image = evil_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        self.now_rect = self.rect
        randi = rand.randint(1, 4)
        if randi == 1:
            self.left()
        elif randi == 2:
            self.right()
        elif randi == 3:
            self.up()
        elif randi == 4:
            self.down()
        if pygame.sprite.spritecollideany(self, player_group):
            player.reti()
            return lose_screen()

    def left(self):
        self.rect = self.image.get_rect().move(tile_width * (self.pos_x - 1) + 15, tile_height * self.pos_y + 5)
        if not pygame.sprite.spritecollideany(self, walls_group):
            self.pos_x -= 1
        else:
            self.rect = self.now_rect

    def right(self):
        self.rect = self.image.get_rect().move(tile_width * (self.pos_x + 1) + 15, tile_height * self.pos_y + 5)
        if not pygame.sprite.spritecollideany(self, walls_group):
            self.pos_x += 1
        else:
            self.rect = self.now_rect

    def up(self):
        self.rect = self.image.get_rect().move(tile_width * (self.pos_x) + 15,
                                                tile_height * (self.pos_y - 1) + 5)
        if not pygame.sprite.spritecollideany(self, walls_group):
            self.pos_y -= 1
        else:
            self.rect = self.now_rect

    def down(self):
        self.rect = self.image.get_rect().move(tile_width * (self.pos_x) + 15,
                                                tile_height * (self.pos_y + 1) + 5)
        if not pygame.sprite.spritecollideany(self, walls_group):
            self.pos_y += 1
        else:
            self.rect = self.now_rect


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.coords = [pos_x, pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def reti(self):
        self.rect = self.image.get_rect().move(tile_width * self.coords[0], tile_height * self.coords[1])
        self.pos_x, self.pos_y = self.coords

    def update(self, *args):
        xcrd, ycrd = self.coords
        if args:
            now_rect = self.rect
        if args[0].key == pygame.K_LEFT:
            self.rect = self.image.get_rect().move(tile_width * (self.pos_x - 1) + 15, tile_height * self.pos_y + 5)
            if not pygame.sprite.spritecollideany(self, walls_group):
                self.pos_x -= 1
                #camera.update(self, -tile_width//2, 0)
            else:
                self.rect = now_rect
        elif args[0].key == pygame.K_RIGHT:
            self.rect = self.image.get_rect().move(tile_width * (self.pos_x + 1) + 15, tile_height * self.pos_y + 5)
            if not pygame.sprite.spritecollideany(self, walls_group):
                self.pos_x += 1
                #camera.update(self, tile_width//2, 0)
            else:
                self.rect = now_rect
        elif args[0].key == pygame.K_UP:
            self.rect = self.image.get_rect().move(tile_width * (self.pos_x) + 15,
                                                tile_height * (self.pos_y - 1) + 5)
            if not pygame.sprite.spritecollideany(self, walls_group):
                self.pos_y -= 1
                #camera.update(self, 0, -tile_height//2)
            else:
                self.rect = now_rect
        elif args[0].key == pygame.K_DOWN:
            self.rect = self.image.get_rect().move(tile_width * (self.pos_x) + 15,
                                                tile_height * (self.pos_y + 1) + 5)
            if not pygame.sprite.spritecollideany(self, walls_group):
                self.pos_y += 1
                #camera.update(self, 0, tile_height//2)
            else:
                self.rect = now_rect


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    new_evil = []
    star = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                new_evil.append(Evil(x, y))
            elif level[y][x] == '*':
                Tile('empty', x, y)
                star = Star(x, y)
    return new_player, x, y, new_evil, star


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png', -1)
evil_image = load_image('evil.png', -1)
star_image = load_image('star.jpg')
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
evil_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
level1 = load_level('lev3.txt')
player, level_x, level_y, ev, st = generate_level(load_level('lev3.txt'))
muslst = ['backfire', 'bitter friend', 'guilt', 'look at me', 'nights', 'on the verge']


def chain():
    pygame.init()
    pygame.display.set_caption('Передвижение героя')
    tile_width = tile_height = 50
    width = len(level1[0] * tile_width)
    height = len(level1 * tile_height)
    screen.fill('white')
    v = 20  # пикселей в секунду
    clock = pygame.time.Clock()
    pygame.mixer.music.load("data" + "/" + rand.choice(muslst) + ".mp3")
    pygame.mixer.music.play()
    walls_group.add([wall for wall in tiles_group.sprites() if wall.tile_type == 'wall'])
    while True:
        screen.fill('black')
        h = False
        tiles_group.draw(screen)
        player_group.draw(screen)
        evil_group.draw(screen)
        star_group.draw(screen)
        clock.tick(v)
        for event in pygame.event.get():
            if event.type != pygame.QUIT:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        h = True
                        loh = event
                else:
                    h = False
            else:
                pygame.quit()
        if h == True:
            player.update(loh)
            for e in ev:
                e.update()
            st.update()
        pygame.display.flip()