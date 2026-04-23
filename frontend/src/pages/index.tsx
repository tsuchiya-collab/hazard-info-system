import { useState } from 'react'
import axios from 'axios'
import HazardForm from '@/components/HazardForm'
import HazardResult from '@/components/HazardResult'
import LoadingSpinner from '@/components/LoadingSpinner'

interface HazardData {
  success: boolean
  address: string
  latitude: number
  longitude: number
  hazard_info: any
  message?: string
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<HazardData | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (formData: any) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      const response = await axios.post(`${apiBaseUrl}/api/hazard/check`, formData, {
        timeout: 30000,
      })

      if (response.data.success) {
        setResult(response.data)
      } else {
        setError(response.data.message || 'エラーが発生しました')
      }
    } catch (err: any) {
      if (err.code === 'ECONNREFUSED') {
        setError(
          'バックエンドに接続できません。サーバーが起動していることを確認してください。'
        )
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError(err.message || 'エラーが発生しました')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', paddingTop: '40px', paddingBottom: '40px' }}>
      <div className="container">
        {/* ヘッダー */}
        <div className="card" style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ marginBottom: '10px', color: '#333', fontSize: '32px' }}>
            🏘️ ハザード情報自動取得
          </h1>
          <p style={{ color: '#666', fontSize: '16px', marginBottom: '0' }}>
            住所を入力すると、自動的に災害ハザード情報を取得します
          </p>
        </div>

        {/* フォーム */}
        <div className="card">
          <h2 style={{ marginBottom: '20px', color: '#333' }}>住所情報を入力</h2>
          <HazardForm onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {/* ローディング */}
        {isLoading && <LoadingSpinner />}

        {/* エラー */}
        {error && !isLoading && (
          <div className="card">
            <div className="error">{error}</div>
            <button
              className="button"
              onClick={() => {
                setError(null)
                setResult(null)
              }}
            >
              戻る
            </button>
          </div>
        )}

        {/* 結果 */}
        {result && !isLoading && (
          <div className="card">
            <HazardResult
              address={result.address}
              latitude={result.latitude}
              longitude={result.longitude}
              hazardInfo={result.hazard_info}
            />
            <button
              className="button"
              onClick={() => {
                setResult(null)
                setError(null)
              }}
              style={{ marginTop: '20px' }}
            >
              別の住所を検索
            </button>
          </div>
        )}

        {/* 使い方 */}
        {!result && !isLoading && !error && (
          <div className="card" style={{ backgroundColor: '#f5f5f5' }}>
            <h3 style={{ marginBottom: '15px', color: '#333' }}>📖 使い方</h3>
            <ol style={{ color: '#666', lineHeight: '1.8', marginLeft: '20px' }}>
              <li>住所を入力してください（例：神奈川県横須賀市望洋台20-3）</li>
              <li>「ハザード情報を取得」ボタンをクリック</li>
              <li>
                各ハザード区域の情報が表示されます。「要確認」「指定あり」の場合は、リンクから詳細を確認してください
              </li>
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}
