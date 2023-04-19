from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Filter of Title model."""
    genre = filters.CharFilter(field_name="genre__slug",)
    category = filters.CharFilter(field_name="category__slug",)

    class Meta:
        model = Title
        fields = ('year', 'name', 'genre', 'category')
