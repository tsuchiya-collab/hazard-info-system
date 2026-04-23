from pydantic import BaseModel
from typing import Optional

class HazardRequest(BaseModel):
    address: str

class CoordinatesResponse(BaseModel):
    latitude: float
    longitude: float
    address: str

class HazardInfo(BaseModel):
    flood_zone: Optional[str] = None
    flood_depth_min: Optional[float] = None
    flood_depth_max: Optional[float] = None
    flood_url: Optional[str] = None

    landslide_zone: Optional[str] = None
    landslide_url: Optional[str] = None

    tsunami_zone: Optional[str] = None
    tsunami_url: Optional[str] = None

    hazard_zone: Optional[str] = None
    hazard_url: Optional[str] = None

    confirmed_at: str

class HazardResponse(BaseModel):
    success: bool
    address: str
    latitude: float
    longitude: float
    hazard_info: HazardInfo
    message: Optional[str] = None
