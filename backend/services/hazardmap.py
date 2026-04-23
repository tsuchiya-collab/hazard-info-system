import requests
import math
from typing import Optional, Dict, Any
import json

MLIT_API_BASE_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external"

def lat_lon_to_tile(lat: float, lon: float, zoom: int) -> tuple:
    """
    緯度経度をXYZタイル座標に変換する
    """
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)

    lat_rad = math.radians(lat)
    y = int(
        (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
    )

    return x, y, zoom

def fetch_hazard_data(
    api_id: str,
    lat: float,
    lon: float,
    api_key: str,
    zoom: int = 15
) -> Optional[Dict[str, Any]]:
    """
    不動産情報ライブラリAPIからハザード情報を取得する
    """
    try:
        x, y, z = lat_lon_to_tile(lat, lon, zoom)

        url = f"{MLIT_API_BASE_URL}/{api_id}"
        params = {
            "response_format": "geojson",
            "z": z,
            "x": x,
            "y": y
        }
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        print(f"不動産情報ライブラリAPI エラー ({api_id}): {e}")
        return None

def determine_hazard_status(geojson_data: Optional[Dict]) -> str:
    """
    GeoJSONデータからハザード区域の判定を行う
    タイル内にフィーチャーが存在すれば「要確認」と判定
    """
    if not geojson_data:
        return "外"

    features = geojson_data.get("features", [])
    if len(features) > 0:
        return "要確認"

    return "外"

async def get_all_hazard_info(
    lat: float,
    lon: float,
    api_key: str
) -> Dict[str, Any]:
    """
    各種ハザード情報を一括取得する
    """
    zoom = 15

    # タイル座標を先に計算（複数API呼び出しで使用）
    x, y, z = lat_lon_to_tile(lat, lon, zoom)

    hazard_info = {
        "flood_zone": "外",
        "flood_depth_min": None,
        "flood_depth_max": None,
        "flood_url": None,
        "landslide_zone": "外",
        "landslide_url": None,
        "tsunami_zone": "外",
        "tsunami_url": None,
        "hazard_zone": "外",
        "hazard_url": None,
    }

    # 洪水浸水想定区域（XKT026）
    try:
        flood_data = fetch_hazard_data("XKT026", lat, lon, api_key, zoom)
        if flood_data and flood_data.get("features"):
            hazard_info["flood_zone"] = "要確認"
            hazard_info["flood_url"] = f"{MLIT_API_BASE_URL}/XKT026?response_format=geojson&z={z}&x={x}&y={y}"
    except Exception as e:
        print(f"洪水情報取得エラー: {e}")

    # 土砂災害警戒区域（XKT027）
    try:
        landslide_data = fetch_hazard_data("XKT027", lat, lon, api_key, zoom)
        if landslide_data and landslide_data.get("features"):
            hazard_info["landslide_zone"] = "要確認"
            hazard_info["landslide_url"] = f"{MLIT_API_BASE_URL}/XKT027?response_format=geojson&z={z}&x={x}&y={y}"
    except Exception as e:
        print(f"土砂災害情報取得エラー: {e}")

    # 津波浸水想定（XKT028）
    try:
        tsunami_data = fetch_hazard_data("XKT028", lat, lon, api_key, zoom)
        if tsunami_data and tsunami_data.get("features"):
            hazard_info["tsunami_zone"] = "指定あり"
            hazard_info["tsunami_url"] = f"{MLIT_API_BASE_URL}/XKT028?response_format=geojson&z={z}&x={x}&y={y}"
    except Exception as e:
        print(f"津波情報取得エラー: {e}")

    # 災害危険区域（XKT016 - 造成宅地防災区域）
    try:
        hazard_data = fetch_hazard_data("XKT016", lat, lon, api_key, zoom)
        if hazard_data and hazard_data.get("features"):
            hazard_info["hazard_zone"] = "内"
            hazard_info["hazard_url"] = f"{MLIT_API_BASE_URL}/XKT016?response_format=geojson&z={z}&x={x}&y={y}"
    except Exception as e:
        print(f"造成宅地情報取得エラー: {e}")

    return hazard_info
