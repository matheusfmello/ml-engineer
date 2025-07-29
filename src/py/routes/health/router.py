from fastapi.routing import APIRouter

from src.py.routes.health.basemodels import HealthResponse

health_router = APIRouter()

@health_router.get('/', response_model=HealthResponse)
def get_health():
    return {"status": "ok"}
