from aiogram import Dispatcher
from .common import router as common_router


async def register_all_handlers(dp: Dispatcher):
    routers = (
        common_router,
    )
    for router in routers:
        dp.include_router(router)