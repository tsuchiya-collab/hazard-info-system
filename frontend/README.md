# ハザード情報自動取得 - フロントエンド

React + Next.js で構築された、ハザード情報自動取得・Salesforce 自動入力アプリケーション。

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.local.example .env.local
```

`.env.local` に以下を設定：

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SALESFORCE_INSTANCE=https://landtrust.my.salesforce.com
```

### 2. 依存パッケージのインストール

```bash
npm install
```

### 3. 開発サーバー起動

```bash
npm run dev
```

ブラウザで `http://localhost:3000` にアクセス。

## ビルド

```bash
npm run build
npm start
```

## Vercel へのデプロイ

### 1. GitHub にプッシュ

```bash
git push origin main
```

### 2. Vercel ダッシュボードで新規プロジェクト作成

- GitHub リポジトリを選択
- プロジェクト名: `hazard-info-frontend`
- Framework Preset: Next.js

### 3. 環境変数の設定

Vercel 設定で以下の環境変数を追加：

```
NEXT_PUBLIC_API_BASE_URL=https://hazard-backend-xxxx.onrender.com
```

（`xxxx` は Render バックエンドの URL に置き換え）

### 4. デプロイ

デプロイボタンをクリック。

## 機能

### 住所からハザード情報を取得

- 国土地理院 API でジオコーディング
- 不動産情報ライブラリ API でハザード情報取得
- リアルタイム表示

### Salesforce 自動入力

- 物件 ID を入力することで、結果を自動的に物件レコードに入力
- オプション機能（チェックボックスで有効化）

### レスポンシブデザイン

- PC / タブレット / スマートフォン対応

## トラブルシューティング

### バックエンドに接続できない

```
バックエンドに接続できません。サーバーが起動していることを確認してください。
```

バックエンド（Render）が起動していることを確認：
```bash
curl https://hazard-backend-xxxx.onrender.com/health
```

### Salesforce 自動入力が失敗

バックエンド側のログを確認：
```bash
Render ダッシュボード → Logs
```

## 技術スタック

- **フロントエンド**: React 18 + Next.js 14
- **スタイリング**: CSS in JS (グローバルCSS)
- **HTTP クライアント**: Axios
- **デプロイ**: Vercel
- **言語**: TypeScript
