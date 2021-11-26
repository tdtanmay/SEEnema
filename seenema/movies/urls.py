from django.conf.urls import url, include
from django.urls import path
from movies import views







urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),  # Notice the URL has been named
    path('apis/', include('movies.apis.urls'))
    # url(, include('movies.apis.urls')),  # tell django to read urls.py in movies app

]