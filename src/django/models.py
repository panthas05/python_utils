from django.db import models


def get_model_fields(
    model: type[models.Model],
) -> list[str]:
    """
    Returns a list of all fields on the model.
    """
    return [f.name for f in model._meta.get_fields()]
