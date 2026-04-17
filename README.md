# diversity_hp

東京都市大学ダイバーシティ推進室ウェブサイト

- 公開サイト: https://kasekiguchi.github.io/diversity_hp/
- ビルド状況: https://github.com/kasekiguchi/diversity_hp/actions

---

## 環境構築

初めて作業する方は、まず環境構築ガイドに従って準備してください。

→ [環境構築ガイド（GitHub アカウント作成〜リポジトリのクローン）](Manual/setup.md)

---

## コンテンツ追加

各コンテンツの追加・編集手順です。テンプレートは [Manual/templates/](Manual/templates/) にあります。

### お知らせ

新しいお知らせを追加します。ファイル: `src/content/news/YYYY-MM-DD.md`

→ [お知らせ追加手順](Manual/add-news.md) ／ [テンプレート](Manual/templates/news.md)

### イベント

イベント情報を追加します。ファイル: `src/content/events/YYYY-MM-DD.md`

→ [イベント追加手順](Manual/add-event.md) ／ [テンプレート](Manual/templates/event.md)

### TCUダイバーシティ通信

通信の新号を追加します。ファイル: `src/content/communication/VolXX.md`

→ [通信追加手順](Manual/add-communication.md) ／ [テンプレート](Manual/templates/communication.md)

### ロールモデル集

卒業生・教員ロールモデル集の新号を追加します。

→ [ロールモデル追加手順](Manual/add-rolemodel.md) ／ テンプレート: [卒業生](Manual/templates/rolemodel.md) ・ [教員](Manual/templates/t_rolemodel.md)

### ライブラリ連載

イクボス・まどか・Work in Life・岡田先生コラムの新記事を追加します。

→ [ライブラリ追加手順](Manual/add-library.md) ／ [テンプレート](Manual/templates/library.md)

### 既存コンテンツの編集

お知らせ・イベント・固定ページの修正・更新をします。

→ [編集手順](Manual/edit-page.md)

---

## 公開

コンテンツの追加・編集後、サイトに反映するための手順です。

→ [公開手順（commit & push）](Manual/publish.md)

---

## ローカルプレビュー

編集中のサイトをブラウザで確認できます（環境構築が必要）。

```bash
cd ~/GitHub/diversity_hp
npm run dev
```

ブラウザで http://localhost:4321/ を開く。停止は `Ctrl+C`。
