from bson import ObjectId
from fastapi import HTTPException

from doc_storage_service.config import settings
from doc_storage_service.database import save_file_to_gridfs, save_file_metadata, get_file_from_gridfs
from doc_storage_service.elastic_conf import es_client


async def upload_file(user_id: int, file_name: str, file_data: str):
    file_data = file_data.encode('latin-1')

    file_id = await save_file_to_gridfs(file_data, file_name)
    file_id = str(file_id)

    try:
        es_client.index(index=settings.ELASTIC_INDEX, document={"user_id": user_id, "file_name": file_name, "file_id": file_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    print(f"File saved with GridFS ID: {file_id} for user {user_id}")


async def download_file(user_id: int, file_name: str):
    try:
        res = es_client.search(index=settings.ELASTIC_INDEX, body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"user_id": user_id}},
                        {"match": {"file_name": file_name}}
                    ]
                }
            }
        })

        if res['hits']['total']['value'] > 0:
            res = res['hits']['hits'][0]
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return await get_file_from_gridfs(ObjectId(res["_source"]["file_id"]))
