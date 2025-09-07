from .base_handlers import router as base_router
from .crypto_handlers import router as crypto_router
from .news_handlers import router as news_router

__all__ = ['base_router', 'crypto_router', 'news_router']