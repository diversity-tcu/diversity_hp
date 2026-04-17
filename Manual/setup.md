# 環境構築ガイド

GitHub アカウントの作成から、リポジトリのクローンまでの手順です。

---

## 1. GitHub にログイン

1. [github.com](https://github.com/) にアクセス
2. 「Sign in」をクリック
3. アカウント名・パスワードを入力してログイン
```bash
account : diversity-tcu
passwd : divers1TY
```

---

## 2. GitHub Desktop をインストールする

1. [desktop.github.com](https://desktop.github.com/) にアクセス
2. 「Download for Windows」（または macOS）をクリック
3. ダウンロードしたインストーラーを実行
4. インストール完了後、GitHub Desktop を起動
5. 「Sign in to GitHub.com」をクリックし、手順1で作成したアカウントでログイン

---

## 3. リポジトリをクローンする

1. GitHub Desktop のメニューから **File → Clone repository** を選択
2. 「URL」タブを選択
3. 以下のURLを入力:
   ```
   https://github.com/kasekiguchi/diversity_hp.git
   ```
4. **Local path** にクローン先フォルダを指定（例: `C:\Users\<ユーザー名>\GitHub\diversity_hp`）
5. 「Clone」をクリック

クローンが完了すると、GitHub Desktop にリポジトリが表示されます。

---

## 4. ローカルプレビュー環境を準備する（任意）

コンテンツの見た目を事前に確認したい場合は、以下をセットアップしてください。

### 4-1. Node.js をインストール

1. [nodejs.org](https://nodejs.org/) から **LTS版** をダウンロード・インストール
2. コマンドプロンプト（またはターミナル）で確認:
   ```
   node -v
   ```

### 4-2. 依存パッケージをインストール

クローンしたフォルダで以下を実行（初回のみ）:

```
cd ~/GitHub/diversity_hp
npm install
```

### 4-3. プレビューサーバーを起動

```
npm run dev
```

ブラウザで http://localhost:4321/ を開くとサイトが確認できます。  
停止するには `Ctrl+C` を押してください。

---

次のステップ: [コンテンツを追加・編集する →](../README.md)
