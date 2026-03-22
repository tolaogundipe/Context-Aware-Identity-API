from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,)


urlpatterns = [
    # admin routes that provides access to django admin panel
    path("admin/", admin.site.urls),

    # authentication (jwt) that handles login and token refresh for api access
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # identity api routes that handles identity resolution and profile updates
    path("api/identities/", include("apps.identities.urls")),

    # api documentation (openapi schema) generates schema for api endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),


    # swagger ui that provides interactive api documentation
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),


    # context api routes handles retrieval of available contexts
    path("api/contexts/", include("apps.contexts.urls")),

    # user api routes handles user listing and current user details
    path("api/users/", include("apps.users.urls")),


    # audit api routes handles audit log retrieval
    path("api/audit/", include("apps.audit.urls")),

]