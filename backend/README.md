# ハザード情報自動取得 API

住所からハザード情報を自動取得し、Salesforce に自動入力するバックエンドAPI。

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
```

以下の環境変数を `.env` に設定：

- `MLIT_API_KEY`: 不動産情報ライブラリAPIキー（要申請: https://www.reinfolib.mlit.go.jp/api/request/）
- `SALESFORCE_INSTANCE`: Salesforce インスタンスURL
- `SALESFORCE_CLIENT_ID`: OAuth クライアントID
- `SALESFORCE_CLIENT_SECRET`: OAuth クライアントシークレット
- `SALESFORCE_USERNAME`: Salesforce ユーザー名
- `SALESFORCE_PASSWORD`: Salesforce パスワード

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. ローカルサーバー起動

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API ドキュメント: http://localhost:8000/docs

## API エンドポイント

### POST /api/hazard/check

住所からハザード情報を取得する

**リクエスト:**
```json
{
  "address": "神奈川県横須賀市望洋台20-3",
  "bukken_id": "a00Q800001CT3JMIA1",
  "update_salesforce": true
}
```

**レスポンス:**
```json
{
  "success": true,
  "address": "神奈川県横須賀市望洋台20-3",
  "latitude": 35.673,
  "longitude": 139.752,
  "hazard_info": {
    "flood_zone": "外",
    "flood_url": "...",
    "landslide_zone": "外",
    "landslide_url": "...",
    "tsunami_zone": "外",
    "tsunami_url": "...",
    "hazard_zone": "外",
    "hazard_url": "...",
    "confirmed_at": "2026-04-23"
  },
  "salesforce_updated": true,
  "message": "ハザード情報を取得しました"
}
```

## Render へのデプロイ

1. GitHub にリポジトリをプッシュ
2. Render ダッシュボードで新規 Web Service 作成
3. `render.yaml` を参照して自動設定
4. 環境変数を設定
5. デプロイ

## Salesforce フィールド名設定

`services/salesforce.py` の `update_bukken_hazard_info` 関数内のコメント部分を、Salesforce の実際のフィールドAPI名で埋める必要があります。

確認対象フィールド：
- 造成宅地防災区域
- 土砂災害警戒区域
- 津波災害警戒区域
- 各情報のURL
- 最終確認日

## トラブルシューティング

### APIキーエラー
不動産情報ライブラリAPIキーが設定されているか確認：
```bash
echo $MLIT_API_KEY
```

### Salesforce 接続エラー
認証情報が正しいか、インスタンスURLが正しいか確認。

### 住所が見つからない
国土地理院API の制限により、番地が不正確な場合は市区町村レベルの座標が返却されます。

## 注意

- 不動産情報ライブラリAPI：月400コール程度で問題なし（月10～100件規模）
- 国土地理院API：無料・登録不要
- Salesforce 自動入力：フィールド名が確認されるまでは無効
