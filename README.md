# ハザード情報自動取得システム

不動産物件の住所から、自動的にハザード情報（洪水・土砂災害・津波・造成宅地防災）を取得し、Salesforce に自動入力するシステム。

## システム構成

```
┌─────────────────────────────────────────────┐
│      Frontend (Next.js + React)             │
│   Vercel にデプロイ                         │
│  - 住所入力フォーム                          │
│  - ハザード情報表示                         │
│  - Salesforce 自動入力ボタン                │
└──────────────────┬──────────────────────────┘
                   │ API 呼び出し
                   ▼
┌─────────────────────────────────────────────┐
│     Backend (FastAPI + Python)              │
│   Render にデプロイ                         │
│  - 国土地理院 API（ジオコーディング）      │
│  - 不動産情報ライブラリ API（ハザード）    │
│  - Salesforce REST API（自動入力）         │
└─────────────────────────────────────────────┘
```

## 無料で動く理由

- **国土地理院 API**: 完全無料・登録不要
- **不動産情報ライブラリ API**: 完全無料（無料申請）
- **Vercel**: フロントエンド無料ホスティング
- **Render**: バックエンド無料ホスティング（スリープあり）
- **Salesforce API**: 既存ライセンスで無料利用可

## クイックスタート

### 1. バックエンド準備（Render）

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# .env を編集（MLIT_API_KEY, Salesforce認証情報を設定）
uvicorn main:app --reload
```

### 2. フロントエンド準備（Vercel）

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

ブラウザで `http://localhost:3000` を開く。

### 3. デプロイ

#### バックエンド（Render）

1. GitHub にプッシュ
2. Render ダッシュボードで新規サービス作成
3. `render.yaml` を参照して自動設定
4. 環境変数を設定してデプロイ

#### フロントエンド（Vercel）

1. GitHub にプッシュ
2. Vercel で新規プロジェクト作成
3. 環境変数を設定してデプロイ

## 実装に必要な確認事項

### 1. 不動産情報ライブラリ API キー申請

👉 https://www.reinfolib.mlit.go.jp/api/request/

申請から5営業日で承認。

### 2. Salesforce フィールド API 名確認

以下のフィールド名を確認して、`backend/services/salesforce.py` に記入：

- 造成宅地防災区域フィールド名
- 土砂災害警戒区域フィールド名
- 津波災害警戒区域フィールド名
- 各情報のURLフィールド名
- 最終確認日フィールド名

### 3. Salesforce OAuth 認証情報取得

Salesforce 設定で、OAuth 2.0 Connected App を作成し、以下を取得：

- Client ID
- Client Secret
- Username
- Password

## 運用方法

### パターン1: Web アプリで検索

1. フロントエンドアプリで住所を入力
2. ハザード情報が表示される
3. 必要に応じて「Salesforce に自動入力」をクリック

### パターン2: API 直接呼び出し（プログラム連携）

```bash
curl -X POST http://localhost:8000/api/hazard/check \
  -H "Content-Type: application/json" \
  -d '{
    "address": "神奈川県横須賀市望洋台20-3",
    "bukken_id": "a00Q800001CT3JMIA1",
    "update_salesforce": true
  }'
```

## 費用見積もり

| 項目 | 費用 | 備考 |
|---|---|---|
| 国土地理院 API | 無料 | 登録不要 |
| 不動産情報ライブラリ API | 無料 | 申請のみ必要 |
| Vercel（フロントエンド） | 無料 | 月100GB転送量まで無料 |
| Render（バックエンド） | 無料 | 15分以上アイドルでスリープ |
| Salesforce API | 無料 | 既存ライセンス内で利用 |
| **合計** | **0円** | |

※ Render の無料プランは、15分以上リクエストがないとスリープします。本番環境では有料プランが推奨されます（月$7〜）。

## トラブルシューティング

### バックエンドが立ち上がらない

```bash
# 依存パッケージを確認
pip install -r requirements.txt

# ログを確認
uvicorn main:app --log-level=debug
```

### Salesforce 自動入力が失敗

1. API キーが正しいか確認
2. フィールド名が正しいか確認（`backend/services/salesforce.py`）
3. Salesforce ユーザーが十分な権限を持っているか確認

### 「住所が見つかりません」エラー

国土地理院 API の制限により、番地が不正確な場合は市区町村レベルの座標が返却されます。住所をより具体的に入力してください。

## 技術ドキュメント

- [バックエンド](./backend/README.md)
- [フロントエンド](./frontend/README.md)

## ライセンス

MIT
