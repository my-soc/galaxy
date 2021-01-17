from fastapi import APIRouter
from fastapi.responses import JSONResponse

from controllers.exchange import Exchange

from config.schema.api import GetObjectsResponseModel, GetObjectResponseModel, ActionObjectFailedModel,\
    ObjectModel, ObjectDeleteModel


router = APIRouter()


@router.get("/api/exchange/objects",  response_model=GetObjectsResponseModel, tags=["exchange"])
async def get_objects():
    return Exchange.get_object()


@router.get("/api/exchange/{object_id}", response_model=GetObjectResponseModel,
            responses={404: {"model": ActionObjectFailedModel}}, tags=["exchange"])
async def get_object(object_id: str):
    response = Exchange.find_object(object_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.post("/api/exchange/objects", tags=["exchange"])
async def post_entry(ct_object: ObjectModel):
    return Exchange.post_objects(ct_object)


@router.delete("/api/exchange/{object_id}", response_model=ObjectDeleteModel,
               responses={404: {"model": ActionObjectFailedModel}}, tags=["exchange"])
async def delete_entry(object_id):
    response = Exchange.delete_object(object_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)

