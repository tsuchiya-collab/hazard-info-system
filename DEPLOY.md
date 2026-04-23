# デプロイガイド

無料でハザード情報自動取得システムを Render + Vercel にデプロイする手順。

## 事前準備（5分）

### 1. 不動産情報ライブラリ API キーの取得

1. 👉 https://www.reinfolib.mlit.go.jp/api/request/ にアクセス
2. 団体名・用途を入力して申請
3. 5営業日で承認 → APIキーが届く
4. APIキーを控えておく

### 2. Salesforce 認証情報の取得

#### 2-1. OAuth Connected App の作成

1. Salesforce 設定 → App Manager
2. 「New Connected App」をクリック
3. 基本情報を入力：
   - Connected App Name: `Hazard Info API`
   - API Name: `Hazard_Info_API`
   - Description: `Hazard Information Auto Input`
4. OAuth Settings を有効化：
   - Callback URL: `http://localhost:8888/callback` （ローカル用ダミー）
5. 保存

#### 2-2. クライアント情報を取得

1. 作成した App Manager の詳細を開く
2. 「Manage Consumer Details」をクリック
3. **Client ID** と **Client Secret** をコピーして控える

#### 2-3. ユーザー名とパスワード

- Salesforce ユーザー名（メールアドレス）
- Salesforce パスワード + セキュリティトークン

### 3. Salesforce フィールド API 名の確認

Salesforce で物件レコード（bukken__c）を開いて、以下のフィールド API 名を確認：

```
- 造成宅地防災区域: ______________________
- 造成宅地URL: ______________________
- 土砂災害警戒区域: ______________________
- 土砂災害URL: ______________________
- 津波災害警戒区域: ______________________
- 津波災害URL: ______________________
- 最終確認日: ______________________
```

---

## ステップ 1: バックエンド (Render) にデプロイ（15分）

### 1-1. GitHub にプッシュ

```bash
cd "/Users/tsuchiya/Projects/⑤ハザード情報自動取得"
git init
git add -A
git commit -m "Initial commit: Hazard Information System"
git remote add origin https://github.com/tsuchiya/hazard-info-backend.git
git branch -M main
git push -u origin main
```

（GitHub にリポジトリを先に作成しておいてください）

### 1-2. Render でサービス作成

1. 👉 https://render.com にログイン
2. ダッシュボード → 「New +」 → 「Web Service」
3. GitHub リポジトリを選択（`hazard-info-backend`）
4. 設定：
   - **Name**: `hazard-backend`
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. 「Create Web Service」をクリック

### 1-3. 環境変数を設定

Render のサービス設定で「Environment」→「Add Environment Variable」：

| Key | Value |
|---|---|
| `MLIT_API_KEY` | 👆事前準備で取得したAPIキー |
| `SALESFORCE_INSTANCE` | `https://landtrust.my.salesforce.com` |
| `SALESFORCE_CLIENT_ID` | Connected App の Client ID |
| `SALESFORCE_CLIENT_SECRET` | Connected App の Client Secret |
| `SALESFORCE_USERNAME` | Salesforce ユーザー名 |
| `SALESFORCE_PASSWORD` | Salesforce パスワード+セキュリティトークン |
| `FRONTEND_URL` | Vercel デプロイ後の URL（後で更新） |

### 1-4. Salesforce フィールド名を設定

1. `backend/services/salesforce.py` を編集
2. `update_data` のコメント部分をアンコメント
3. フィールド API 名を記入（事前準備3-3 で確認した値）
4. GitHub にプッシュ

```python
update_data = {
    "dosha_saigai_keikai_kuiki__c": hazard_info.get("landslide_zone"),  # 実際のフィールド名に変更
    "dosha_saigai_url__c": hazard_info.get("landslide_url"),
    # ... その他フィールド
    "saishuu_kakuninbi__c": str(date.today()),
}
```

### 1-5. デプロイ確認

Render ダッシュボードで「Logs」を確認：

```
Started server process
Uvicorn running on 0.0.0.0:10000
```

と表示されれば OK。

**バックエンド URL をコピー**（例：`https://hazard-backend-xxxx.onrender.com`）

---

## ステップ 2: フロントエンド (Vercel) にデプロイ（10分）

### 2-1. GitHub にプッシュ

```bash
cd "/Users/tsuchiya/Projects/⑤ハザード情報自動取得/frontend"
git add -A
git commit -m "Frontend: Next.js Hazard Info App"
git push origin main
```

### 2-2. Vercel でプロジェクト作成

1. 👉 https://vercel.com にログイン
2. 「Add New...」 → 「Project」
3. GitHub リポジトリを選択（`hazard-info-frontend`）
4. 設定：
   - **Project Name**: `hazard-info-frontend`
   - **Framework**: Next.js
   - **Root Directory**: `frontend` (部分デプロイする場合)

### 2-3. 環境変数を設定

Vercel プロジェクト設定で「Environment Variables」を追加：

| Key | Value |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | 👆ステップ 1-5 でコピーした Render URL |

### 2-4. デプロイ

「Deploy」ボタンをクリック。

完了したら、Vercel から割り当てられた URL をコピー。

---

## ステップ 3: バックエンド環境変数を更新（2分）

### 3-1. Render 環境変数を更新

1. Render サービス設定 → Environment Variables
2. `FRONTEND_URL` を更新：
   ```
   https://hazard-info-frontend.vercel.app
   ```
3. 保存（自動的に再デプロイ）

---

## ✅ デプロイ完了！

以下をテスト：

### テスト 1: バックエンドが生きているか

```bash
curl https://hazard-backend-xxxx.onrender.com/health
# 戻り値: {"status":"ok"}
```

### テスト 2: フロントエンドを開く

ブラウザで `https://hazard-info-frontend.vercel.app` を開く。

### テスト 3: 実際に使ってみる

1. 住所を入力：`神奈川県横須賀市望洋台20-3`
2. 「ハザード情報を取得」をクリック
3. ハザード情報が表示される ✅

### テスト 4: Salesforce 自動入力

1. Salesforce で物件 ID をコピー
2. フロントエンドで物件 ID を入力
3. 「Salesforce に自動入力する」をチェック
4. 実行
5. Salesforce レコードで値が入力されているか確認 ✅

---

## 注意点

### Render の無料プランについて

- ⏰ 15分以上リクエストがないとスリープ
- 😴 スリープ中は初回リクエストが 30～50 秒遅い
- 💰 本番運用なら有料プラン推奨（月 $7）

### スリープ対策

バックエンドを起こしておきたい場合：
1. Render で「Scheduled Event」を設定
2. 10分ごとに `/health` を呼び出す

### 月間コスト

無料プランでこのまま使う場合：**0円**

本番向けに Render 有料プラン にアップグレード：**月 $7～**

---

## トラブルシューティング

### ❌ バックエンドに接続できない

```
バックエンドに接続できません。サーバーが起動していることを確認してください。
```

**原因**: Render がスリープ中、または起動失敗

**対策**:
```bash
curl https://hazard-backend-xxxx.onrender.com/health
```

で状態確認。エラーなら Render ダッシュボードで Logs を確認。

### ❌ 「住所が見つかりません」

国土地理院 API の制限。以下を試す：
- より具体的な住所を入力
- 郵便番号を追加

### ❌ Salesforce 自動入力が失敗

1. バックエンド Logs を確認
2. Salesforce 認証情報が正しいか再確認
3. フィールド API 名が正しいか再確認

---

## 次のステップ

✅ 基本システムが動いている

オプション機能：

- [ ] LandtrustAI プラットフォームに統合
- [ ] 複数物件の一括登録機能
- [ ] API ドキュメント（Swagger）の公開
- [ ] モニタリング・ログ記録の強化
- [ ] メール通知機能

---

**楽しいデプロイを！🚀**
