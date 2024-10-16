from aiogram import Router

from app.handlers.start import router as start_router
from app.handlers.register import router as register_router
from app.handlers.main_menu import router as main_menu_router
from app.handlers.time_delta import router as time_delta_router


router = Router()

router.include_routers(
    start_router,
    register_router,
    main_menu_router,
)

router.include_router(time_delta_router)
