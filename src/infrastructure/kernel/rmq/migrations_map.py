from src.infrastructure.kernel.settings.unit.rmq_migration import RmqMigrationSettings

__MIGRATIONS_MAP = {
    "queues": [
        {"name": "q.user.update", "kwargs": {}},
        {"name": "q.user.new", "kwargs": {}},
    ],
    "bindings": [
        {"queue": "q.user.update", "exchange": "x.user.update", "kwargs": {}},
        {"queue": "q.user.new", "exchange": "x.user.new", "kwargs": {}},
    ],
    "exchanges": [
        {"name": "x.user.update", "exchange_type": "fanout", "kwargs": {}},
        {"name": "x.user.new", "exchange_type": "fanout", "kwargs": {}},
    ],
}


def get_migration_settings() -> RmqMigrationSettings:
    return RmqMigrationSettings(**__MIGRATIONS_MAP)
