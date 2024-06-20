import asyncio
import sys

from src.infrastructure.kernel.rmq.run import RmqRunnerFactory


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
