from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = "CCTV OS"
admin.site.site_title = "CCTV OS"
admin.site.index_title = "CCTV Business Dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", obtain_auth_token, name="api_login"),
    path("api/clients/", include("clients.urls")),
    path("api/quotes/", include("quotes.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/invoices/", include("invoices.urls")),
    path("api/maintenance/", include("maintenance.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
