import pyxel

BG_COLOR = 7

class PyxelText:
  def __init__(self, pos_x, pos_y, word, color):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.word = word
    self.color = color
  
  def print(self):
    pyxel.text(self.pos_x, self.pos_y, self.word, self.color)

class PyxelRainbowText(PyxelText):
  def roop_color(self):
    return PyxelRainbowText(self.pos_x, self.pos_y, self.word, pyxel.frame_count % 16)

class PyxelImage:
  def __init__(self, pos_x, pos_y, imgnum, pos_u, pos_v, width, height):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.imgnum = imgnum
    self.pos_u = pos_u
    self.pos_v = pos_v
    self.width = width
    self.height = height

  def print(self):
    pyxel.blt(self.pos_x, self.pos_y, self.imgnum, self.pos_u, self.pos_v, self.width, self.height)

class PyxelPenguinImage(PyxelImage):
  def dance_animation(self):
    if pyxel.frame_count % 15 != 0: return self
    if self.pos_u == 0:
      return PyxelPenguinImage(self.pos_x, self.pos_y, self.imgnum, self.pos_u + 16, self.pos_v, self.width, self.height)
    else:
      return PyxelPenguinImage(self.pos_x, self.pos_y, self.imgnum, self.pos_u - 16, self.pos_v, self.width, self.height)

class App:
  def __init__(self):
    pyxel.init(160, 128, title = "Hello Penguin")
    pyxel.load("assetes/main.pyxres")

    self.title = PyxelRainbowText(52, 50, "Hello Penguin!!", 0)
    self.penguin = PyxelPenguinImage(72, 60, 0, 0, 0, 16, 16)

    pyxel.run(self.update, self.draw)

  def update(self):
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()
    self.title = self.title.roop_color()
    self.penguin = self.penguin.dance_animation()

  def draw(self):
    pyxel.cls(BG_COLOR)
    self.title.print()
    self.penguin.print()

if __name__ == "__main__":
  App()