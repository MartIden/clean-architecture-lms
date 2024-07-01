from typing import Optional

from src.presentation.rmq.init.publisher import AbstractRmqPublisher


class UserNewPublisher(AbstractRmqPublisher):
    @property
    def _exchange_name(self) -> Optional[str]:
        return "x.user.new"
