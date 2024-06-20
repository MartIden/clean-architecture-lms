import asyncio

from src.infrastructure.kernel.rmq.migrations_map import get_migration_settings


async def get_connect() -> None:
    # from src import infrastructure, presentation
    from src.infrastructure.kernel.ioc.container.infrastructure import InfrastructureContainer

    container = InfrastructureContainer()
    # container.wire(packages=[infrastructure, presentation])
    connector = container.postgres_connector()

    get_migration_settings()


if __name__ == "__main__":
    asyncio.run(get_connect())
