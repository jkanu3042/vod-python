from django import forms
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse, reverse_lazy

from .models import Post


post_list = ListView.as_view(model=Post, paginate_by=3)
post_detail = DetailView.as_view(model=Post)

# success_url이 기입되지 않으면, Post Model에 정의된 get_absolute_url()이 자동으로 호출된다.
post_new = CreateView.as_view(model=Post)
post_edit = UpdateView.as_view(model=Post, fields='__all__')
post_delete = DeleteView.as_view(model=Post, success_url=reverse_lazy('blog:post_list'))