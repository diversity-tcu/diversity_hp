# diversity_hp 運用ガイド

東京都市大学ダイバーシティ推進室のウェブサイト(Astro静的サイト)。
このファイルは **AIアシスタント(Claude等)に作業を依頼するときの共通ルール** を定義する。
非エンジニアでも「AIに自然言語で頼む → AIがファイルを編集 → GitHubにpush → 自動公開」で運用できる。

## サイト構成

- **フレームワーク**: Astro v5(静的サイト生成)
- **デプロイ先**: GitHub Pages(`main` ブランチへのpushで自動公開)
- **コンテンツ**: `src/content/` 配下の Markdown ファイル

```
src/content/
├── pages/    … 固定ページ(About、お問い合わせ等)
├── news/     … お知らせ
└── events/   … イベント情報
public/
└── uploads/  … 画像ファイル(年/月のフォルダ構造)
```

## よくある運用タスク(AIへの依頼例)

### 1. お知らせを追加する
> 「2026年5月10日にシンポジウム『○○』を開催することをお知らせに追加して。本文は次の通り: …」

AIは `src/content/news/YYYY-MM-DD.md` を以下の形式で作成する（同日に複数ある場合は `YYYY-MM-DD-2.md`）:
```markdown
---
title: "シンポジウム○○開催のお知らせ"
date: "2026-05-10"
status: "publish"
---

本文…
```

### 2. イベントを追加する
> 「○○イベントを events に追加。日時は…、会場は…」

`src/content/events/YYYY-MM-DD.md` に同形式で作成（同日複数は `YYYY-MM-DD-2.md`）。

### 3. 画像を追加する
1. 画像を `public/uploads/2026/04/<filename>.jpg` に置く(年/月フォルダで整理)
2. Markdown本文中で `![説明](/uploads/2026/04/<filename>.jpg)` と参照

### 4. お知らせ・イベントを修正する
> 「news の 2026-05-10 の日付を5月17日に変更して」

該当 `.md` の frontmatter または本文を編集。

### 5. 固定ページの文言を直す
> 「About ページの『私たちは…』の段落を次のように書き換えて」

`src/content/pages/about.md` を編集。

### 6. TCUダイバーシティ通信の新号を追加する
> 「TCUダイバーシティ通信Vol.21(2026年9月発行)を追加して。PDFは /uploads/2026/09/Vol21.pdf、表紙画像は同フォルダの Vol21.jpg」

`src/content/communication/VolXX.md` を新規作成するだけ。date 降順で自動ソートされ
`/communication/` 一覧に即反映される。サムネイル画像を用意できない場合は `thumb` を
省略すれば PDF アイコンの fallback 表示になる。ファイル名は `Vol21` のように連番で命名。

```markdown
---
title: "TCUダイバーシティ通信Vol.21(2026年9月発行)"
date: "2026-09-01"
pdf: "/uploads/2026/09/Vol21.pdf"
thumb: "/uploads/2026/09/Vol21.jpg"
---
```

### 7. 卒業生/教員ロールモデル集の新号を追加する
> 「卒業生ロールモデル集 Vol.19 を追加して。所属は○○学部○○学科、氏名は△△△△、本文は…」

- 卒業生: `src/content/pages/publication/rolemodel/vol-XX.md` を新規作成
- 教員: `src/content/pages/publication/t_rolemodel/t_volXX.md` を新規作成

**HTMLは不要。** frontmatter にプロフィール情報を書き、本文は普通のMarkdownで書く。
タイトル接頭辞は必ず以下を使うこと(ページ側のフィルタ条件):

- 卒業生: `社会で輝く卒業生たち Vol.XX`
- 教員: `東京都市大学の多様な教員たち Vol.XX`

#### 卒業生ロールモデルのテンプレート

```markdown
---
title: "社会で輝く卒業生たち Vol.19"
date: "2026-04-20"
status: "publish"
name: "山田 花子"
affiliation: "理工学部 機械システム工学科"
role: "さん"
photo_main: "/uploads/2026/04/role19_01.jpg"
workplace: "株式会社○○\n○○部 ○○課"
education: "2020年 東京都市大学 理工学部 機械システム工学科 卒業\n2022年 東京都市大学大学院 総合理工学研究科 修了"
high_school: "東京都立○○高等学校 卒業"
photo_style: "/uploads/2026/04/role19_style.png"
---

## 現在の仕事内容

ここに本文を書く。

### 職業を選択したきっかけ

ここに本文を書く。

### 夢の実現に向けて努力したこと

ここに本文を書く。

### 私の趣味

![趣味の写真](/uploads/2026/04/role19_02.jpg)

ここに本文を書く。

### 都市大を選んでよかったこと

![写真](/uploads/2026/04/role19_03.jpg)

ここに本文を書く。

## Message

メッセージ本文を書く。
```

#### 教員ロールモデルのテンプレート

```markdown
---
title: "東京都市大学の多様な教員たち Vol.09"
date: "2026-04-20"
status: "publish"
name: "田中 太郎"
affiliation: "理工学部 機械工学科"
role: "教授"
photo_main: "/uploads/2026/04/t_role09_01.jpg"
theme: "ここに教員のテーマとなる一言を入れる"
career: "○○大学○○学部卒業。\n○○大学大学院修了。\n東京都市大学講師を経て現職。\n／出身地"
photo_style: "/uploads/2026/04/t_role09_style.png"
published_date: "2026年4月20日"
---

## 研究内容の見出し

ここに本文を書く。

### 研究のきっかけ

ここに本文を書く。

### 夢のために努力したこと

ここに本文を書く。

### マイブーム

![写真](/uploads/2026/04/t_role09_02.jpg)

ここに本文を書く。

### 研究をどのように社会に役立てていきたいですか？

ここに本文を書く。

## 若い人へのメッセージをお願いします。

メッセージ本文を書く。
```

#### frontmatter フィールド一覧

| フィールド | 必須 | 説明 |
|---|---|---|
| `name` | ○ | 氏名 |
| `affiliation` | | 所属(学部・学科) |
| `role` | | 役職(「さん」「教授」「准教授」など) |
| `photo_main` | | メイン写真パス |
| `photo_style` | | 1日のスタイル画像パス |
| `workplace` | | 勤務先(卒業生用、改行は `\n`) |
| `education` | | 出身学部(卒業生用、改行は `\n`) |
| `high_school` | | 出身高校(卒業生用) |
| `theme` | | テーマの一言(教員用) |
| `career` | | 経歴(教員用、改行は `\n`) |
| `published_date` | | 掲載日(教員用、「2026年4月20日」形式) |

> 既存記事(Vol.01〜18, t_vol01〜08)も含め、全記事がこのMarkdown形式に変換済み。

### 8. ライブラリ連載の新記事を追加する
> 「イクボス連載の第13回を追加して。所属・氏名は…、本文は…」

`src/content/pages/library/<series>/<name>.md` を新規作成するだけ。
`<series>` は `workinlife` / `ikubosu` / `mado` / `okada` のいずれか。
ファイル名は `ikubosu13` のように連番で命名。本文冒頭に `**所属 氏名 役職**` の
太字ブロックと `/uploads/...` の画像があれば、 `/library/` の該当セクションに
date 降順で自動反映される。タイトルには `第XX回` を含めること(Vol表示に使用)。

一覧ページの書影(サムネイル)を指定するには、frontmatter に `thumb` を追加する。
指定がなければ本文中の最初の画像が自動的に使われる。どちらもなければシリーズ別のデフォルト画像が表示される。

```markdown
---
title: "第03回 ..."
date: "2026-04-20"
status: "publish"
thumb: "/uploads/2026/04/workinlife03.jpg"
---
```

## AIへの作業ルール(依頼者が伝えなくてもAIは守ること)

1. **新規お知らせ/イベントは既存ファイルのfrontmatterをそのまま踏襲**(余計なフィールドを追加しない)
2. **ファイル名は `YYYY-MM-DD.md` 形式**(同日複数は末尾に `-2`, `-3` を付与）
3. **画像の保存先は `public/uploads/YYYY/MM/`**(WordPress時代と同構造)
4. **HTMLタグは最小限**(段落・見出し・リスト・リンク・画像はMarkdown記法を使う。表など複雑なものはHTMLでOK)
5. **編集後は `npm run build` でビルドが通ることを確認**(エラーがあれば修正してから報告)
6. **コミットメッセージは内容を要約**(例: `news: シンポジウム告知を追加`)

## 公開フロー(運用者向け)

1. AIに依頼してファイルを編集してもらう
2. 内容を確認する(`npm run dev` でローカルプレビュー: http://localhost:4321 )
3. GitHubにpushする(AIに「pushして」と依頼すればOK)
4. 数分後、 https://www.diversity.tcu.ac.jp/ に反映される

## トラブル時

- **ビルドが失敗する** → AIに「`npm run build` を実行してエラーを直して」と依頼
- **画像が表示されない** → パスが `/uploads/...` で始まっているか確認
- **どこに何があるか分からない** → AIに「○○について書かれているファイルを探して」と依頼

## 開発コマンド

```bash
npm install        # 初回のみ
npm run dev        # ローカルプレビュー (http://localhost:4321)
npm run build      # 本番ビルド (dist/ に出力)
npm run preview    # ビルド結果をプレビュー
```

## ディレクトリ詳細

```
.
├── src/
│   ├── content/           # ★編集対象: ページ・お知らせ・イベント
│   ├── content.config.ts  # コンテンツのスキーマ定義(編集注意)
│   ├── layouts/Base.astro # 共通レイアウト(ヘッダー・フッター)
│   └── pages/             # ルーティング定義(編集注意)
├── public/
│   ├── uploads/           # ★編集対象: 画像
│   └── assets/wp-css/     # 旧WordPressテーマのCSS(編集注意)
├── astro.config.mjs       # Astro設定(編集注意)
└── package.json
```

「★編集対象」以外は通常の運用では触らない。AIには「コンテンツ更新だけしたい」と伝えれば誤って構成を壊さない。
