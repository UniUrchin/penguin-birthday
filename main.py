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

SYSTEM_BG_COLOR = COLOR_PEACH

SWEETS_DONUT     = 0
SWEETS_SHORTCAKE = 1

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
    pyxel.blt(self.pos_x, self.pos_y, self.imgnum, self.pos_u, self.pos_v, self.width, self.height, SYSTEM_BG_COLOR)

class Score(PyxelDoubledText):
  def print(self):
    pyxel.text(self.pos_x + 1, self.pos_y, str(self.word), self.shadow_color)
    pyxel.text(self.pos_x, self.pos_y, str(self.word), self.main_color)


class Penguin(PyxelImage):
  def __init__(self, pos_x, pos_y, pos_u, pos_v):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.imgnum = 0
    self.pos_u = pos_u
    self.pos_v = pos_v
    self.width = 16
    self.height = 16

  # 外側に出ないようにする処理が必要...
  def walk_right(self):
    return Penguin(self.pos_x + 1, self.pos_y, pyxel.frame_count % 4 * 16, 0)
  
  # 外側に出ないようにする処理が必要...
  def walk_left(self):
    return Penguin(self.pos_x - 1, self.pos_y, pyxel.frame_count % 4 * 16, 16)

class Sweets(PyxelImage):
  def __init__(self, pos_x, pos_y, pos_u, pos_v):
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.imgnum = 0
    self.pos_u = pos_u
    self.pos_v = pos_v
    self.width = 16
    self.height = 16

  # pos_u, pos_vの組み合わせで挙動を変える
  def fall_down(self):
    return Sweets(self.pos_x, self.pos_y + 1, self.pos_u, self.pos_v)

  def is_inside_screen(self):
    return True if self.pos_y < pyxel.height else False

  def is_touched(self, pos_x, pos_y):
    return True if pos_x - 16 < self.pos_x < pos_x + 16 and pos_y - 16 < self.pos_y < pos_y + 16 else False

class App:
  def __init__(self):
    pyxel.init(128, 128, title = "Birthday Penguin")
    pyxel.load("assetes/penguin.pyxres")

    self.stage = PyxelImage(0, 0, 1, 128, 0, 128, 128)
    self.score = Score(30, 4, 0, COLOR_ORANGE, COLOR_BROWN)
    self.penguin = Penguin(64, 106, 0, 0)
    self.sweets_list = []

    pyxel.run(self.update, self.draw)

  def update(self):
    # キーボード入力処理

    ## Qを押すとゲームが強制終了する
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()

    ## 十字キーの左右でぺんぎんの移動 
    if pyxel.btn(pyxel.KEY_LEFT):
      self.penguin = self.penguin.walk_left()
    if pyxel.btn(pyxel.KEY_RIGHT):
      self.penguin = self.penguin.walk_right()
    
    # タイマー処理(1秒に30フレーム)

    ## 2秒(60フレーム)に一回お菓子を生成する処理
    if pyxel.frame_count % 60 == 0:
      self.sweets_list.append(Sweets(60, 0, 0, 32))

    # 毎フレームやりたい処理

    ## お菓子の移動とスクリーン外に出たお菓子の廃棄
    self.sweets_list = list(map(lambda sweets: sweets.fall_down(), self.sweets_list))
    self.sweets_list = list(filter(lambda sweets: sweets.is_inside_screen(), self.sweets_list))

    # お菓子の接触判定(スコアの加算処理もやる)
    self.sweets_list = list(filter(lambda sweets: self.update_score(sweets), self.sweets_list))

  def update_score(self, sweets):
    if sweets.is_touched(self.penguin.pos_x, self.penguin.pos_y):
      if sweets.pos_u % 16 == 0:
        self.score = Score(30, 4, self.score.word + 100, COLOR_ORANGE, COLOR_BROWN)
      if sweets.pos_u % 16 == 1:
        self.score = Score(30, 4, self.score.word + 200, COLOR_ORANGE, COLOR_BROWN)
      return False
    else:
      return True

  def draw(self):
    pyxel.cls(SYSTEM_BG_COLOR)

    self.stage.print()

    for sweets in self.sweets_list:
      sweets.print()

    self.score.print()
    self.penguin.print()


if __name__ == "__main__":
  App()