# penguin-birthday

[Pyxel](https://github.com/kitao/pyxel)で開発したぺんぎんがお菓子を食べまくる2Dゲーム。

作成したゲームはPyxel様の謎の力により、以下のリンクからどこでも遊べます(現在はPCからの操作のみ対応)。
- https://kitao.github.io/pyxel/wasm/launcher/?run=UniUrchin.penguin-birthday.main

<div align="center">
<img width="350" src="./images/game-image.png">
</div>

## Requirement

- Python 3.10.6
- Pyxel 1.9.1

penguin-birthdeyの開発および実行には、事前にpyxelのインストールが必要です。

```
$ python3 -m pip install -U pyxel
```

## How to Execute & Build

- 開発用Pyxelアプリケーションの実行

```
$ pyxel run main.py
```

- penguin-birthdayに使用しているアセットの編集

```
$ pyxel edit assets/main.pyxres
```

- Pyxelアプリケーションのビルド(ファイル名を後から変更する必要アリ)

```
$ pyxel package . main.py
```

- 本番用Pyxelアプリケーションの実行

```
$ play penguin-birthday.pyxapp
```

## 🚧 How to Play?

完成してないので未記載です。今後の開発に乞うご期待!!