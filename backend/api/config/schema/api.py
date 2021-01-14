from pydantic import BaseModel
from typing import List, Optional

# /** Root Schema **\
# ####################### #


class VersionResponse(BaseModel):
    Version: str


class VersionResponseModel(BaseModel):
    status: str
    payload: VersionResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "Version": "1.0"
                }
            }
        }


# /** Generator Schema **\
# ####################### #

# / Models Dictionaries\

class Entry(BaseModel):
    id: str
    content: str


class EntriesResponse(BaseModel):
    data: List[Entry]


class EntryResponse(BaseModel):
    data: Entry


class EntryFailedResponse(BaseModel):
    message: str


class ActionEntryResponse (BaseModel):
    index: str
    id: str
    result: str


# / Requests and Response Models\

class GetObjectsResponseModel (BaseModel):
    status: str
    payload: Optional[EntriesResponse]

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "data": [
                        {
                            "id": "1607753673554",
                            "content": "Entry1"
                        }
                    ],
                    "total": 1
                }
            }
        }


class GetObjectResponseModel (BaseModel):
    status: str
    payload: EntryResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "data": {
                        "id": "1607753673554",
                        "content": "Entry1"
                    }
                }
            }
        }


class ActionObjectFailedModel(BaseModel):
    status: str
    payload: EntryFailedResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (E:2) Entry not found .."
                }
            }
        }


class ObjectDeleteModel (BaseModel):
    status: str
    payload: ActionEntryResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "index": "notebook",
                    "id": "1608223604241",
                    "result": "deleted"
                }
            }
        }


class ObjectAddModel (BaseModel):
    status: str
    payload: ActionEntryResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "index": "notebook",
                    "id": "1607753673554",
                    "result": "created"
                }
            }
        }


class ObjectModel(BaseModel):
    content: str

    class Config:
        schema_extra={
            "example": {
                "content": "Entry1"
            }
        }


# /** Settings Schema **\
# ####################### #

# / Models Dictionaries\


class PingResponse(BaseModel):
    elasticsearch: Optional[bool] = None
    minio: Optional[bool] = None
    redis: Optional[bool] = None
    rabbitmq: Optional[bool] = None
    docker: Optional[bool] = None


class PingFailedResponse(BaseModel):
    message: str

# / Requests and Response Models\


class PingResponseModel(BaseModel):
    status: str
    payload: PingResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "elasticsearch": True,
                    "minio": True,
                    "redis": True
                }
            }
        }


class PingFailedModel(BaseModel):
    status: str
    payload: PingFailedResponse

    class Config:

        schema_extra = {
            "example": {
                "status": "fail",
                "payload": {
                    "message": "Error (W:01) Service not found .."
                }
            }
        }

