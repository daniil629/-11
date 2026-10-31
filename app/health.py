from __future__ import annotations

from aiohttp import web

from . import __version__


async def health(_request: web.Request) -> web.Response:
    """Small, secret-free endpoint for platforms that expect an HTTP health check."""
    return web.json_response(
        {"status": "ok", "service": "message-keeper", "version": __version__},
        headers={"Cache-Control": "no-store"},
    )


def create_health_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    app.router.add_get("/healthz", health)
    return app


async def start_health_server(port: int) -> web.AppRunner:
    """Listen in the same process as polling; no extra worker or dependency is needed."""
    runner = web.AppRunner(create_health_app(), access_log=None)
    await runner.setup()
    try:
        site = web.TCPSite(runner, host="0.0.0.0", port=port)
        await site.start()
    except Exception:
        await runner.cleanup()
        raise
    return runner
