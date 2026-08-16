from ursina import Entity, Ursina, color

app = Ursina()

# 動作確認用の3Dキューブ
cube = Entity(model="cube", color=color.orange, scale=2)


def update():
    cube.rotation_y += 1


app.run()