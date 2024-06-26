from src.domain.user.dto.user import Order


def get_order(order: str) -> Order:
    return Order.desc if order.lower() == "desc" else Order.asc
