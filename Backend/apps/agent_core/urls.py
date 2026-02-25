from django.urls import path

from .views import (
    agent_index,
    agent_status,
    agent_view,
)
from .views_safe import SafeAgentServiceView

urlpatterns = [
    path("", agent_index, name="agent-index"),
    path("status/", agent_status, name="agent-status"),
    path("agent/", agent_view, name="agent"),
    path("agent/safe/", SafeAgentServiceView.as_view(), name="agent-safe"),
]
