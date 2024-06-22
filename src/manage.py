import asyncio
import sys

from src.presentation.fastapi.run import FastApiRunnerFactory
from src.presentation.rmq.run import RmqRunnerFactory


async def run_consumer() -> None:
    runner = RmqRunnerFactory.create()
    await runner.run()


def run_api() -> None:
    runner = FastApiRunnerFactory.create()
    runner.run()


def run_by_command(argv: list[str], runners: dict) -> None:
    try:
        runner_method = runners.get(argv[1])
    except IndexError:
        return

    if not runner_method:
        return
    if asyncio.iscoroutinefunction(runner_method):
        asyncio.run(runner_method())
    else:
        runner_method()


if __name__ == "__main__":
    run_by_command(
        argv=sys.argv,
        runners={
            "consumer": run_consumer,
            "api": run_api,
        }
    )
