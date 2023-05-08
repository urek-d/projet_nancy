from rest_framework.routers import SimpleRouter
from .user.viewsets import UserViewSet
from .auth.viewsets.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet,LogoutViewSet,ChangePasswordViewSet

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register(r'auth/logout', LogoutViewSet, basename='auth-logout')
routes.register(r'user/changepassword', ChangePasswordViewSet, basename='change-password')



# USER
routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]
