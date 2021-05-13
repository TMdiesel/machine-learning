# machine-learning
機械学習に関連する実装です。
詳細は各ディレクトリ下のREADMEをご参照ください。

- [pipeline][pipeline]
    - 特徴量管理、学習・推論パイプラインコードです。
- [classification_bokeh][classification_bokeh]
  - ロジスティック回帰のハイパーパラメーターを変更した際の分類境界の変化をbokehでインタラクティブに可視化します。
- [vscode_python_setting][vscode_python_setting]
  - VSCode Python用のsettings.jsonです。
- [automl][automl]
  - AutoMLライブラリの練習です。
- [pytest_][pytest_]
  - GitHub Actionsでpytestを実行する対象のテストスクリプトです。

[pipeline]:./pipeline
[classification_bokeh]:./classification_bokeh
[vscode_python_setting]:./vscode_python_setting
[automl]:./automl
[pytest_]:./pytest_

## 実行環境
下記コマンドで必要なパッケージをインストールできます。
```
poetry install
```