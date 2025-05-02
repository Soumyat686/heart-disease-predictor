from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
import time

from app.schemas.api import router
from app.config import get_settings
from app.schemas.metrics import ACTIVE_REQUESTS, REQUEST_COUNT, REQUEST_LATENCY

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="API for predicting heart failure outcomes based on patient data",
        version="1.0.0",
        debug=settings.debug
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add Prometheus middleware
    app.add_middleware(
        PrometheusMiddleware,
        app_name="heart_failure_predictor",
        group_paths=True,
        prefix="heart_failure",
    )
    
    # Add metrics endpoint
    app.add_route("/metrics", handle_metrics)
    
    # Include router
    app.include_router(router, prefix="/api")
    
    # Add custom middleware for tracking request metrics
    @app.middleware("http")
    async def track_request_metrics(request: Request, call_next):
        # Increment active request counter
        ACTIVE_REQUESTS.inc()
        
        # Start timer
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise e
        finally:
            # Track request latency
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=request.method, 
                endpoint=request.url.path
            ).observe(latency)
            
            # Track request count
            REQUEST_COUNT.labels(
                method=request.method, 
                endpoint=request.url.path, 
                status=status_code
            ).inc()
            
            # Decrement active request counter
            ACTIVE_REQUESTS.dec()
            
        return response
    
    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.schemas.main:app", host="0.0.0.0", port=8000, reload=True)