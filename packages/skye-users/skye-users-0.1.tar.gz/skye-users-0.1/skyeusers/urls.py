from .views import UserViewSet, RoleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skyeusers', UserViewSet, basename='skyeuser')
router.register(r'skyeusers-roles', RoleViewSet, basename='skyeusers-role')
urlpatterns = router.urls
