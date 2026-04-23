import { useState } from 'react'

interface HazardFormProps {
  onSubmit: (data: any) => void
  isLoading: boolean
}

export default function HazardForm({ onSubmit, isLoading }: HazardFormProps) {
  const [address, setAddress] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!address.trim()) {
      alert('住所を入力してください')
      return
    }

    onSubmit({ address: address.trim() })
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

      <button type="submit" className="button" disabled={isLoading}>
        {isLoading ? 'ハザード情報を取得中...' : 'ハザード情報を取得'}
      </button>
    </form>
  )
}
