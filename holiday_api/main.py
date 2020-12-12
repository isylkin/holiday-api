import time
from ipaddress import ip_address
from typing import Callable

from fastapi import Depends, FastAPI, Request, Response
from starlette_prometheus import PrometheusMiddleware, metrics

from holiday_api import auth, database, stats
from holiday_api.routers import holidays, users

app = FastAPI(
    title='Holiday API',
    description='Easy access to holiday data',
    redoc_url=None,
)

app.include_router(
    users.ROUTER,
    prefix='/users',
    tags=['Users'],
    dependencies=[Depends(auth.authenticate)],
)

app.include_router(
    holidays.ROUTER,
    prefix='/holidays',
    tags=['Holidays'],
)

app.add_middleware(PrometheusMiddleware)  # TODO prometheus server


@app.api_route(
    path='/metrics',
    dependencies=[Depends(auth.authenticate)],
    include_in_schema=False,
)
async def show_metrics(request: Request) -> Response:
    return metrics(request)  # type: ignore


@app.middleware('http')
async def update_unique_users_stats(
    request: Request,
    call_next: Callable,
) -> Response:
    try:
        session = database.SessionLocal()
        unique_users = stats.UniqueUsers(session)
        unique_users.update(ip_address(request.client.host))
        response = await call_next(request)
    finally:
        session.close()  # pylint: disable=no-member
    return response  # type: ignore


@app.middleware('http')
async def add_process_time_header(
        request: Request, call_next: Callable,) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers['Server-Timing'] = f'total;dur={process_time}'
    return response  # type: ignore
