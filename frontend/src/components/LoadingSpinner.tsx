import React from 'react'

export default function LoadingSpinner() {
  return (
    <div style={{ textAlign: 'center', padding: '40px 20px' }}>
      <div className="spinner"></div>
      <p style={{ color: '#666', marginTop: '20px' }}>ハザード情報を取得中...</p>
    </div>
  )
}
