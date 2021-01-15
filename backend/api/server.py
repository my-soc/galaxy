from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import generator
from api.controllers.logging import log_debug, log_info, log_error

from .initialize import BackInit


ORIGINS = ["http://localhost:3000"]

services_up = BackInit.ping_services()

if services_up:
    BackInit.services_prep()
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(generator.router)
    log_info('Galaxy server is running ..')

else:
    log_error('Galaxy is not ready to start, one or more data access service is down')

