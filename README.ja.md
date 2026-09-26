# VS Code Dark Modern Theme for Ghidra

[English](README.md) | 日本語

Ghidra 12.1.4 PUBLIC 向けの VS Code Dark Modern 風テーマです。

![VS Code Dark Modern テーマのスクリーンショット](https://github.com/user-attachments/assets/5767b4f8-0b72-4dad-afc1-47850b6349c4)

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

1. [最新リリースの vscode-dark-modern.theme.zip](https://github.com/pinksawtooth/VS_Code_dark_modern_theme/releases/latest/download/vscode-dark-modern.theme.zip) をダウンロードします（リポジトリの `dist/` にも同梱しています）。
2. Ghidra で `Edit` -> `Theme` -> `Import...` を開きます。
3. ダウンロードした `vscode-dark-modern.theme.zip` を選択します。

Ghidra が同梱アイコンをユーザー設定ディレクトリへ展開し、テーマを登録するところまで一括で行います。一部 UI に反映されない場合は Ghidra を再起動してください。

この zip は Ghidra 純正のテーマバンドル形式（`.theme` ファイル＋アイコン一式）です。テーマ編集後は次で再生成できます。

```sh
./tools/build-theme-zip.sh
```

手動でファイルをコピーしたい場合は、以下のスクリプトによるインストール方法も利用できます。

## Windows でのインストール

Windows / Ghidra 12.1.4 PUBLIC では、このリポジトリのディレクトリで PowerShell を開いて実行します。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

インストーラーはテーマを次の場所にコピーします。

```text
%APPDATA%\ghidra\ghidra_12.1.4_PUBLIC
```

手動でインストールする場合:

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.4_PUBLIC'

New-Item -ItemType Directory -Force -Path "$GhidraUserDir\themes" | Out-Null
New-Item -ItemType Directory -Force -Path "$GhidraUserDir\images\vscode\codicons" | Out-Null

Copy-Item .\themes\vscode-dark-modern.theme -Destination "$GhidraUserDir\themes\" -Force
Copy-Item .\images\vscode\codicons\* -Destination "$GhidraUserDir\images\vscode\codicons\" -Recurse -Force
```

別の Ghidra バージョンで使う場合は、`ghidra_12.1.4_PUBLIC` を自分の Ghidra ユーザー設定ディレクトリ名に置き換えてください。

インストール先を明示する場合:

```powershell
.\install.ps1 -GhidraUserDir '<Ghidra user settings directory>'
```

## macOS / Linux でのインストール

macOS では、インストーラーの既定インストール先は次の場所です。

```text
$HOME/Library/ghidra/ghidra_12.1.4_PUBLIC
```

Linux では、インストーラーの既定インストール先は次の場所です。

```text
${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.4_PUBLIC
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
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.4_PUBLIC'

Remove-Item "$GhidraUserDir\themes\vscode-dark-modern.theme" -Force
Remove-Item "$GhidraUserDir\images\vscode\codicons" -Recurse -Force
```

その後、Ghidra を再起動して別のテーマを選択してください。

## macOS / Linux でのアンインストール

インストール時に使った Ghidra ユーザー設定ディレクトリを指定してください。

macOS:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.1.4_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Linux:

```sh
GHIDRA_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.4_PUBLIC"

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
- Ghidra 12.1.4 PUBLIC のテーマ定義と同梱アイコンを検証しています。全 OS での GUI 動作の再確認は行っていません。12.1.x で追加されたテーマキー（デバッガのブレークポイントタイムライン、ドッキングタブの active/inactive 分離、バイトビューアの編集カーソル）にも対応しつつ、12.0.x の旧キーも残しているため Ghidra 12.0.4 / 12.1.2 / 12.1.3 との互換性も維持しています。旧バージョンへインストールする際は、インストール先を明示してください。
- 配色は VS Code Dark Modern の公式パレット（エディタ `#1F1F1F`、サイドバー等 `#181818`、境界線 `#2B2B2B`、入力欄 `#313131`、アクセント `#0078D4`）に合わせています。
- Listing / Decompiler は選択中も構文の文字色を維持するため、コード選択には濃い青 `#193549`、検索には暗い黄土色を使います。一般の入力欄の選択色は `#264F78` です。変更済みバイトとデバッガの変更値は黄系 `#D7BA7D`、エラー文字は明るい赤 `#F48771` とし、エラーアイコンの赤と使い分けます。アドレスは行番号より明るく表示します。
- Function Graph の通常フローは緑、条件分岐は黄、無条件分岐は青で、Program Graph と意味を揃えています。強調中の経路は白です。ビットフィールドの背景は文字が読める暗い色を使います。
- パネル見出しは平坦な背景にし、操作中のタイトルを白、非アクティブなタイトルをグレーで区別します。選択中のタブも白文字にし、閉じるアイコンはホバー時に明るく、タブ一覧ボタンは下向きの山形にしています。ポップアップと対応するウィンドウの境界は控えめなグレーです。フォント、クリック領域、ドッキングの操作は従来の設定を維持します。
- 標準 Swing タブには FlatLaf の下線スタイルを使います。Ghidra 独自のドキュメントタブには専用の立体的な枠があり、テーマでは描画処理を置き換えられません。OS のタイトルバーとの一体化にも、OS とアプリケーション側のウィンドウ処理が関係します（[FlatLaf のウィンドウ装飾](https://www.formdev.com/flatlaf/window-decorations/)、[macOS 対応](https://www.formdev.com/flatlaf/macos/)）。
- 汎用操作には Codicons を使い、Ghidra 固有の機能や状態には同じ配色・16px グリッドの専用アイコンを使います。`tools/icon-map.py` が割り当てを管理し、専用アイコンの編集可能な SVG 原本は `tools/custom-icons/` にあります。
- 外部関数と Thunk は矢印、union は重なる領域、ポインターは参照先への矢印で表現します。ブレークポイントは塗りつぶし／輪郭／半塗りと途切れた輪郭で状態を区別し、不整合には小さな感嘆符を重ねます。Function Graph の方向・循環、Decompiler の読み取り専用・到達不能コード、フォルダーのロック状態にも専用の形を割り当てています。アプリ用の 16/24px アイコンは配線を簡略化しています。
- 再生成手順: `python3 tools/build-theme.py` でテーマの `icon.*` 行とレンダリング用マニフェストを再生成し、`CODICONS_SRC=<codicons>/src/icons ./tools/generate-icons.sh` で Codicons と専用 SVG から PNG を生成します（SVG 対応の ImageMagick 7 が必要）。SVG の基準解像度を 96 DPI として、出力サイズで直接描画します。

## ビルドと検証

生成スクリプトは `~/ghidra/` 以下の Ghidra 12.0.4 / 12.1.2 / 12.1.3 / 12.1.4 を探し、新しいバージョンの定義を優先します。別の場所にある場合は、`GHIDRA_DIRS` に Ghidra 本体のディレクトリを指定してください（ユーザー設定ディレクトリではありません）。複数指定する場合の区切りは macOS/Linux では `:`、Windows では `;` です。

```sh
GHIDRA_DIRS="/path/to/ghidra_12.1.4_PUBLIC" python3 tools/build-theme.py
CODICONS_SRC="/path/to/codicons/package/src/icons" ./tools/generate-icons.sh
./tools/build-theme-zip.sh
python3 -m unittest discover -s tests -v
```

Codicons は同梱素材と同じ `@vscode/codicons` **0.0.45** を使用してください。Ghidra のアイコン定義が読み込めない場合は生成を停止します。画像生成では Codicons と `tools/custom-icons/` の必要な SVG をすべて確認し、一時ディレクトリでの描画が完了してから素材を更新します。

エディタのフォントは OS 共通の Java 論理フォント `Monospaced` です。有効なフィルターはアクセント色で表示します。Version Tracking の状態アイコンは各表示位置を維持し、進捗表示は Ghidra の回転指定でアニメーションします。これらの指定はテーマを再生成しても保持されます。

JDK とローカルの Ghidra がある場合は、実際の読込・描画処理でも検証できます。

```sh
python3 tests/check_ghidra.py "/path/to/ghidra_12.1.4_PUBLIC"
```

一時設定ディレクトリへ Ghidra の処理で ZIP を読み込み、状態アイコンの表示位置とアニメーションフレーム、専用アイコンの形の違い、不整合マークの重なり、閉じるアイコンのホバー表示を確認します。目視確認用の画像は `build/theme-check.png`、`build/icons-check.png`、`build/colors-check.png`、`build/windows-check.png` に出力します。いずれも画面外で描画したサンプルで、実画面のスクリーンショットではありません。ウィンドウ画像は見出しの配色サンプル、Ghidra の実際のタブ枠描画、標準 Swing タブを示します。OS のタイトルバーやドラッグ・リサイズ操作の検証は含みません。

配色テストでは重要な文字と背景の組み合わせを 4.5:1 以上、構文の文字色を維持する選択・検索背景を 3:1 以上で検証します。後者は視認性の退行を防ぐための下限で、テーマ全体のアクセシビリティ適合を保証するものではありません。
