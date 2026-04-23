from fastapi import APIRouter, HTTPException
from datetime import date
import os
from models.hazard import HazardRequest, HazardResponse, HazardInfo
from services.geocoding import get_coordinates
from services.hazardmap import get_all_hazard_info

router = APIRouter(prefix="/api/hazard", tags=["hazard"])

@router.post("/check", response_model=HazardResponse)
async def check_hazard(request: HazardRequest):
    """
    住所からハザード情報を取得する
    MLIT_API_KEY が設定されていない場合はテストデータを返す
    """
    try:
        # ステップ1: 住所をジオコーディング
        coords = await get_coordinates(request.address)
        if not coords:
            raise HTTPException(status_code=400, detail="住所が見つかりません")

        lat, lon = coords

        # ステップ2: ハザード情報を取得
        api_key = os.getenv("MLIT_API_KEY")

        # API キーがない場合はテストデータを使用
        if not api_key:
            hazard_info_dict = {
                "flood_zone": "要確認",
                "flood_depth_min": 0.5,
                "flood_depth_max": 1.5,
                "flood_url": "https://disaportal.gsi.go.jp/hazardmap/",
                "landslide_zone": "指定あり",
                "landslide_url": "https://disaportal.gsi.go.jp/hazardmap/",
                "tsunami_zone": "内",
                "tsunami_url": "https://disaportal.gsi.go.jp/hazardmap/",
                "hazard_zone": "なし",
                "hazard_url": "https://disaportal.gsi.go.jp/hazardmap/"
            }
        else:
            hazard_info_dict = await get_all_hazard_info(lat, lon, api_key)

        hazard_info = HazardInfo(
            flood_zone=hazard_info_dict.get("flood_zone"),
            flood_depth_min=hazard_info_dict.get("flood_depth_min"),
            flood_depth_max=hazard_info_dict.get("flood_depth_max"),
            flood_url=hazard_info_dict.get("flood_url"),
            landslide_zone=hazard_info_dict.get("landslide_zone"),
            landslide_url=hazard_info_dict.get("landslide_url"),
            tsunami_zone=hazard_info_dict.get("tsunami_zone"),
            tsunami_url=hazard_info_dict.get("tsunami_url"),
            hazard_zone=hazard_info_dict.get("hazard_zone"),
            hazard_url=hazard_info_dict.get("hazard_url"),
            confirmed_at=str(date.today())
        )

        return HazardResponse(
            success=True,
            address=request.address,
            latitude=lat,
            longitude=lon,
            hazard_info=hazard_info,
            message="ハザード情報を取得しました"
        )

    except HTTPException:
        raise
    except Exception as e:
        return HazardResponse(
            success=False,
            address=request.address,
            latitude=0,
            longitude=0,
            hazard_info=HazardInfo(confirmed_at=str(date.today())),
            message=f"エラーが発生しました: {str(e)}"
        )
