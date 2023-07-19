from django.http import Http404, HttpResponseForbidden
from django.shortcuts import _get_queryset

def get_object_or_403(klass, *args, owner_fields=('author',), operator='and', **kwargs):
    queryset = _get_queryset(klass)
    user = kwargs.pop('user', None)
    if not user:
        raise ValueError("Must include 'user' keyword argument")
    try:
        obj = queryset.get(*args, **kwargs)
        if operator == 'and':
            if all(getattr(obj, field) == user for field in owner_fields):
                return obj
        elif operator == 'or':
            if any(getattr(obj, field) == user for field in owner_fields):
                return obj
        raise HttpResponseForbidden("You do not have permission to view this.")
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)

def get_list_or_403(klass, *args, owner_fields=('author',), operator='and', **kwargs):
    queryset = _get_queryset(klass)
    user = kwargs.pop('user', None)
    if not user:
        raise ValueError("Must include 'user' keyword argument")
    objects = queryset.filter(*args, **kwargs)
    if not objects:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
    if operator == 'and':
        if all(all(getattr(obj, field) == user for field in owner_fields) for obj in objects):
            return objects
    elif operator == 'or':
        if any(any(getattr(obj, field) == user for field in owner_fields) for obj in objects):
            return objects
    raise HttpResponseForbidden("You do not have permission to view this.")

