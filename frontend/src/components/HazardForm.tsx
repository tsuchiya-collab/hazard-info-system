import React, { useState } from 'react'

interface HazardFormProps {
  onSubmit: (data: any) => void
  isLoading: boolean
}

export default function HazardForm({ onSubmit, isLoading }: HazardFormProps) {
  const [address, setAddress] = useState('')
  const [bukkenId, setBukkenId] = useState('')
  const [updateSalesforce, setUpdateSalesforce] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!address.trim()) {
      alert('住所を入力してください')
      return
    }

    const payload = {
      address: address.trim(),
      bukken_id: bukkenId.trim() || null,
      update_salesforce: updateSalesforce,
    }

    onSubmit(payload)
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <label htmlFor="address">住所 *</label>
        <input
          id="address"
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="例：神奈川県横須賀市望洋台20-3"
          disabled={isLoading}
        />
      </div>

      <div className="input-group">
        <label htmlFor="bukkenId">物件ID（Salesforce）</label>
        <input
          id="bukkenId"
          type="text"
          value={bukkenId}
          onChange={(e) => setBukkenId(e.target.value)}
          placeholder="例：a00Q800001CT3JMIA1"
          disabled={isLoading}
        />
      </div>

      <div className="checkbox-group">
        <input
          id="updateSalesforce"
          type="checkbox"
          checked={updateSalesforce}
          onChange={(e) => setUpdateSalesforce(e.target.checked)}
          disabled={isLoading || !bukkenId.trim()}
        />
        <label htmlFor="updateSalesforce" style={{ marginBottom: 0 }}>
          Salesforce に自動入力する
          {!bukkenId.trim() && (
            <span style={{ color: '#999', fontSize: '12px' }}>
              {' '}
              (物件ID が必要)
            </span>
          )}
        </label>
      </div>

      <button type="submit" className="button" disabled={isLoading}>
        {isLoading ? 'ハザード情報を取得中...' : 'ハザード情報を取得'}
      </button>
    </form>
  )
}
