from django.conf.urls import patterns, url

from .views import MultiorgAdoptionView

urlpatterns = patterns('multiorg.views',
    url(r'^adopt/$', MultiorgAdoptionView.as_view(), name='multiorg_adopt'),
)
