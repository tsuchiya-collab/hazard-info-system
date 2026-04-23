import os
from simple_salesforce import Salesforce
from typing import Optional, Dict, Any
from datetime import date

async def update_bukken_hazard_info(
    bukken_id: str,
    hazard_info: Dict[str, Any]
) -> bool:
    """
    Salesforceの物件レコードにハザード情報を自動入力する
    """
    try:
        # 環境変数から Salesforce 認証情報を取得
        sf_instance = os.getenv("SALESFORCE_INSTANCE")
        sf_client_id = os.getenv("SALESFORCE_CLIENT_ID")
        sf_client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
        sf_username = os.getenv("SALESFORCE_USERNAME")
        sf_password = os.getenv("SALESFORCE_PASSWORD")

        if not all([sf_instance, sf_client_id, sf_client_secret, sf_username, sf_password]):
            print("Salesforce認証情報が不完全です")
            return False

        # Salesforce 接続
        sf = Salesforce(
            instance=sf_instance.replace("https://", ""),
            client_id=sf_client_id,
            client_secret=sf_client_secret,
            username=sf_username,
            password=sf_password
        )

        # 更新するフィールド（フィールドAPI名はユーザーから確認が必要）
        update_data = {
            # "dosha_saigai_keikai_kuiki__c": hazard_info.get("landslide_zone"),
            # "dosha_saigai_url__c": hazard_info.get("landslide_url"),
            # "tsunami_keikai_kuiki__c": hazard_info.get("tsunami_zone"),
            # "tsunami_url__c": hazard_info.get("tsunami_url"),
            # "zoseitakuchi_bousai_kuiki__c": hazard_info.get("hazard_zone"),
            # "zoseitakuchi_url__c": hazard_info.get("hazard_url"),
            # "saishuu_kakuninbi__c": str(date.today()),
        }

        # フィールド名が確認されたら、上記の値をアンコメントして使用

        if not update_data:
            print("更新するフィールドが設定されていません")
            return False

        # レコード更新
        sf.bukken__c.update(bukken_id, update_data)
        print(f"Salesforce レコード更新成功: {bukken_id}")
        return True

    except Exception as e:
        print(f"Salesforce 更新エラー: {e}")
        return False
