from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from logging import Logger
from typing import Any


class StatusEnum(str, Enum):
    OK = "OK"
    FAIL = "FAIL"


class IStep(ABC):

    @abstractmethod
    async def __call__(self) -> Any: ...

    @abstractmethod
    async def compensation(self, result: Any) -> Any: ...


@dataclass
class StepResult:
    step: IStep
    result: Any


@dataclass
class SagaResult:
    status: StatusEnum = StatusEnum.OK
    step_results: list[StepResult] = field(default_factory=list)
    compensation_results: list[StepResult] = field(default_factory=list)


class ISagaOrchestrator(ABC):
    @abstractmethod
    async def run_step(self, step: IStep) -> Any: ...

    @abstractmethod
    async def _compensation(self) -> None: ...

    @abstractmethod
    def get_result(self) -> SagaResult: ...


class SagaOrchestrator(ISagaOrchestrator):

    def __init__(self, logger: Logger, retry_count=5):
        self.__steps_results: list[StepResult] = []
        self.__compensation_results: list[StepResult] = []
        self.__logger = logger
        self.__result = SagaResult()
        self.__retry_count = retry_count

    @property
    def __step_result(self):
        return self.__steps_results

    @__step_result.setter
    def __step_result(self, v: StepResult) -> None:
        self.__steps_results.append(v)
        self.__result.step_results = self.__steps_results

    @property
    def __compensation_result(self):
        return self.__compensation_results

    @__compensation_result.setter
    def __compensation_result(self, v: StepResult) -> None:
        self.__compensation_results.append(v)
        self.__result.compensation_results = self.__compensation_results

    async def run_step(self, step: IStep) -> Any:
        try:
            result = await step()
            self.__step_result = StepResult(step=step, result=result)
            return result
        except Exception as err:
            msg = f"Cannot commit step '{step.__class__.__name__}' with error '{str(err)}'"
            self.__logger.error(msg)
            await self._compensation()
            self.__step_result = StepResult(step=step, result=err)
            self.__result.status = StatusEnum.FAIL
            raise

    async def _compensation(self) -> None:
        for step_result in reversed(self.__steps_results):
            try:
                result = await step_result.step.compensation(step_result.result)
                self.__compensation_result = StepResult(step=step_result.step, result=result)
            except Exception as err:
                msg = f"Cannot compensate step '{step_result.step.__class__.__name__}' with error '{str(err)}'"
                self.__logger.error(msg)
                self.__compensation_result = StepResult(step=step_result.step, result=err)

    def get_result(self) -> SagaResult:
        return self.__result
