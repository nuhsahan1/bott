"""Health check script for all services."""
import asyncio
import httpx
from shared.config import settings
from shared.logger import get_logger

logger = get_logger(__name__)

SERVICES = {
    "Gateway": settings.GATEWAY_URL,
    "Registry": settings.REGISTRY_URL,
    "Flow Engine": settings.FLOW_ENGINE_URL,
    "Template Service": settings.TEMPLATE_SERVICE_URL,
    "Dispatcher": settings.DISPATCHER_URL,
    "Analytics": settings.ANALYTICS_URL,
    "Admin Panel": settings.ADMIN_PANEL_URL,
}


async def check_service_health(name: str, url: str) -> bool:
    """Check if a service is healthy."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{url}/")
            return response.status_code == 200
    except Exception as e:
        logger.error(f"{name} health check failed: {e}")
        return False


async def check_all_services():
    """Check health of all services."""
    logger.info("Checking service health...")
    
    results = {}
    for name, url in SERVICES.items():
        is_healthy = await check_service_health(name, url)
        status = "✓ HEALTHY" if is_healthy else "✗ DOWN"
        results[name] = is_healthy
        print(f"{name:20} {status}")
    
    healthy_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n{healthy_count}/{total_count} services healthy")
    return all(results.values())


if __name__ == "__main__":
    success = asyncio.run(check_all_services())
    exit(0 if success else 1)
