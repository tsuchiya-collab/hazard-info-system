#!/bin/bash

# ハザード情報 API テストスクリプト

echo "================================"
echo "🧪 ハザード情報 API テスト"
echo "================================"
echo ""

# API URL を入力
read -p "バックエンド URL を入力（例：https://hazard-backend-xxxxx.onrender.com）: " API_URL

if [ -z "$API_URL" ]; then
  echo "❌ URL が入力されていません"
  exit 1
fi

echo ""
echo "🔍 ヘルスチェック..."
HEALTH=$(curl -s "$API_URL/health")
echo "Response: $HEALTH"

if [[ $HEALTH == *"ok"* ]]; then
  echo -e "✅ バックエンド OK\n"
else
  echo -e "❌ バックエンド エラー\n"
  exit 1
fi

echo "📍 テスト住所: 神奈川県横須賀市望洋台20-3"
echo ""
echo "🚀 ハザード情報取得リクエスト送信中..."
echo ""

RESPONSE=$(curl -s -X POST "$API_URL/api/hazard/check" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "神奈川県横須賀市望洋台20-3",
    "update_salesforce": false
  }')

echo "Response:"
echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

echo ""
echo "✅ テスト完了！"
echo ""
echo "レスポンスの確認："
echo "- success: true （成功）"
echo "- latitude/longitude: 座標が返っている"
echo "- hazard_info: ハザード情報が表示されている"
echo ""
echo "🎉 すべてOK なら、フロントエンドアプリで試してみてください！"
