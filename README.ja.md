# VS Code Dark Modern Theme for Ghidra

[English](README.md) | 日本語

Ghidra 12.1.2 PUBLIC 向けの VS Code Dark Modern 風テーマです。

![VS Code Dark Modern テーマのスクリーンショット](https://raw.githubusercontent.com/pinksawtooth/VS_Code_dark_modern_theme/main/assets/screenshot.png)

このパッケージは Ghidra のテーマファイルと外部アイコン素材で構成されています。インストール先は Ghidra のユーザー設定ディレクトリで、Ghidra 本体のディレクトリ、jar ファイル、署名済みバイナリは変更しません。

## 内容

- `themes/vscode-dark-modern.theme`
- `images/vscode/codicons/`
- `install.ps1`
- `install.sh`
- `tools/`（アイコンのマッピング・生成スクリプト。インストールには不要）

`images/vscode/codicons/` には、テーマが `[EXTERNAL]images/vscode/codicons/...` として参照する PNG アイコンと Codicons のライセンスファイルが含まれています。

## インストール（推奨）: テーマファイルを1つインポート

手動コピーもスクリプトも不要の、最も簡単な方法です（OS共通）。

1. このリポジトリから `dist/vscode-dark-modern.theme.zip` をダウンロードします。
2. Ghidra で `Edit` -> `Theme` -> `Import...` を開きます。
3. ダウンロードした `vscode-dark-modern.theme.zip` を選択します。

Ghidra が同梱アイコンをユーザー設定ディレクトリへ展開し、テーマを登録するところまで一括で行います。一部 UI に反映されない場合は Ghidra を再起動してください。

この zip は Ghidra 純正のテーマバンドル形式（`.theme` ファイル＋アイコン一式）です。テーマ編集後は次で再生成できます。

```sh
./tools/build-theme-zip.sh
```

手動でファイルをコピーしたい場合は、以下のスクリプトによるインストール方法も利用できます。

## Windows でのインストール

Windows / Ghidra 12.1.2 PUBLIC では、このリポジトリのディレクトリで PowerShell を開いて実行します。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

インストーラーはテーマを次の場所にコピーします。

```text
%APPDATA%\ghidra\ghidra_12.1.2_PUBLIC
```

手動でインストールする場合:

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.2_PUBLIC'

New-Item -ItemType Directory -Force -Path "$GhidraUserDir\themes" | Out-Null
New-Item -ItemType Directory -Force -Path "$GhidraUserDir\images\vscode\codicons" | Out-Null

Copy-Item .\themes\vscode-dark-modern.theme -Destination "$GhidraUserDir\themes\" -Force
Copy-Item .\images\vscode\codicons\* -Destination "$GhidraUserDir\images\vscode\codicons\" -Recurse -Force
```

別の Ghidra バージョンで使う場合は、`ghidra_12.1.2_PUBLIC` を自分の Ghidra ユーザー設定ディレクトリ名に置き換えてください。

インストール先を明示する場合:

```powershell
.\install.ps1 -GhidraUserDir '<Ghidra user settings directory>'
```

## macOS / Linux でのインストール

macOS では、インストーラーの既定インストール先は次の場所です。

```text
$HOME/Library/ghidra/ghidra_12.1.2_PUBLIC
```

Linux では、インストーラーの既定インストール先は次の場所です。

```text
${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.2_PUBLIC
```

```sh
git clone https://github.com/pinksawtooth/VS_Code_dark_modern_theme.git
cd VS_Code_dark_modern_theme
./install.sh
```

インストール先を明示する場合:

```sh
GHIDRA_USER_DIR="<Ghidra user settings directory>" ./install.sh
```

## テーマの有効化

1. Ghidra を起動、または再起動します。
2. `Edit` -> `Theme` を開きます。
3. `VS Code Dark Modern` を選択します。
4. 一部 UI に反映されない場合は Ghidra を再起動してください。

## 更新

最新版を取得して、もう一度インストーラーを実行します。

Windows:

```powershell
git pull
.\install.ps1
```

macOS / Linux:

```sh
git pull
./install.sh
```

## Windows でのアンインストール

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.2_PUBLIC'

Remove-Item "$GhidraUserDir\themes\vscode-dark-modern.theme" -Force
Remove-Item "$GhidraUserDir\images\vscode\codicons" -Recurse -Force
```

その後、Ghidra を再起動して別のテーマを選択してください。

## macOS / Linux でのアンインストール

インストール時に使った Ghidra ユーザー設定ディレクトリを指定してください。

macOS:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.1.2_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Linux:

```sh
GHIDRA_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.2_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

その後、Ghidra を再起動して別のテーマを選択してください。

## 備考

- Ghidra のユーザーインストールテーマはユーザー設定ディレクトリに保存されます。Windows の既定設定ディレクトリは `%APPDATA%\ghidra\ghidra_<version>` です。
- macOS の既定設定ディレクトリは `$HOME/Library/ghidra/ghidra_<version>` です。
- Linux の既定設定ディレクトリは `${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_<version>` です。
- Ghidra 本体が別のアプリケーションディレクトリにある場合でも、このテーマは Ghidra が検出できるユーザー設定ディレクトリにコピーしてください。
- このテーマは Ghidra のテーマ機能で扱える範囲に限定しています。
- Ghidra 本体ファイル、jar、署名済みファイルは変更しません。
- Ghidra 12.1.2 PUBLIC で検証しています。12.1.x で追加されたテーマキー（デバッガのブレークポイントタイムライン、ドッキングタブの active/inactive 分離、バイトビューアの編集カーソル）にも対応しつつ、12.0.x の旧キーも残しているため Ghidra 12.0.4 でもそのまま使えます。
- 配色は VS Code Dark Modern の公式パレット（エディタ `#1F1F1F`、サイドバー等 `#181818`、境界線 `#2B2B2B`、入力欄 `#313131`、アクセント `#0078D4`）に合わせています。
- アイコンは「意味」で対応付けています。`tools/icon-map.py` が Ghidra の各概念を VS Code が同じ用途で使うコドアイコンに割り当てます（例: デバッガのツールバーは本物の `debug-continue` / `debug-pause` / `debug-step-*`、有効ブレークポイントは塗りつぶしの赤丸、Version Tracking の承認/却下は緑チェック/赤バツ）。
- 再生成手順: `python3 tools/build-theme.py` でテーマの `icon.*` 行とレンダリング用マニフェストを再生成し、`CODICONS_SRC=<codicons>/src/icons ./tools/generate-icons.sh` で `@vscode/codicons` の SVG から PNG を生成します（librsvg 対応の ImageMagick が必要）。
