# 公開手順（commit & push）

コンテンツの追加・編集が完了したら、以下の手順で公開します。

---

## GitHub Desktop で公開する

### 1. 変更を確認する

GitHub Desktop を開くと、左側の **Changes** タブに変更されたファイルが一覧表示されます。

- ファイル名をクリックすると、右側に変更内容（差分）が表示されます
- 意図しないファイルが含まれていないか確認してください

### 2. コミットする

1. 左下の **Summary** 欄にコミットメッセージを入力  
   例: `news: シンポジウム告知を追加`
2. 「**Commit to main**」ボタンをクリック

> **コミットメッセージの書き方**:  
> `種類: 内容の要約` の形式で書くと分かりやすくなります。  
> - `news: ○○のお知らせを追加`  
> - `events: ○○イベント情報を追加`  
> - `communication: Vol.21を追加`  
> - `fix: ○○の日付を修正`

### 3. プッシュする

コミット後、上部に「**Push origin**」ボタンが表示されます。クリックすると GitHub にアップロードされます。

### 4. 公開を確認する

- push から数分で自動ビルドが走り、サイトに反映されます
- ビルドの進行状況: https://github.com/diversity-tcu/diversity_hp/actions
- 公開サイト: https://diversity-tcu.github.io/diversity_hp/

---

## AI（Claude）に依頼する場合

コンテンツ編集後に以下のように伝えるだけで OK です:

> 「push して」

AI が commit → push まで自動で実行します。

---

## トラブルシューティング

| 症状 | 対処 |
|------|------|
| Push ボタンが表示されない | Commit が完了しているか確認。Changes タブにファイルが残っていればまだ Commit していません |
| Push でエラーが出る | 「**Fetch origin**」→「**Pull origin**」で最新を取得してから再度 Push |
| ビルドが失敗した | [Actions ページ](https://github.com/diversity-tcu/diversity_hp/actions) でエラー内容を確認し、AI に修正を依頼 |
