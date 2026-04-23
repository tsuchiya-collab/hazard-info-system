import requests
from typing import Tuple, Optional

GSI_GEOCODING_URL = "https://msearch.gsi.go.jp/address-search/AddressSearch"

async def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """
    国土地理院APIを使用して、住所から緯度経度を取得する
    戻り値: (latitude, longitude) または None
    """
    try:
        params = {"q": address}
        response = requests.get(GSI_GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()

        results = response.json()
        if not results or len(results) == 0:
            return None

        # 最初の結果を取得
        result = results[0]
        coordinates = result.get("geometry", {}).get("coordinates", [])

        if len(coordinates) >= 2:
            lon, lat = coordinates[0], coordinates[1]
            return (lat, lon)

        return None

    except requests.RequestException as e:
        print(f"国土地理院API エラー: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"レスポンスパース エラー: {e}")
        return None
