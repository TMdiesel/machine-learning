# classification_bokeh
- ロジスティック回帰のハイパーパラメーターを変更した時の分類境界の変化をbokehでインタラクティブに可視化します。
- データはirisを対象とします。

## 実行方法
下記コマンドを実行します。ブラウザ上でパラメータを変更させられます。
```
poetry run bokeh serve src/lr_vis.py
```
![lr_vis](https://user-images.githubusercontent.com/50258785/112723703-435a9700-8f53-11eb-87f0-ae87f96bcdce.gif)
