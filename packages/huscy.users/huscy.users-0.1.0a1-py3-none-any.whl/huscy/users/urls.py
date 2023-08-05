from rest_framework.routers import DefaultRouter

from huscy.users import views


router = DefaultRouter()
router.register('userprofiles', views.UserProfileViewSet, basename='userprofile')
router.register('users', views.UserViewSet)
