from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    schema: str = "public"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.getenv("ANALYTICS_DB_HOST", "localhost"),
            port=int(os.getenv("ANALYTICS_DB_PORT", "5432")),
            database=os.getenv("ANALYTICS_DB_NAME", "sellix_db"),
            username=os.getenv("ANALYTICS_DB_USER", "store_user"),
            password=os.getenv("ANALYTICS_DB_PASSWORD", "sellix_2024"),
            schema=os.getenv("ANALYTICS_DB_SCHEMA", "public"),
        )

    def sqlalchemy_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
