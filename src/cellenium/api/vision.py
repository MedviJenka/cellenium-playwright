from asyncio import to_thread
from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import AsyncGenerator
from cellenium.ai.agents.vision.crew import run_vision_agent
from cellenium.functions.logger import Logger
from cellenium.settings import get_config


log = Logger(name='vision-service')

Config = get_config()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    log.fire(f'{log.name} service started')
    yield
    log.fire(f'{log.name} service stopped')


router = APIRouter(prefix=f'/api/{Config.API_VERSION}/vision')


@router.post('/ai')
async def vision(prompt: str, image: UploadFile = File(...)) -> JSONResponse:
    suffix = Path(image.filename or "").suffix
    with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        image_path = Path(temp_file.name)
        temp_file.write(await image.read())

    try:
        response = await to_thread(run_vision_agent, prompt=prompt, image=[str(image_path)])
    finally:
        image_path.unlink(missing_ok=True)

    return JSONResponse({'status': f'{image} uploaded successfully', 'ai_response': response})


@router.get('/health')
async def vision() -> JSONResponse:
    return JSONResponse({'status': 'healthy'})


app = FastAPI(
    title=f"AI Vision API\nenv: {Config.APP_ENV}",
    description="Vision image with AI",
    version=Config.API_VERSION,
    lifespan=lifespan,
    docs_url=f"/api/{Config.API_VERSION}/vision/docs",
    openapi_url=f"/api/{Config.API_VERSION}/vision/openapi.json",
    redoc_url=f"/api/{Config.API_VERSION}/vision/redoc",
)


app.include_router(router=router)


@app.get('/health')
def docs() -> JSONResponse:
    return JSONResponse({'status': 'healthy'})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host='0.0.0.0', port=8888, use_colors=True)
