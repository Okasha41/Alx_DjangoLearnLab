from rest_framework.routers import DefaultRouter
from .views import UserViewSet


# login/ // register/
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = router.urls
