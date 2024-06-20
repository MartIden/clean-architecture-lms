import asyncio
import sys

from src.presentation.rmq.run import RmqRunnerFactory


async def run_consumer():
    runner = RmqRunnerFactory.create()
    await runner.run()


def run_by_command(argv: list[str], runners: dict) -> None:
    if not argv:
        return

    coroutine = runners.get(argv[1])

    if coroutine:
        asyncio.run(coroutine())


if __name__ == "__main__":
    run_by_command(
        argv=sys.argv,
        runners={
            "consumer": run_consumer
        }
    )


