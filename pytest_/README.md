# pytest

## ローカルでの実行方法
```sh
poetry run pytest test.py 
```

## GitHub Actions
- [ci.yml][ci.yml]で指定したトリガーイベントが発生した際に、pytestを実行します。

## 参考
- [pytestに入門してみたメモ](https://qiita.com/everylittle/items/1a2748e443d8282c94b2)

[ci.yml]:../github/workflows/ci.yml