
from django.conf.urls import patterns, url
from solr import views

# url: <a href="{% url 'category'  c.slug %}">{{ c.name }}</a></li>   url name, and paramter to category
urlpatterns = patterns('',
        url(r'^$', views.index, name='main_page'),
        url(r'^about/$', views.about, name = 'about'),
        url(r'^search/$', views.search, name = 'search'),
        url(r'^detail/(?P<md5>.+)/$', views.detail, name = 'detail'),
        url(r'^jumppage/(?P<page_info>.+)/$', views.jumppage, name = 'jumppage'),
        )