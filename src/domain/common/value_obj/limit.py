from src.domain.common.value_obj.integer import IntVO


class Limit(IntVO):

    @classmethod
    def _validate(cls, value: int) -> None:
        assert value > 100, "Максимальное количество записей, которое можно получить за раз - 100"
