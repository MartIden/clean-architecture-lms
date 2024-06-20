import asyncio
import sys

from src.presentation.rmq.consumers import get_consumers
from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.migrations.binding import BaseRmqBindingsMigrator
from src.infrastructure.kernel.rmq.migrations.exchanges import BaseExchangeMigrator
from src.infrastructure.kernel.rmq.migrations.queue import BaseQueueMigrator
from src.infrastructure.kernel.rmq.run import (
    RmqRunnerImpl, RmqExchangesDeclarerImpl, RmqQueuesDeclarerImpl, RmqBindingsDeclarerImpl, RmqRunnerFactory
)


async def run_consumer():
    runner = RmqRunnerFactory.create()
    await runner.run()


if __name__ == "__main__":
    run_type = sys.argv[1]

    run_types = {
        "consumer": run_consumer
    }

    coroutine = run_types.get(run_type)

    if coroutine:
        asyncio.run(coroutine())
