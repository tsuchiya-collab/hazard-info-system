# ⚡ クイックスタート（30分で完成）

## 必要な準備（手動：10分）

### ステップ 1: 不動産情報ライブラリ API キーを申請

1. ブラウザで開く：https://www.reinfolib.mlit.go.jp/api/request/
2. フォームに入力：
   - 団体名：ランドトラスト（または会社名）
   - 用途：不動産物件管理システムへの災害ハザード情報自動取得
3. 「申請」をクリック
4. **5営業日で APIキーが届く** ← これをメモしておく

### ステップ 2: Salesforce OAuth 設定

#### 2-1. Connected App を作成

1. Salesforce → 設定 → App Manager
2. 「New Connected App」をクリック
3. 入力：
   - **Connected App Name**: `Hazard Info API`
   - **API Name**: `Hazard_Info_API`
   - **Description**: `Hazard Information Auto Input`
4. 「OAuth Settings」で「Enable OAuth Settings」をチェック
5. Callback URL: `http://localhost:8888/callback` （何でもOK）
6. **保存**

#### 2-2. クライアント情報を取得

1. 作成した App を App Manager で開く
2. 「Manage Consumer Details」をクリック
3. **以下をコピーして控える**：
   - Client ID
   - Client Secret

#### 2-3. Salesforce ユーザー情報

以下を確認：
- Salesforce ユーザー名（メールアドレス）
- Salesforce パスワード + セキュリティトークン

**セキュリティトークンの取得**：
- Salesforce → ユーザー設定 → 「セキュリティトークンをリセット」
- メールで新しいトークンが届く

---

## 自動デプロイ（手動：20分）

### ステップ 3: セットアップスクリプトを実行

```bash
cd "/Users/tsuchiya/Projects/⑤ハザード情報自動取得"
bash SETUP_AUTO.sh
```

このスクリプトが自動で以下をやります：
✅ GitHub にリポジトリ作成・プッシュ
✅ 環境変数ファイル作成
✅ デプロイ手順書を生成

### ステップ 4: Render にデプロイ（5分）

スクリプトの指示に従って：

1. https://render.com にログイン
2. 「New Web Service」を選択
3. GitHub リポジトリを選択
4. **以下を入力**：
   ```
   Build Command: pip install -r backend/requirements.txt && pip install uvicorn
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. 「Create」をクリック
6. **デプロイ完了を待つ** （5～10分）
7. **生成された URL をコピー** （例：`https://hazard-backend-xxxxx.onrender.com`）

### ステップ 5: Vercel にデプロイ（5分）

1. https://vercel.com にログイン
2. 「Add New Project」を選択
3. GitHub リポジトリを選択
4. **ルートディレクトリ**: `./frontend`
5. **環境変数を追加**:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://hazard-backend-xxxxx.onrender.com
   ```
   （👆 Render URL を貼り付け）
6. 「Deploy」をクリック
7. **デプロイ完了を待つ** （3～5分）
8. **生成された URL をメモ** （例：`https://hazard-info-frontend.vercel.app`）

---

## ✅ テスト（5分）

### テスト 1: API が生きているか

```bash
bash test_api.sh
```

Render URL を入力して実行。

### テスト 2: フロントエンドを開く

ブラウザで Vercel URL を開く：
```
https://hazard-info-frontend.vercel.app
```

### テスト 3: 実際に検索

1. 住所を入力：`神奈川県横須賀市望洋台20-3`
2. 「ハザード情報を取得」をクリック
3. **ハザード情報が表示される** ✅

### テスト 4: Salesforce 自動入力（オプション）

1. Salesforce で物件 ID をコピー
2. フロントエンド画面に ID を入力
3. 「Salesforce に自動入力する」をチェック
4. 実行
5. **Salesforce レコードに値が入っている** ✅

---

## 🎉 完成！

これで全部完成です。おめでとう！🚀

---

## トラブルシューティング

### ❌ API キーを忘れた

新しく申請してください。5営業日かかります。

### ❌ Salesforce 認証エラー

- パスワード + セキュリティトークン（スペースなし）が正しいか確認
- Connected App が正しく作成されているか確認

### ❌ Render でデプロイが失敗

Render のダッシュボード → Logs でエラーメッセージを確認。

### ❌ Vercel が「API に接続できない」エラー

Render の URL が正しいか確認。スリープ中の可能性もあります。

---

## 次のステップ（オプション）

- [ ] LandtrustAI に統合
- [ ] 複数物件の一括登録
- [ ] メール通知機能
- [ ] ダッシュボード

楽しい開発を！
