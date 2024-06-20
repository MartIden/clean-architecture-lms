from pydantic import BaseModel


class PostgresSettings(BaseModel):
    engine: str = "postgresql"
    user: str = "postgres"
    password: str = "mysecretpassword"
    db: str = "postgres"
    host: str = "127.0.0.1"
    port: str = "5432"
    db_schema: str = "public"
