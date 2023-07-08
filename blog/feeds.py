from typing import Any
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from . models import Post

class LatestPostsFeed(Feed):
    title = 'Medium-R'
    link = reverse_lazy('blog:post_list')
    description = 'New posts from the Medium-R'

    def items(self):
        return Post.published.all() [:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item) -> str:
        return truncatewords(item.body, 30)