from django.shortcuts import render
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = 'index.html'


class SingleView(TemplateView):
    template_name = 'single.html'


class ArchiveView(TemplateView):
    template_name = 'archive.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


class ElementsView(TemplateView):
    template_name = 'elements.html'


class GenericsView(TemplateView):
    template_name = 'generic.html'


class SearchView(TemplateView):
    template_name = 'search.html'

