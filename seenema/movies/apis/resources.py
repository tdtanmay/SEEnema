from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django.contrib.auth import login
from movies.models import Movie, UserProfile
from .serializers import MovieSerializer, RegisterUserSerializer, LoginUserSerializer, UserProfileSerializer


class MoviesListCreateAPIView(generics.ListCreateAPIView):
    """
    **Use Cases**

    **Allowed Methods**

    **Example Requests**
        POST:
            url: ""
            On Success:
            On Failure:

    **API Usage**
    """
    queryset = Movie.objects.all()
    # permission_classes =
    # authentication_classes =
    pagination_class = PageNumberPagination
    permission_classes = []
    search_fields = ['name', ]
    # ordering_fields = ['release_date', 'upvotes', 'downvotes']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = MovieSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """
    **Use Cases**

    **Allowed Methods**

    **Example Requests**
        POST:
            url: ""
            On Success:
            On Failure:

    **API Usage**


    """

    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        return super(UserRegisterAPIView, self).dispatch(request, *args, **kwargs)


class UserLoginView(APIView):
    """
    **Use Cases**

    **Allowed Methods**

    **Example Requests**
        POST:
            url: ""
            On Success:
            On Failure:

    **API Usage**
    """

    http_method_names = ["post"]
    serializer_class = LoginUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # import ipdb;ipdb.set_trace()
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            login(request, user)
            return Response({"username": user.username}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class MoviesModelViewset(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []
    search_fields = ['genre__id',]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    def get_permissions(self):
        # import ipdb;ipdb.set_trace()
        if self.request.method == "GET" and 'genre__id' not in self.request.query_params:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super(MoviesModelViewset, self).get_permissions()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # import ipdb;ipdb.set_trace()
        if partial and 'upvotes' in request.data.keys():
                upvotes = instance.upvotes+1
                request._full_data = {'upvotes': upvotes}
                serializer = self.get_serializer(instance, data=request._full_data, partial=partial)
        elif partial and 'downvotes' in request.data.keys():
                downvotes = instance.downvotes-1
                request._full_data = {'downvotes': downvotes}
                serializer = self.get_serializer(instance, data=request._full_data, partial=partial)
        else:
            serializer = self.get_serializer(instance, data=request._full_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class UserProfileUpdateAPIView(generics.UpdateAPIView):
    """
    **Use Cases**

    **Allowed Methods**

    **Example Requests**
        POST:
            url: ""
            On Success:
            On Failure:

    **API Usage**
    """
    queryset = UserProfile.objects.all()
    lookup_field = "id"
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        if not hasattr('User', 'profile'):
            raise ObjectDoesNotExist('requesting User has no UserProfile object associated.')
        if not request.user.profile == obj:
            raise PermissionDenied('Requested resource does not being to the authenticated User ')
        return super(UserProfileUpdateAPIView, self).check_object_permissions(request, obj)

