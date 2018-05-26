from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from .models import Post


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        path = request.POST.get('path', '')
        text = request.POST.get('text', '')

        post = get_object_or_404(Post, pk=pk)
        post.comments.add_comment(path, request.user, text)

        return HttpResponseRedirect(reverse('post', kwargs={'pk': pk}))
