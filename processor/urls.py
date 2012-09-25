from django.conf.urls import patterns, url
import views

urlpatterns = patterns('processor.views',
    # main page
    url(r'^$', views.home, name="home"),

    # actions
    url(r'^login/$', views.home, name="home"),
)
