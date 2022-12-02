import pyxel

COLOR_BLACK      = 0
COLOR_NAVY       = 1
COLOR_PURPLE     = 2
COLOR_GREEN      = 3
COLOR_BROWN      = 4
COLOR_DARK_BLUE  = 5
COLOR_LIGHT_BLUE = 6
COLOR_WHITE      = 7
COLOR_RED        = 8
COLOR_ORANGE     = 9
COLOR_YELLOW     = 10
COLOR_LIME       = 11
COLOR_CYAN       = 12
COLOR_GRAY       = 13
COLOR_PINK       = 14
COLOR_PEACH      = 15

BG_COLOR = COLOR_PEACH

class PyxelText:
  def __init__(self, pos_x, pos_y, word, color):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.word = word
    self.color = color
  
  def print(self):
    pyxel.text(self.pos_x, self.pos_y, self.word, self.color)

class PyxelDoubledText(PyxelText):
  def __init__(self, pos_x, pos_y, word, main_color, shadow_color):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.word = word
    self.main_color = main_color
    self.shadow_color = shadow_color

  def print(self):
    pyxel.text(self.pos_x + 1, self.pos_y, self.word, self.shadow_color)
    pyxel.text(self.pos_x, self.pos_y, self.word, self.main_color)

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
    pyxel.blt(self.pos_x, self.pos_y, self.imgnum, self.pos_u, self.pos_v, self.width, self.height, BG_COLOR)

class Penguin(PyxelImage):
  def __init__(self, pos_x, pos_y, pos_u, pos_v):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.imgnum = 0
    self.pos_u = pos_u
    self.pos_v = pos_v
    self.width = 16
    self.height = 16

  def walk_right(self):
    return Penguin(self.pos_x + 1, self.pos_y, pyxel.frame_count % 4 * 16, 0)
 
  def walk_left(self):
    return Penguin(self.pos_x - 1, self.pos_y, pyxel.frame_count % 4 * 16, 16)

class App:
  def __init__(self):
    pyxel.init(128, 128, title = "Birthday Penguin")
    pyxel.load("assetes/penguin.pyxres")

    self.title = PyxelImage(0, 0, 1, 128, 0, 128, 128)
    self.score = PyxelDoubledText(30, 4, "35", COLOR_ORANGE, COLOR_BROWN)
    self.penguin = Penguin(64, 106, 0, 0)

    pyxel.run(self.update, self.draw)

  def update(self):
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()

    if pyxel.btn(pyxel.KEY_LEFT):
      self.penguin = self.penguin.walk_left()
    if pyxel.btn(pyxel.KEY_RIGHT):
      self.penguin = self.penguin.walk_right()

  def draw(self):
    pyxel.cls(BG_COLOR)
    self.title.print()
    self.score.print()
    self.penguin.print()

if __name__ == "__main__":
  App()