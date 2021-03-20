# pipeline
- 特徴量管理、学習・推論パイプラインコードです。
- サンプルとしてタイタニックデータを対象としています。

## 実行手順
1. 特徴量を下記コマンドで作成します。必要に応じて`config/feature/config.yaml`を変更します。
    ```
    poetry run python src/feature/create.py
    ```
2. 学習・推論を行います。必要に応じて`config/model/config.yaml`を変更します。
CV結果はMLflow UIから一覧を確認することができます。
    ```
    poetry run python src/model/run.py
    ```

## 参考
- [データ分析コンペで使っているワイの学習・推論パイプラインを晒します](https://www.takapy.work/entry/2019/12/14/165119)
- [Kaggleで使えるFeather形式を利用した特徴量管理法](https://amalog.hateblo.jp/entry/kaggle-feature-management)
- [ghmagazine/kagglebook](https://github.com/ghmagazine/kagglebook)

