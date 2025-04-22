from django.urls import path
from .views import (
    IndexView, SingleView, ArchiveView,
    CategoryView, ElementsView, GenericsView,
    SearchView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('single/', SingleView.as_view(), name='single'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('category/', CategoryView.as_view(), name='category'),
    path('elements/', ElementsView.as_view(), name='elements'),
    path('generics/', GenericsView.as_view(), name='generics'),
    path('search/', SearchView.as_view(), name='search'),

]