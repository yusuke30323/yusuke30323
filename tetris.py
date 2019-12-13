#cd ~/Desktop/python_lesson python tetris.py

import pygame
import random

pygame.font.init()


#windowの大きさ
s_width = 800
s_height = 700


#プレイエリアの大きさ
#10 x 20 square grid
#// 切り捨て割り算
play_width = 300 #300 // 10 = 30 width per block
play_height = 600 #600 // 20 = 30 height per block
block_size = 30


#プレイエリアの位置
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


#形
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


#色
#文字と（）がそれぞれ対応する
#libraryを作らなくてもいい
shapes = [S, Z, I, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


#それぞれのブロックを呼び出す
#defはmethodと呼ばれる
#always put 'self' for the first argument
class Piece(object):
    def __init__(self, x, y, shape): #__init__を使うとinstanceを作ると同時にcallできる
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)] #それぞれの色を呼び出せる
        self.rotation = 0 #１つ目の形からスタート


#マスの作成
def create_grid(locked_pos = {}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)] #0,0,0は黒色、１０コのマス*２０列
#? # ブロックがくるとマスの色が変わる様に
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
        return grid


#?#ブロックの形を認識させる
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] #回転とブロックの形を対応させる

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
         if pos not in accepted_pos:
             if pos[1] > -1:  #下限を作る
                 return False
    return True


#y＝０で終了
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False




# どのブッロクの形が来るかランダムに設定
def get_shape():
    return Piece(5, 0, random.choice(shapes)) #pieceの初期の位置、classのx,y,shapeに入れられる


#?#マスの線の表示
def draw_grid(surface,grid):
    sx = top_left_x #sx stands for start x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size)) #20の平行線
        for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx, sy + play_height))#10の垂直線



#windowの表示 #マスと赤い境界線の表示
def draw_window(surface, grid):
    surface.fill((0,0,0)) #画面を黒で塗りつぶし

    pygame.font.init() #フォントモジュールの初期化
    font = pygame.font.SysFont('comicsans', 60) #フォントタイプと大きさの設定
    label = font.render('Tetris', 1, (255, 255, 255)) #文字と色の設定、255は白、１は意味ない

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30)) #blitで描画できる、位置の指定も

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size),0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height),4)
    draw_grid(surface, grid)
    pygame.display.update()


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run  = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1 #動いてない様に調整
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1 #軸を動かす
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(win,grid)

        if check_lost(locked_positions):
            run = False
    pygame.display.quit()


def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
