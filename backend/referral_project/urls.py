from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import RetriveUser, user_login

v1_urlpatterns = [
    path("profile", RetriveUser.as_view()),
    path("login", user_login, name="login"),
]

api_urlpatterns = [
    path("v1/", include(v1_urlpatterns)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
]

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
