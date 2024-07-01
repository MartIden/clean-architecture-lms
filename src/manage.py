import asyncio
import sys

import fastapi

import src
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.rmq.init.run import RmqRunnerFactory
from src.presentation.fastapi.init.run import FastApiRunnerFactory


async def run_consumer() -> None:
    runner = RmqRunnerFactory.create()
    await runner.run()


def run_api() -> None:
    runner = FastApiRunnerFactory().create()
    runner.run()


async def run_all() -> None:
    run_api()
    await run_consumer()


def run_by_command(argv: list[str], runners_map: dict) -> None:
    try:
        runner_method = runners_map.get(argv[1])
    except IndexError:
        return

    if not runner_method:
        return

    if asyncio.iscoroutinefunction(runner_method):
        asyncio.run(runner_method())
    else:
        runner_method()


if __name__ == "__main__":
    container = AppContainer()
    container.wire(packages=[src, fastapi])

    run_by_command(
        argv=sys.argv,
        runners_map={
            "consumer": run_consumer,
            "api": run_api,
            "all": run_all,
        }
    )
