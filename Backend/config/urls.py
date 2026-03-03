from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.agent_core.urls")),
    path("api/kpi/", include("apps.kpi_api.urls")),
    path("api/hr/", include("apps.hr_api.urls")),
    path("api/beverage/", include("apps.beverage_api.urls")),
    path("api/menu/", include("apps.menu_api.urls")),
    path("api/recipe/", include("apps.recipe_api.urls")),
    path("api/strategic/", include("apps.strategic_api.urls")),
    path("chat/", include("apps.chat_assistant.urls")),
    # path("dashboard/", include("apps.dashboard.urls")),
    # path("", include("apps.dashboard.urls")),
]
