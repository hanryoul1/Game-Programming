# Cocos2d 입문
# https://alegruz.imweb.me/blog/?q=YToyOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjtzOjc6ImtleXdvcmQiO3M6NDoiY29jbyI7fQ%3D%3D&bmode=view&idx=243177&t=board

import cocos

class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super(MainLayer, self).__init__()
        self.label = cocos.text.Label(
            'Hello, World!',
            font_name = 'Times New Roman',
            font_size = 32,
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.label.position = (320, 240)
        self.add(self.label)

if __name__ == '__main__':
    cocos.director.director.init(caption = 'Hello, World!')
    layer = MainLayer()
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)