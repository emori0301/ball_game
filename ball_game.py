import pygame
import pymunk
import sys
import random

# Pygameの初期化
pygame.init()

# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ゲームループ内での生成位置
spawn_x = 400
spawn_y = 50

# 四角形のサイズと色
spawn_rect_size = 20
spawn_rect_color = (255, 0, 0)

# ウィンドウの作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# タイトルバーの設定
pygame.display.set_caption("ボールゲーム")

# Pymunkの物理空間を作成
space = pymunk.Space()
space.gravity = (0, 900)  # 重力


# 大きさと色を対応づけるディクショナリ
circle_sizes_and_colors = {
    20: (0, 255, 0),  # 緑
    30: (255, 0, 0),  # 赤
    40: (0, 0, 255),  # 青
    50: (255, 255, 0),  # 黄色
    60: (255, 0, 255),  # マゼンタ
    70: (0, 255, 255),  # シアン
    80: (128, 0, 0),  # 暗赤
    90: (0, 128, 0),  # 暗緑
    100: (0, 0, 128),  # 暗青
    110: (128, 128, 128)  # グレー
}

# スコアの初期化
score = 0

# 衝突ハンドリング関数
def collision_handler(arbiter, space, data):
    global score  # スコアをグローバル変数として使用
    global game_over  # ゲームオーバーの状態

    circle1, circle2 = arbiter.shapes  # 衝突した2つの円を取得
    if hasattr(circle1, 'color') and hasattr(circle2, 'color'):
        if circle1.color == circle2.color and circle1.radius == circle2.radius:  # 同じ色で同じサイズの円同士が衝突した場合
            # 2つの円の中心座標を取得
            center_x = (circle1.body.position.x + circle2.body.position.x) / 2
            center_y = (circle1.body.position.y + circle2.body.position.y) / 2

            if circle1.radius < 110:
                # 次の大きさの円の半径と色を取得
                next_radius = circle1.radius + 10  # 10を加えて次の大きさにする例
                next_color = circle_sizes_and_colors.get(next_radius, (128, 128, 128))  # デフォルトはグレー

                # スコアの計算と更新
                if next_radius  == 20:  # サイズが20の倍数の場合
                    score += 5
                elif next_radius == 30:
                    score += 10
                elif next_radius == 40:
                    score += 15
                elif next_radius == 50:
                    score += 20
                elif next_radius == 60:
                    score += 25
                elif next_radius == 70:
                    score += 30
                elif next_radius == 80:
                    score += 35
                elif next_radius == 90:
                    score += 40
                elif next_radius == 100:
                    score += 45
                elif next_radius == 110:
                    score += 50
                
                else:
                    score += 1
            
                # 新しい円を作成
                inertia = pymunk.moment_for_circle(1, 0, next_radius, (0, 0))
                body = pymunk.Body(1, inertia)
                body.position = center_x, center_y
                shape = pymunk.Circle(body, next_radius, (0, 0))
                shape.color = next_color  # 色を設定
                space.add(body, shape)

            # 衝突して消える円を削除
            space.remove(circle1.body, circle1)
            space.remove(circle2.body, circle2)

    return True

# 衝突ハンドラを設定
handler = space.add_collision_handler(0, 0)
handler.begin = collision_handler

# スコア表示用のフォントとテキストの色を設定
font = pygame.font.Font('font/kkm_analogtv_v2.ttf', 36)
font_big = pygame.font.Font('font/kkm_analogtv_v2.ttf', 72)
font_small = pygame.font.Font('font/kkm_analogtv_v2.ttf', 18)
text_color = (255, 255, 255)

# プレビュー用の変数を初期化
preview_circle_radius = random.choice([20, 30, 40, 50])  # ランダムな半径を選択
preview_circle_color = circle_sizes_and_colors[preview_circle_radius]
preview_circle_x = SCREEN_WIDTH - 100  # 右上に表示

# プレビューを描画する関数
def draw_preview_circle(surface, radius, color, x, y):
    pygame.draw.circle(surface, color, (x, y), radius)

circle_x = 400
circle_falling = False

# ゲームオーバーの状態を示す変数
game_over = False

left_speed = 10
right_speed = 10

index = 0

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
            if event.key == pygame.K_w:
                screen = pygame.display.set_mode((800, 600))

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:
                spawn_x -= left_speed
            if event.key == pygame.K_RIGHT:
                spawn_x += right_speed
            if spawn_x < 220 :
                left_speed = 0
            if 570 < spawn_x :
                right_speed = 0
            if 220 < spawn_x < 570 :
                left_speed = 10
                right_speed = 10
            if index == 0:
                if event.key == pygame.K_SPACE:
                    index += 1
                    if pygame.mixer.music.get_busy() == 0:
                        pygame.mixer.music.load('sound/intro.ogg')
                        pygame.mixer.music.set_volume(0.1)
                        pygame.mixer.music.play(-1)
            if index == 1:
                if event.key == pygame.K_SPACE and not circle_falling and not game_over and index != 0:
                    circle_falling = True
                    circle_radius = preview_circle_radius  # プレビューと同じ半径を使用
                    circle_color = preview_circle_color 
                    circle_x = spawn_x  # 四角形の位置に円を生成

                    # 新しいプレビューを生成
                    preview_circle_radius = random.choice([20, 30, 40, 50])  # ランダムな半径を選択
                    preview_circle_color = circle_sizes_and_colors[preview_circle_radius]
                
                    # Pymunkの物理オブジェクトとして円を追加
                    inertia = pymunk.moment_for_circle(1, 0, circle_radius, (0, 0))
                    body = pymunk.Body(1, inertia)
                    body.position = circle_x, circle_radius
                    shape = pymunk.Circle(body, circle_radius, (0, 0))
                    shape.color = circle_color  # 色を設定
                    space.add(body, shape)
            
        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_SPACE:
                circle_falling = False

    if index == 0:
        screen.fill((231, 255, 231))
        TITLE = font_big.render("BALL GAME", True, (136, 160, 32))
        screen.blit(TITLE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100))
        # リトライメッセージを表示
        start_text = font.render("PRESS SPACE TO START", True, (136, 160, 32))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 + 50))


    if index == 1:
        # ゲームオーバーの条件
        if not game_over:
            for shape in space.shapes:
                if isinstance(shape, pymunk.Circle):
                    if shape.body.position.y < 0:
                        game_over = True
                        break  # ゲームオーバー条件が一度満たされたらループを抜ける

        # ゲームオーバー条件のチェック
        if game_over:
            screen.fill((21,105,189))
            game_over_text = font_big.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 100))
            # スコアを表示
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
            
            # リトライメッセージを表示
            retry_text = font.render("Press SPACE to Retry", True, (255, 255, 255))
            screen.blit(retry_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 100))

            # スペースキーが押されたらゲームをリセット
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # ゲームをリセット
                game_over = False
                score = 0
                space = pymunk.Space()
                space.gravity = (0, 900)
                
        else:
            # 画面をクリア
            screen.fill((255, 231, 189))
            # screen.fill((237, 201, 81))
            pygame.draw.rect(screen,(189, 147, 21),(0,400,2000,400))
            point = [(200,100),(280,50),(520,50),(600,100),(600,550),(200,550)]
            pygame.draw.polygon(screen,(231, 255, 231), point)
            point2 = [(200,100),(280,50),(520,50),(600,100)]
            pygame.draw.polygon(screen,(189, 231, 189), point2)
            pygame.draw.line(screen, (105,189,189), (200,100), (200,550), width=5)
            pygame.draw.line(screen, (105,189,189), (600,100), (600,550), width=5)
            pygame.draw.line(screen, (105,189,189), (200,550), (600,550), width=5)

            pygame.draw.line(screen, (105,189,189), (200,100), (280,50), width=5)
            pygame.draw.line(screen, (105,189,189), (280,50), (520,50), width=5)
            pygame.draw.line(screen, (105,189,189), (600,100), (520,50), width=5)

            pygame.draw.line(screen, (105,189,189), (280,50), (280,100), width=5)
            pygame.draw.line(screen, (216,224,160), (280,100), (280,500), width=5)

            pygame.draw.line(screen, (105,189,189), (520,50), (520,100), width=5)
            pygame.draw.line(screen, (216,224,160), (520,100), (520,500), width=5)

            pygame.draw.line(screen, (105,189,189), (200,100), (600,100), width=5)
            pygame.draw.line(screen, (216,224,160), (203,547), (280,500), width=5)
            pygame.draw.line(screen, (216,224,160), (597,547), (520,500), width=5)
            pygame.draw.line(screen, (216,224,160), (280,500), (520,500), width=5)

            # 画面底を表す静的なセグメントを追加
            static_ground = pymunk.Segment(space.static_body, (200,550), (600,550), 5)
            static_ground.friction = 1.0
            space.add(static_ground)

            # 画面左壁を表す静的なセグメントを追加
            static_left_wall = pymunk.Segment(space.static_body, (200,100), (200,550), 5)
            static_left_wall.friction = 1.0
            space.add(static_left_wall)

            # 画面右壁を表す静的なセグメントを追加
            static_right_wall = pymunk.Segment(space.static_body, (600,100), (600,550), 5)
            static_right_wall.friction = 1.0
            space.add(static_right_wall)

            # プレビューの円を描画
            pygame.draw.rect(screen,(189,189,189),(630,70,150,150), width=5, border_radius=30)
            score_text = font.render("Next ", True, (85,127,120))
            screen.blit(score_text, (660, 50))
            draw_preview_circle(screen, preview_circle_radius, preview_circle_color, preview_circle_x, 160)


            # Pymunkの物理オブジェクトを描画
            for shape in space.shapes:
                if isinstance(shape, pymunk.Circle):
                    pygame.draw.circle(screen, shape.color, (int(shape.body.position.x), int(shape.body.position.y)), int(shape.radius))

            # 四角形を描画
            HERO = pygame.image.load('images/allow.png')
            HERO_mini = pygame.transform.scale(HERO,(72, 72))
            screen.blit(HERO_mini, (spawn_x -38, spawn_y, spawn_rect_size, spawn_rect_size))

            # スコアを表示
            pygame.draw.rect(screen,(189,189,189),(30,70,150,150), width=5, border_radius=30)
            score_text = font.render("Score ", True, (85,127,120))
            screen.blit(score_text, (50, 50))
            score_text = font.render(str(score), True, (85,127,120))
            screen.blit(score_text, (80, 150))

            left_text = font_small.render("← key :", True, (21,21,105))
            screen.blit(left_text, (50, 250))
            left_explain_text = font_small.render("left move", True, (21,21,105))
            screen.blit(left_explain_text, (50, 280))
            right_text = font_small.render("→ key :", True, (21,21,105))
            screen.blit(right_text, (50, 350))
            right_explain_text = font_small.render("right move", True, (21,21,105))
            screen.blit(right_explain_text, (50, 380))
            space_text = font_small.render("SPACE key :", True, (21,21,105))
            screen.blit(space_text, (50, 450))
            space_explain_text = font_small.render("ball drop", True, (21,21,105))
            screen.blit(space_explain_text, (50, 480))

            ALLOW = pygame.image.load('images/sinka.png')
            ALLOW = pygame.transform.scale(ALLOW,(100, 330))
            screen.blit(ALLOW, (660,250))
            color_list =[(0, 255, 0),  # 緑
            (255, 0, 0),  # 赤
            (0, 0, 255),  # 青
            (255, 255, 0),  # 黄色
            (255, 0, 255),  # マゼンタ
            (0, 255, 255),  # シアン
            (128, 0, 0),  # 暗赤
            (0, 128, 0),  # 暗緑
            (0, 0, 128),  # 暗青
            (128, 128, 128)  # グレー
            ]
            for i ,item in enumerate(color_list):
                pygame.draw.circle(screen, item, (675+((i+1)*5), 600-((i+1)*33)), 10+(i+1)*0.6)

    # 画面を更新
    pygame.display.flip()

    # 物理シミュレーションのステップを進める
    if not game_over:
        space.step(1/60.0)  # 1/60秒ごとに更新

    # フレームレートの制御
    pygame.time.delay(16)  # 60FPS

# Pygameを終了
pygame.quit()
sys.exit()
