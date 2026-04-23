#!/bin/bash

set -e

echo "================================"
echo "🚀 ハザード情報システム自動セットアップ"
echo "================================"
echo ""

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ステップ 1-2: 手動準備の確認
echo -e "${BLUE}【ステップ 1-2】手動準備の確認（5分）${NC}"
echo ""
echo "以下の作業をお願いします："
echo ""
echo "1️⃣  不動産情報ライブラリ API キー申請"
echo "   👉 https://www.reinfolib.mlit.go.jp/api/request/"
echo "   申請完了後、APIキーをコピーしておいてください"
echo ""
echo "2️⃣  Salesforce OAuth Connected App 作成"
echo "   設定 → App Manager → New Connected App"
echo "   - Client ID と Client Secret をコピー"
echo ""

read -p "上記の準備は完了しましたか？ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${RED}準備完了後に再度実行してください${NC}"
  exit 1
fi

echo ""
echo -e "${GREEN}✅ 準備確認完了${NC}"
echo ""

# ステップ 3: GitHub に自動プッシュ
echo -e "${BLUE}【ステップ 3】GitHub に自動プッシュ${NC}"
echo ""

read -p "GitHub ユーザー名を入力: " GITHUB_USER
read -p "リポジトリ名を入力（デフォルト: hazard-info-system）: " REPO_NAME
REPO_NAME=${REPO_NAME:-hazard-info-system}

cd "$(dirname "$0")"

# Git 初期化
if [ ! -d .git ]; then
  git init
  git config user.name "$GITHUB_USER"
  git config user.email "$GITHUB_USER@users.noreply.github.com"
fi

# .gitignore 作成
cat > .gitignore <<EOF
backend/.env
frontend/.env.local
__pycache__/
node_modules/
.next/
dist/
.vercel
.DS_Store
EOF

# コミット
git add -A
git commit -m "Initial commit: Hazard Information Auto System" || true

# リモートを設定
REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"
git branch -M main

echo ""
echo "📝 GitHub にリポジトリを作成してください（もしまだなら）"
echo "   👉 https://github.com/new"
echo "   リポジトリ名: $REPO_NAME"
echo ""
read -p "リポジトリ作成完了した？ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  exit 1
fi

echo "🔄 GitHub にプッシュ中..."
git push -u origin main

echo -e "${GREEN}✅ GitHub プッシュ完了${NC}"
echo ""

# ステップ 3: 環境変数の入力
echo -e "${BLUE}【ステップ 3】環境変数を入力${NC}"
echo ""

read -p "MLIT API キーを入力: " MLIT_API_KEY
read -p "Salesforce Client ID を入力: " SALESFORCE_CLIENT_ID
read -p "Salesforce Client Secret を入力: " SALESFORCE_CLIENT_SECRET
read -p "Salesforce ユーザー名を入力: " SALESFORCE_USERNAME
read -sp "Salesforce パスワード+トークンを入力: " SALESFORCE_PASSWORD
echo

# backend/.env を作成
cat > backend/.env <<EOF
MLIT_API_KEY=$MLIT_API_KEY
SALESFORCE_INSTANCE=https://landtrust.my.salesforce.com
SALESFORCE_CLIENT_ID=$SALESFORCE_CLIENT_ID
SALESFORCE_CLIENT_SECRET=$SALESFORCE_CLIENT_SECRET
SALESFORCE_USERNAME=$SALESFORCE_USERNAME
SALESFORCE_PASSWORD=$SALESFORCE_PASSWORD
FRONTEND_URL=https://$REPO_NAME-frontend.vercel.app
EOF

echo -e "${GREEN}✅ 環境変数ファイル作成完了${NC}"
echo ""

# ステップ 4-5: デプロイメモ
echo -e "${BLUE}【ステップ 4-5】Render & Vercel にデプロイ${NC}"
echo ""

cat > DEPLOY_INSTRUCTIONS.txt <<EOF
🚀 デプロイ手順（手動）

【Render - バックエンド】
1. https://render.com にログイン
2. Dashboard → "New +" → "Web Service"
3. GitHub リポジトリ選択: $GITHUB_USER/$REPO_NAME
4. 設定:
   - Name: hazard-backend
   - Build Command: pip install -r backend/requirements.txt && pip install uvicorn
   - Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT
   - Root Directory: ./
5. "Create Web Service"をクリック
6. 自動デプロイ開始（5～10分待つ）
7. デプロイURL をコピー: https://hazard-backend-xxxxx.onrender.com

【Vercel - フロントエンド】
1. https://vercel.com にログイン
2. "Add New..." → "Project"
3. GitHub リポジトリ選択: $GITHUB_USER/$REPO_NAME
4. 設定:
   - Framework: Next.js
   - Root Directory: ./frontend
5. Environment Variables を追加:
   - NEXT_PUBLIC_API_BASE_URL: https://hazard-backend-xxxxx.onrender.com (👆 Render URL)
6. "Deploy" をクリック
7. デプロイURL をメモ: https://$REPO_NAME-frontend.vercel.app

【確認】
✅ Render ダッシュボード → Logs で "Uvicorn running..." を確認
✅ ブラウザで frontend URL にアクセス
✅ 住所を入力して動作確認

完了！🎉
EOF

cat DEPLOY_INSTRUCTIONS.txt

echo ""
echo -e "${YELLOW}⚠️  次のステップ（手動）:${NC}"
echo ""
echo "1. Render でバックエンドをデプロイ"
echo "2. Vercel でフロントエンドをデプロイ"
echo "3. ブラウザでテスト"
echo ""
echo "詳しくは DEPLOY_INSTRUCTIONS.txt を確認してください"
echo ""
echo -e "${GREEN}自動セットアップ完了！🎉${NC}"
