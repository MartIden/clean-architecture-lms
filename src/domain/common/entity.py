from src.domain.common.data_models import JsonModel
from src.domain.common.value_obj.created_at import CreatedAt
from src.domain.common.value_obj.updated_at import UpdatedAt


class Entity[IdT](JsonModel):
    id: IdT
    created_at: CreatedAt
    updated_at: UpdatedAt
