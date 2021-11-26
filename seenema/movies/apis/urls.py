from django.urls import path, re_path
from movies.apis.resources import MoviesListCreateAPIView, UserRegisterAPIView, UserLoginView, UserProfileUpdateAPIView

urlpatterns = [
    path('movies/', MoviesListCreateAPIView.as_view(), name=''),
    path('user/registration/', UserRegisterAPIView.as_view(), name='register'),
    path('user/login/', UserLoginView.as_view(), name='login'),  # http://127.0.0.1:8000/apis/user/login/
    re_path(r'^update/user-profile/(?P<id>[0-9]+)/$', UserProfileUpdateAPIView.as_view(), name=""),

]