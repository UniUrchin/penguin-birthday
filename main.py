import pyxel
import random

# Pyxelカラーパレット早見表
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

# システム変数...のつもり(後でリファクタリングする時に仕分ける)
SYSTEM_BG_COLOR = COLOR_PEACH
SYSTEM_TIME_RIMIT = 60

# お菓子の識別ナンバー
SWEETS_DONUT     = 0
SWEETS_SHORTCAKE = 1
SWEETS_PUDDING   = 2
SWEETS_SOFTCREAM = 3

# ページ遷移用変数
PAGE_MAIN_MENU     = 0
PAGE_GAME_SCREEN   = 1
PAGE_RESULT_SCREEN = 2

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

class Timer(PyxelDoubledText):
  def print(self):
    pyxel.text(self.pos_x + 1, self.pos_y, str(self.word).zfill(2), self.shadow_color)
    pyxel.text(self.pos_x, self.pos_y, str(self.word).zfill(2), self.main_color)

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

  def fall_down(self):
    if self.pos_u // 16 == SWEETS_DONUT:
      return Sweets(self.pos_x, self.pos_y + 1, self.pos_u, self.pos_v)
    if self.pos_u // 16 == SWEETS_SHORTCAKE:
      return Sweets(self.pos_x, self.pos_y + 2, self.pos_u, self.pos_v)
    if self.pos_u // 16 == SWEETS_PUDDING:
      return Sweets(self.pos_x, self.pos_y + 1, self.pos_u, self.pos_v)
    if self.pos_u // 16 == SWEETS_SOFTCREAM:
      return Sweets(self.pos_x, self.pos_y + 2, self.pos_u, self.pos_v)

  def is_inside_screen(self):
    return True if self.pos_y < pyxel.height else False

  def is_touched(self, pos_x, pos_y):
    return True if pos_x - 16 < self.pos_x < pos_x + 16 and pos_y - 16 < self.pos_y < pos_y + 16 else False

class App:
  def __init__(self):
    pyxel.init(128, 128, title = "Birthday Penguin")
    pyxel.load("assetes/penguin.pyxres")

    self.stage = PyxelImage(0, 0, 1, 0, 0, 128, 128)
    self.score = Score(26, 4, 0, COLOR_ORANGE, COLOR_BROWN)
    self.timer = Timer(118, 4, SYSTEM_TIME_RIMIT, COLOR_ORANGE, COLOR_BROWN)
    self.penguin = Penguin(64, 106, 0, 0)
    self.sweets_list = []
    self.screen = PAGE_MAIN_MENU
    self.start = PyxelImage(26, 84, 1, 0, 128, 20, 8)
    self.result = PyxelImage(22, 72, 1, 32, 128, 24, 8)
    self.score_text = PyxelImage(16, 88, 1, 0, 136, 24, 8)

    pyxel.run(self.update, self.draw)

  def update(self):
    ## Qを押すとゲームが強制終了する
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()

    ## メインメニューでの処理
    if self.screen == PAGE_MAIN_MENU:
      ## スペースーキーが押されたら、ゲーム画面に遷移する
      if pyxel.btn(pyxel.KEY_SPACE):
        self.screen = PAGE_GAME_SCREEN
        self.stage = PyxelImage(0, 0, 1, 128, 0, 128, 128)

    ## ゲーム画面での処理
    if self.screen == PAGE_GAME_SCREEN:
      ## 十字キーの左右でぺんぎんの移動 
      if pyxel.btn(pyxel.KEY_LEFT):
        self.penguin = self.penguin.walk_left()
      if pyxel.btn(pyxel.KEY_RIGHT):
        self.penguin = self.penguin.walk_right()

      ## 1秒に一回タイマーを進める処理
      if pyxel.frame_count % 30 == 0:
        self.timer = Timer(118, 4, self.timer.word - 1, COLOR_ORANGE, COLOR_BROWN)

      ## 2秒に一回お菓子を生成する処理
      if pyxel.frame_count % 60 == 0:
        self.sweets_list.append(Sweets(random.randint(0, pyxel.width - 16), 0, random.randint(0, 3) * 16, 32))

      ## お菓子の移動とスクリーン外に出たお菓子の廃棄
      self.sweets_list = list(map(lambda sweets: sweets.fall_down(), self.sweets_list))
      self.sweets_list = list(filter(lambda sweets: sweets.is_inside_screen(), self.sweets_list))

      # お菓子の接触判定(スコアの加算処理もやる)
      self.sweets_list = list(filter(lambda sweets: self.update_score(sweets), self.sweets_list))

      ## タイマーがゼロになったら、リザルト画面へ遷移
      if self.timer.word == 0:
        self.screen = PAGE_RESULT_SCREEN
        self.stage = PyxelImage(0, 0, 1, 0, 0, 128, 128)
        self.score = Score(40, 88, self.score.word, COLOR_ORANGE, COLOR_BROWN)
        self.timer = Timer(118, 4, SYSTEM_TIME_RIMIT, COLOR_ORANGE, COLOR_BROWN)
        self.penguin = Penguin(64, 106, 0, 0)
        self.sweets_list = []

    # リザルト画面での処理
    if self.screen == PAGE_RESULT_SCREEN:
      ## スペースキーが離れたら、メインメニューに戻る(何故かこうしないと勝手に戻ってしまう...)
      if pyxel.btnr(pyxel.KEY_SPACE):
        self.screen = PAGE_MAIN_MENU
        self.score = Score(26, 4, 0, COLOR_ORANGE, COLOR_BROWN)

  def update_score(self, sweets):
    if sweets.is_touched(self.penguin.pos_x, self.penguin.pos_y):
      if sweets.pos_u // 16 == SWEETS_DONUT:
        self.score = Score(26, 4, self.score.word + 100, COLOR_ORANGE, COLOR_BROWN)
      if sweets.pos_u // 16 == SWEETS_SHORTCAKE:
        self.score = Score(26, 4, self.score.word + 500, COLOR_ORANGE, COLOR_BROWN)
      if sweets.pos_u // 16 == SWEETS_PUDDING:
        self.score = Score(26, 4, self.score.word + 200, COLOR_ORANGE, COLOR_BROWN)
      if sweets.pos_u // 16 == SWEETS_SOFTCREAM:
        self.score = Score(26, 4, self.score.word + 700, COLOR_ORANGE, COLOR_BROWN)
      return False
    else:
      return True

  def draw(self):
    pyxel.cls(SYSTEM_BG_COLOR)
    
    self.stage.print()

    if self.screen == PAGE_MAIN_MENU:
      self.start.print()

    if self.screen == PAGE_GAME_SCREEN:
      for sweets in self.sweets_list:
        sweets.print()
      self.score.print()
      self.timer.print()
      self.penguin.print()

    if self.screen == PAGE_RESULT_SCREEN:
      self.result.print()
      self.score.print()
      self.score_text.print()

if __name__ == "__main__":
  App()