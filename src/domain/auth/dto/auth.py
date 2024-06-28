from src.domain.common.data_models import JsonModel


class JwtInResponse(JsonModel):
    token:      str
    token_type: str
