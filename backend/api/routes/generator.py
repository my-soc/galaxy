from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.controllers.generator import Generator

from api.config.schema.api import GetObjectsResponseModel, GetObjectResponseModel, ActionObjectFailedModel,\
    ObjectModel, ObjectAddModel, ObjectDeleteModel


router = APIRouter()


@router.get("/api/generator/objects", tags=["notebook"])
async def get_entries():
    return Generator.get_object()


@router.get("/api/generator/{object_id}", response_model=GetObjectResponseModel,
            responses={404: {"model": ActionObjectFailedModel}}, tags=["notebook"])
async def get_entry(object_id: str):
    response = Generator.find_object(object_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)


@router.post("/api/generator/objects", tags=["generators"])
async def post_entry(ct_object: ObjectModel):
    return Generator.post_objects(ct_object)


@router.delete("/api/generator/{object_id}", response_model=ObjectDeleteModel,
               responses={404: {"model": ActionObjectFailedModel}}, tags=["notebook"])
async def delete_entry(object_id):
    response = Generator.delete_object(object_id)
    if response.get('status') == 'success':
        return response
    else:
        return JSONResponse(status_code=404, content=response)

