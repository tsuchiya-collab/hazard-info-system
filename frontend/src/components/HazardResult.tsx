interface HazardInfo {
  flood_zone?: string
  flood_depth_min?: number
  flood_depth_max?: number
  flood_url?: string
  landslide_zone?: string
  landslide_url?: string
  tsunami_zone?: string
  tsunami_url?: string
  hazard_zone?: string
  hazard_url?: string
  confirmed_at: string
}

interface HazardResultProps {
  address: string
  latitude: number
  longitude: number
  hazardInfo: HazardInfo
  salesforceUpdated: boolean
  message?: string
}

export default function HazardResult({
  address,
  latitude,
  longitude,
  hazardInfo,
  salesforceUpdated,
  message,
}: HazardResultProps) {
  const getStatusColor = (value: string) => {
    if (value === '要確認' || value === '指定あり' || value === '内') {
      return '#f44336'
    }
    return '#4caf50'
  }

  return (
    <div>
      {salesforceUpdated && (
        <div className="success">
          ✅ Salesforce に自動入力しました！
        </div>
      )}

      <div className="card">
        <h2 style={{ marginBottom: '20px', color: '#333' }}>ハザード情報</h2>

        <div style={{ marginBottom: '20px', paddingBottom: '20px', borderBottom: '2px solid #e0e0e0' }}>
          <p style={{ marginBottom: '8px' }}>
            <strong>住所：</strong> {address}
          </p>
          <p style={{ marginBottom: '8px' }}>
            <strong>座標：</strong> {latitude.toFixed(6)}, {longitude.toFixed(6)}
          </p>
          <p style={{ fontSize: '12px', color: '#999' }}>
            確認日時：{hazardInfo.confirmed_at}
          </p>
        </div>

        <div className="result-grid">
          {/* 洪水浸水想定 */}
          <div className="hazard-item">
            <div className="hazard-item-label">洪水浸水想定区域</div>
            <div
              className="hazard-item-value"
              style={{ color: getStatusColor(hazardInfo.flood_zone || '') }}
            >
              {hazardInfo.flood_zone || '不明'}
            </div>
            {hazardInfo.flood_depth_min !== undefined && hazardInfo.flood_depth_max !== undefined && (
              <div style={{ fontSize: '12px', color: '#666', marginBottom: '8px' }}>
                浸水深：{hazardInfo.flood_depth_min}～{hazardInfo.flood_depth_max}m
              </div>
            )}
            {hazardInfo.flood_url && (
              <div className="hazard-item-url">
                📎{' '}
                <a href={hazardInfo.flood_url} target="_blank" rel="noopener noreferrer">
                  詳細を確認
                </a>
              </div>
            )}
          </div>

          {/* 土砂災害警戒区域 */}
          <div className="hazard-item">
            <div className="hazard-item-label">土砂災害警戒区域</div>
            <div
              className="hazard-item-value"
              style={{ color: getStatusColor(hazardInfo.landslide_zone || '') }}
            >
              {hazardInfo.landslide_zone || '不明'}
            </div>
            {hazardInfo.landslide_url && (
              <div className="hazard-item-url">
                📎{' '}
                <a href={hazardInfo.landslide_url} target="_blank" rel="noopener noreferrer">
                  詳細を確認
                </a>
              </div>
            )}
          </div>

          {/* 津波浸水想定 */}
          <div className="hazard-item">
            <div className="hazard-item-label">津波浸水想定区域</div>
            <div
              className="hazard-item-value"
              style={{ color: getStatusColor(hazardInfo.tsunami_zone || '') }}
            >
              {hazardInfo.tsunami_zone || '不明'}
            </div>
            {hazardInfo.tsunami_url && (
              <div className="hazard-item-url">
                📎{' '}
                <a href={hazardInfo.tsunami_url} target="_blank" rel="noopener noreferrer">
                  詳細を確認
                </a>
              </div>
            )}
          </div>

          {/* 造成宅地防災区域 */}
          <div className="hazard-item">
            <div className="hazard-item-label">造成宅地防災区域</div>
            <div
              className="hazard-item-value"
              style={{ color: getStatusColor(hazardInfo.hazard_zone || '') }}
            >
              {hazardInfo.hazard_zone || '不明'}
            </div>
            {hazardInfo.hazard_url && (
              <div className="hazard-item-url">
                📎{' '}
                <a href={hazardInfo.hazard_url} target="_blank" rel="noopener noreferrer">
                  詳細を確認
                </a>
              </div>
            )}
          </div>
        </div>

        <div style={{ marginTop: '20px', padding: '12px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <p style={{ fontSize: '12px', color: '#666', marginBottom: '0' }}>
            ℹ️ 「要確認」「指定あり」「内」と表示された場合は、リンクから詳細を確認してください。
          </p>
        </div>
      </div>
    </div>
  )
}
