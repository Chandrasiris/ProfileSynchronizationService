from sqlalchemy import create_engine
from profile_sync.config import Settings

def build_engine(settings: Settings):
    if not settings.DATABASE_URL: raise RuntimeError('DATABASE_URL required')
    url=settings.DATABASE_URL.get_secret_value()
    if not url.startswith('postgresql+psycopg://'): raise ValueError('Explicit psycopg URL required')
    return create_engine(url, pool_pre_ping=True, hide_parameters=True, pool_size=5, max_overflow=2)
