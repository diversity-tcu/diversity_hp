# TCUダイバーシティ通信を追加する

---

## 手順

### 1. PDF・サムネイル画像を配置する

1. PDF ファイルを `public/uploads/YYYY/MM/VolXX.pdf` に保存
2. 表紙画像（任意）を `public/uploads/YYYY/MM/VolXX.jpg` に保存

### 2. ファイルを作成する

`src/content/communication/` フォルダに新しい `.md` ファイルを作成します。

- **ファイル名**: `VolXX.md`（号数の連番）

### 3. テンプレートをコピーして編集する

[テンプレート](templates/communication.md) の内容をコピーし、以下を編集してください:

| 項目 | 説明 | 例 |
|------|------|----|
| `title` | 通信のタイトル | `"TCUダイバーシティ通信Vol.21（2026年9月発行）"` |
| `date` | 発行日（YYYY-MM-DD） | `"2026-09-01"` |
| `pdf` | PDF のパス | `"/uploads/2026/09/Vol21.pdf"` |
| `thumb` | 表紙画像のパス（任意） | `"/uploads/2026/09/Vol21.jpg"` |

### 4. 公開する

→ [公開手順（commit & push）](publish.md)

---

## AI に依頼する場合

> 「TCUダイバーシティ通信Vol.21（2026年9月発行）を追加して。PDFは /uploads/2026/09/Vol21.pdf、表紙画像は同フォルダの Vol21.jpg」

---

## 注意事項

- 本文は空でOKです（PDF がメインコンテンツのため）
- `thumb` を省略すると、一覧ページで PDF アイコンが代わりに表示されます
- 一覧は `date` の降順で自動ソートされます
