from django.db.models import Q, Count
from django.utils.timezone import now
from datetime import timedelta

class FilterManager:
    def __init__(self, queryset, search=None, filter_option=None, category_option=None, tag_option=None):
        self.queryset = queryset
        self.search = search
        self.filter_option = filter_option
        self.category_option = category_option
        self.tag_option = tag_option

    def all_filters(self):
        # Qidiruv buyicha filter
        if self.search:
            self.queryset = self.queryset.filter(
                Q(title__icontains=self.search) | Q(content__icontains=self.search)
            ).distinct()

        # Kategoriya buyicha filter
        if self.category_option:
            self.queryset = self.queryset.filter(category__slug=self.category_option)

        # Teg buyicha filter
        if self.tag_option:
            self.queryset = self.queryset.filter(tags__name__icontains=self.tag_option).distinct()

        # Qo‘shimcha filterlar
        if self.filter_option == 'yangilar':
            self.queryset = self.queryset.order_by('-created_at')
        elif self.filter_option == 'top':
            self.queryset = self.queryset.order_by('-views')
        elif self.filter_option == 'yonmoqda':
            self.queryset = self.queryset.filter(views__gte=100).order_by('-views')
        elif self.filter_option == 'emoji':
            self.queryset = self.queryset.annotate(
                emoji_count=Count('reactions__emoji')
            ).filter(emoji_count__gt=0).order_by('-emoji_count')
        elif self.filter_option == 'hafta':
            one_week_ago = now() - timedelta(days=7)
            self.queryset = self.queryset.filter(created_at__gte=one_week_ago)
        elif self.filter_option == 'oy':
            one_month_ago = now() - timedelta(days=30)
            self.queryset = self.queryset.filter(created_at__gte=one_month_ago)
        elif self.filter_option == 'hammasi' or self.filter_option is None:
            pass

        return self.queryset
