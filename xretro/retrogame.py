from pygame.sprite import LayeredDirty


class Game:

    def __init__(self, title, w, h):
        self.title = title
        self.w = w
        self.h = h
        self.all_actors: LayeredDirty = LayeredDirty()

    def add_actor(self, actor, lay: int):
        self.all_actors.add(actor, layer=lay)
        actor.game = self

    def update_all(self):
        self.all_actors.update()

    def draw_all(self, surf):
        self.all_actors.draw(surf)
