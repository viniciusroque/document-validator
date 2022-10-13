import environs

_env = environs.Env()

SQLALCHEMY_DATABASE_URL: str = _env(
    "SQLALCHEMY_DATABASE_URL", "sqlite:///test.db"
)
DEBUG: bool = _env.bool("DEBUG", False)
