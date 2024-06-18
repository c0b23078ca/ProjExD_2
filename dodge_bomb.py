import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1000, 700 
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
    }

def look():  # 飛ぶ方向
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img2 = pg.transform.flip(kk_img, True, False)
    
    return{
    (-5, 0): kk_img,  # 0
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 2.0),  # 45
    (0, +5): pg.transform.rotozoom(kk_img2, -90, 2.0),  # 90tf
    (+5, +5): pg.transform.rotozoom(kk_img2, -50, 2.0),  # 45tf
    (+5, 0): kk_img2,  # 0tf
    (+5, -5): pg.transform.rotozoom(kk_img2, 50, 2.0),  # -45tf
    (0, -5): pg.transform.rotozoom(kk_img2, 90, 2.0),  # -90ft
    (-5, -5): pg.transform.rotozoom(kk_img, -45, 2.0),  # -45
    (0, 0): kk_img
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横の判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦の判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_imgs = look()[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb_img = pg.Surface((20, 20))  # 一辺が20のSufaceを作る 
    bomb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)  #
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center  = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k ,v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_imgs = look()[tuple(sum_mv)]
        if kk_rct.colliderect(bomb_rct):  # 衝突判定
            return  # ゲームオーバー
        screen.blit(kk_img, kk_rct)
        
        
        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bomb_img, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
