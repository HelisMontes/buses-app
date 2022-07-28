from django.db.models.functions import Lower

from app.helpers.validate_datetime import validate_datetime


def filter_and_sort(
    sort_by: str,
    sort_type: str,
    filter_by: str = None,
    filter_value: str = None,
    data_list: list = None,
    model: object = None,
) -> dict:
    """
    Filtrado y ordenamiento de una lista de objetos.
    """

    TYPES_FILTERS = {
        'IntegerField': lambda query: query.filter(**{filter_by: filter_value}),
        'BigIntegerField': lambda query: query.filter(**{filter_by: filter_value}),
        'BigAutoField': lambda query: query.filter(**{filter_by: filter_value}),

        'CharField': lambda query: query.extra(
            where=[''+filter_by+' LIKE %s'],
            params=['%'+filter_value+'%']
        ),

        'BooleanField': lambda query: query.filter(**{filter_by: filter_value}),

        'DateTimeField': lambda query: query.filter(**{filter_by: validate_datetime(filter_value)}),

        'default': lambda query: query.filter(**{filter_by: filter_value}),
    }

    TYPES_SORT = {
        'CharField': lambda query: query.order_by(Lower(sort_by).asc()) if sort_type == 'asc' else query.order_by(Lower(sort_by).desc()),
        'default': lambda query: query.order_by(sort_by) if sort_type == 'asc' else query.order_by('-'+sort_by),
    }

    fields_types = {}
    fields = model._meta.fields
    for field in fields:
        fields_types[field.name] = field.get_internal_type()

    if filter_by and filter_by in fields_types:
        data_list = TYPES_FILTERS.get(fields_types[filter_by], TYPES_FILTERS['default'])(data_list)

    data_list = data_list.all()

    if sort_by and sort_by in fields_types:
        data_list = TYPES_SORT.get(fields_types[sort_by], TYPES_SORT['default'])(data_list)

    return data_list
