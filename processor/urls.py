from django.conf.urls import patterns, url
import views

urlpatterns = patterns('processor.views',
    # main page
    url(r'^$', views.home, name="home"),
    url(r'auth^$', views.auth, name="auth"),
    url(r'tasks^$', views.tasks, name="tasks"),
    url(r'traces^$', views.traces, name="traces"),
    url(r'models^$', views.models, name="models"),
    url(r'summary^$', views.summary, name="summary"),

    # actions
    url(r'^login/$', views.home, name="home"),
)
