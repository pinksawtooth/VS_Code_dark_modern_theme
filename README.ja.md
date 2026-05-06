# VS Code Dark Modern Theme for Ghidra

[English](README.md) | 日本語

Ghidra 12.0.4 PUBLIC 向けの VS Code Dark Modern 風テーマです。

![VS Code Dark Modern テーマのスクリーンショット](assets/screenshot.png)

テーマファイルと外部アイコンだけで構成しているため、Ghidra 本体の jar、アプリケーションバンドル、署名済みバイナリは変更しません。macOS のコード署名にも影響しない配布形式です。

## 内容

- `themes/vscode-dark-modern.theme`
- `images/vscode/codicons/`
- `install.sh`

`images/vscode/codicons/` には、テーマが `[EXTERNAL]images/vscode/codicons/...` として参照する PNG アイコンと、Codicons のライセンスファイルを含めています。

## インストール

macOS / Ghidra 12.0.4 PUBLIC の場合:

```sh
git clone https://github.com/pinksawtooth/VS_Code_dark_modern_theme.git
cd VS_Code_dark_modern_theme
./install.sh
```

手動で入れる場合:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"

mkdir -p "$GHIDRA_USER_DIR/themes"
mkdir -p "$GHIDRA_USER_DIR/images/vscode/codicons"

cp themes/vscode-dark-modern.theme "$GHIDRA_USER_DIR/themes/"
cp -R images/vscode/codicons/. "$GHIDRA_USER_DIR/images/vscode/codicons/"
```

Ghidra のバージョンが違う場合は、`ghidra_12.0.4_PUBLIC` の部分を自分のユーザーディレクトリ名に置き換えてください。

インストール先を明示したい場合は、次のように `GHIDRA_USER_DIR` を指定できます。

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC" ./install.sh
```

## テーマの有効化

1. Ghidra を起動、または再起動します。
2. `Edit` -> `Theme` を開きます。
3. `VS Code Dark Modern` を選択します。
4. 反映が不完全な場合は Ghidra を再起動してください。

## 更新

このリポジトリを pull してから、もう一度 `./install.sh` を実行してください。

```sh
git pull
./install.sh
```

## アンインストール

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

その後、Ghidra を再起動して別のテーマを選択してください。

## 備考

- Ghidra のテーマ機能だけで変更できる範囲に限定しています。
- Ghidra 本体ファイル、jar、アプリケーションバンドル、署名済みファイルは変更しません。
- Ghidra 12.0.4 PUBLIC で検証しています。
