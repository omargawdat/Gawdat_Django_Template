import rules
from django.db import models

from apps.users.models.customer import Customer


@rules.predicate
def is_object_owner(user, obj, max_depth=5):
    user_types_map = {
        Customer: "customer",
    }

    user_type = next(
        (user_type for user_type in user_types_map if isinstance(user, user_type)), None
    )
    if not user_type:
        return False

    user_field = user_types_map[user_type]

    return check_relation(obj, user, user_field, max_depth)


def check_relation(obj, user, user_field, max_depth, depth=0):
    if depth > max_depth:
        return False

    if check_direct_relation(obj, user, user_field):
        return True

    if check_foreign_key_relations(obj, user, user_field, max_depth, depth):
        return True

    if check_reverse_relations(obj, user, user_field, max_depth, depth):
        return True
    return False


def check_direct_relation(obj, user, user_field):
    try:
        return getattr(obj, user_field) == user
    except AttributeError:
        return False


def check_foreign_key_relations(obj, user, user_field, max_depth, depth):
    for field in obj._meta.fields:
        if isinstance(field, models.ForeignKey):
            try:
                related_obj = getattr(obj, field.name)
                if related_obj is not None and check_relation(
                    related_obj, user, user_field, max_depth, depth + 1
                ):
                    return True
            except AttributeError:
                continue
    return False


def check_reverse_relations(obj, user, user_field, max_depth, depth):
    for field in obj._meta.related_objects:
        related_name = field.get_accessor_name()
        try:
            related_queryset = getattr(obj, related_name).all()
            if any(
                check_relation(related_obj, user, user_field, max_depth, depth + 1)
                for related_obj in related_queryset[:5]
            ):
                return True
        except AttributeError:
            continue
    return False


rules.add_perm("myapp.view_mymodel", is_object_owner)
rules.add_perm("myapp.change_mymodel", is_object_owner)
