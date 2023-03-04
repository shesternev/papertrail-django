from books.models import Category


def get_parent_categories_from_child_to_parent(obj, serializer):
    categories = []

    while obj.parent is not None:
        try:
            obj = obj.parent
            categories.append(obj)
        except AttributeError:
            continue

    Category.objects.select_related('parent').filter(id__in=[category.id for category in categories])

    serializer_data = serializer(categories, many=True).data
    return serializer_data
