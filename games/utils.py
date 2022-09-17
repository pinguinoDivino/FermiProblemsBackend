from itertools import chain

import inspect


def model_to_dict(instance, fields=None, exclude=None):
    from django.db.models.fields.related import ManyToManyField
    from django.db.models.fields import DateTimeField
    from django.db.models.fields.files import ImageField, FileField

    opts = instance._meta
    data = {}

    """
    Why is `__fields` in here?
        it holds the list of fields except for the one ends with a suffix '__[field_name]'.
        When converting a model object to a dictionary using this method,
        You can use a suffix to point to the field of ManyToManyField in the model instance.
        The suffix ends with '__[field_name]' like 'publications__name'
    """
    __fields = list(map(lambda a: a.split('__')[0], fields or []))

    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        is_editable = getattr(f, 'editable', False)

        if fields is not None and f.name not in __fields:
            continue

        if exclude and f.name in exclude:
            continue

        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                qs = f.value_from_object(instance)
                if qs._result_cache is not None:
                    data[f.name] = [item.pk for item in qs]
                else:
                    try:
                        m2m_field = list(filter(lambda a: f.name in a and a.find('__') != -1, fields))[0]
                        key = m2m_field[len(f.name) + 2:]
                        data[f.name] = list(qs.values_list(key, flat=True))
                    except IndexError:
                        data[f.name] = list(qs.values_list('pk', flat=True))

        elif isinstance(f, DateTimeField):
            date = f.value_from_object(instance)
            data[f.name] = date.strftime("%d/%m/%Y, %H:%M:%S")

        elif isinstance(f, ImageField):
            image = f.value_from_object(instance)
            data[f.name] = image.url if image else None

        elif isinstance(f, FileField):
            file = f.value_from_object(instance)
            data[f.name] = file.url if file else None

        elif is_editable:
            data[f.name] = f.value_from_object(instance)

    """
    Just call an instance's function or property from a string with the function name in `__fields` arguments.
    """
    funcs = set(__fields) - set(list(data.keys()))
    for func in funcs:
        obj = getattr(instance, func)
        if inspect.ismethod(obj):
            data[func] = obj()
        else:
            data[func] = obj
    return data
