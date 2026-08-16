import random
from ursina import (
    Audio,
    Color,
    Entity,
    Text,
    Ursina,
    application,
    camera,
    color,
    destroy,
    distance,
    mouse,
    time,
)
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# プレイヤー（マインクラフト風の一人称視点コントローラー）
player = FirstPersonController(position=(0, 1, 0), speed=7)

# 画面中央のクロスヘア（採掘対象を狙う目印）
crosshair = Entity(
    parent=camera.ui, model="quad", color=color.white, scale=0.006
)

# 地面
ground = Entity(
    model="plane",
    color=color.gray,
    scale=(20, 1, 20),
    position=(0, -1, 0),
    collider="box",  # プレイヤーが乗れるように当たり判定を追加
)

# スコア表示
score = 0
score_text = Text(text=f"Score: {score}", position=(-0.85, 0.45), scale=2)

# コインと障害物のグループ
coins = []
obstacles = []


# コインをランダム生成する関数
def spawn_coin():
    coin = Entity(
        model="sphere",
        color=color.gold,
        scale=0.8,
        position=(random.uniform(-8, 8), 0, random.uniform(-8, 8)),
        collider="sphere",  # 当たり判定を追加
    )
    coins.append(coin)


# 障害物をランダム生成する関数
def spawn_obstacle():
    obs = Entity(
        model="cube",
        color=color.red,
        scale=(1, 2, 1),
        position=(random.uniform(-8, 8), 0, random.uniform(-8, 8)),
        collider="box",  # 当たり判定を追加
    )
    obstacles.append(obs)


# 初期配置
for _ in range(5):
    spawn_coin()
for _ in range(3):
    spawn_obstacle()


# 毎フレームの更新処理
def update():
    global score

    # --- 1. 当たり判定（コイン獲得） ---
    for coin in coins[:]:
        if distance(player.position, coin.position) < 1:  # プレイヤーと接触したか
            score += 10
            score_text.text = f"Score: {score}"
            coins.remove(coin)
            destroy(coin)  # 画面から削除
            spawn_coin()  # 新しいコインを生成

    # --- 2. 当たり判定（障害物接触） ---
    for obs in obstacles:
        if distance(player.position, obs.position) < 1:
            player.color = color.black  # ゲームオーバー演出
            print("Game Over!")


# コインを採掘（左クリック）する関数
def mine_coin():
    global score

    target = mouse.hovered_entity
    if target not in coins:
        return
    if distance(player.position, target.position) > 4:  # 採掘可能距離を超えている
        return

    score += 10
    score_text.text = f"Score: {score}"
    coins.remove(target)
    destroy(target)
    spawn_coin()


# ESCキーでゲームを終了、左クリックでコインを採掘
def input(key):
    if key == "escape":
        application.quit()
    if key == "left mouse down":
        mine_coin()


app.run()