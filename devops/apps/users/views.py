from rest_framework import viewsets
# from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend #搜索
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
User = get_user_model()

from .serializers import UserSerializer
from .filters import UserFilter
# from .pagination import Pagination



class UserViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:返回指定用户信息
    list:返回用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PageNumberPagination
    # pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter
    filter_fields = ("username",) #搜索的字段
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (AllowAny,)



