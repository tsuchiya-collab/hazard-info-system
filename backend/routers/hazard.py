from fastapi import APIRouter, HTTPException
from datetime import date
import os
from models.hazard import HazardRequest, HazardResponse, HazardInfo
from services.geocoding import get_coordinates
from services.hazardmap import get_all_hazard_info
from services.salesforce import update_bukken_hazard_info

router = APIRouter(prefix="/api/hazard", tags=["hazard"])

@router.post("/check", response_model=HazardResponse)
async def check_hazard(request: HazardRequest):
    """
    住所からハザード情報を取得し、オプションで Salesforce に自動入力する
    """
    try:
        # ステップ1: 住所をジオコーディング
        coords = await get_coordinates(request.address)
        if not coords:
            raise HTTPException(status_code=400, detail="住所が見つかりません")

        lat, lon = coords

        # ステップ2: ハザード情報を取得
        api_key = os.getenv("MLIT_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API キーが設定されていません")

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

        # ステップ3: Salesforce 自動入力（オプション）
        sf_updated = False
        if request.update_salesforce and request.bukken_id:
            sf_updated = await update_bukken_hazard_info(request.bukken_id, hazard_info_dict)

        return HazardResponse(
            success=True,
            address=request.address,
            latitude=lat,
            longitude=lon,
            hazard_info=hazard_info,
            salesforce_updated=sf_updated,
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
