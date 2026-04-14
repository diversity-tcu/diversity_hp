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

AIは `src/content/news/<slug>.md` を以下の形式で作成する:
```markdown
---
title: "シンポジウム○○開催のお知らせ"
slug: "symposium-2026-05"
date: "2026-05-10"
status: "publish"
---

本文…
```

### 2. イベントを追加する
> 「○○イベントを events に追加。日時は…、会場は…」

`src/content/events/<slug>.md` に同形式で作成。

### 3. 画像を追加する
1. 画像を `public/uploads/2026/04/<filename>.jpg` に置く(年/月フォルダで整理)
2. Markdown本文中で `![説明](/uploads/2026/04/<filename>.jpg)` と参照

### 4. お知らせ・イベントを修正する
> 「news の symposium-2026-05 の日付を5月17日に変更して」

該当 `.md` の frontmatter または本文を編集。

### 5. 固定ページの文言を直す
> 「About ページの『私たちは…』の段落を次のように書き換えて」

`src/content/pages/about.md` を編集。

### 6. TCUダイバーシティ通信の新号を追加する
> 「TCUダイバーシティ通信Vol.21(2026年9月発行)を追加して。PDFは /uploads/2026/09/Vol21.pdf、表紙画像は同フォルダの Vol21.jpg」

`src/data/communication.ts` の配列 `communicationEntries` の **先頭(または任意位置)に1エントリ追加** するだけ。
date 降順で自動ソートされ、 `/communication/` 一覧に即反映される。サムネイル画像を用意できない
場合は `thumb` を省略すれば PDF アイコンの fallback 表示になる。

```ts
{ title: 'TCUダイバーシティ通信Vol.21(2026年9月発行)', date: '2026-09-01',
  pdf: '/uploads/2026/09/Vol21.pdf', thumb: '/uploads/2026/09/Vol21.jpg' },
```

### 7. 卒業生/教員ロールモデル集の新号を追加する
> 「卒業生ロールモデル集 Vol.19 を追加して。所属は○○学部○○学科、氏名は△△△△、本文は…」

- 卒業生: `src/content/pages/publication/rolemodel/vol-XX.md` を新規作成
- 教員: `src/content/pages/publication/t_rolemodel/t_volXX.md` を新規作成

frontmatter の `title` / `slug` / `date` を既存号に倣って設定し、本文の冒頭に
**所属・氏名・役職** (Markdown の太字 `**...**` か WordPress移行時の
`<span class="font-15em">氏名</span>` を含む HTML ブロック)を置き、本文中に画像
(`/uploads/YYYY/MM/xxx.(jpg|png|gif|webp)`) を1枚以上入れておけば、
`/rolemodel/` または `/t_rolemodel/` 一覧ページに **date 降順で自動反映** される。
タイトル接頭辞は必ず以下を使うこと(ページ側のフィルタ条件):

- 卒業生: `社会で輝く卒業生たち Vol.XX`
- 教員: `東京都市大学の多様な教員たち Vol.XX`

### 8. ライブラリ連載の新記事を追加する
> 「イクボス連載の第13回を追加して。所属・氏名は…、本文は…」

`src/content/pages/library/<series>/<slug>.md` を新規作成するだけ。
`<series>` は `workinlife` / `ikubosu` / `mado` / `okada` のいずれか。
slug は `ikubosu13` のように連番で命名。本文冒頭に `**所属 氏名 役職**` の
太字ブロックと `/uploads/...` の画像があれば、 `/library/` の該当セクションに
date 降順で自動反映される。タイトルには `第XX回` を含めること(Vol表示に使用)。

## AIへの作業ルール(依頼者が伝えなくてもAIは守ること)

1. **新規お知らせ/イベントは既存ファイルのfrontmatterをそのまま踏襲**(余計なフィールドを追加しない)
2. **slug は英数字とハイフンのみ**(日本語不可)
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
