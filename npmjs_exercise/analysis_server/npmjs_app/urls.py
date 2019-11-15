from django.urls import re_path
from npmjs_app.views import dependency_tree_view

urlpatterns = [
    re_path(r'package/(?P<name>[a-zA-Z0-9\-]*)/dependencies/?$', dependency_tree_view, name='dependency-tree'),
]
