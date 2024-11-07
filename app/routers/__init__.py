from fastapi import APIRouter

from .guest_lists import router as guest_lists_router
from .tables import router as tables_router

router = APIRouter()
router.include_router(guest_lists_router, prefix="/guest_lists", tags=["GuestList"])
router.include_router(tables_router, prefix="/tables", tags=["Tables"])
