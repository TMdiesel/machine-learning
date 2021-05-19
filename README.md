# machine-learning

機械学習に関連する実装です。
詳細は各ディレクトリ下の README をご参照ください。

- [pipeline][pipeline]
  - 特徴量管理、学習・推論パイプラインコードです。
- [classification_bokeh][classification_bokeh]
  - ロジスティック回帰のハイパーパラメーターを変更した際の分類境界の変化を bokeh でインタラクティブに可視化します。
- [vscode_python_setting][vscode_python_setting]
  - VSCode Python 用の settings.json です。
- [automl][automl]
  - AutoML ライブラリの練習です。
- [pytest\_][pytest_]
  - GitHub Actions で pytest を実行する対象のテストスクリプトです。
- [interpretable_ml][interpretable_ml]
  - 教師ありモデルの解釈手法のまとめです。
- [jssc][jssc]
  - 統計検定に関連する実装です。

[pipeline]: ./pipeline
[classification_bokeh]: ./classification_bokeh
[vscode_python_setting]: ./vscode_python_setting
[automl]: ./automl
[pytest_]: ./pytest_
[interpretable_ml]: ./interpretable_ml
[jssc]: ./jssc

## 実行環境

下記コマンドで必要なパッケージをインストールできます。

```bash
poetry install
```
