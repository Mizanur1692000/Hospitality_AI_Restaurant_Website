from django.shortcuts import render
from django.http import Http404
from django.template import TemplateDoesNotExist


def _render_dashboard_page(request, template_name, page_title=None, extra_context=None):
    """Render a dashboard page with common context."""
    context = {
        'page_title': page_title or template_name.replace('_', ' ').title(),
        'template_name': template_name,
    }
    
    if extra_context:
        context.update(extra_context)
    
    try:
        return render(request, f"dashboard/{template_name}.html", context)
    except TemplateDoesNotExist:
        raise Http404(f"Template 'dashboard/{template_name}.html' not found")


def dashboard_view(request):
    context = {
        'dashboard_stats': {
            'total_pages': 10,
            'features': ['KPI Analysis', 'HR Solutions', 'Beverage Management', 
                        'Menu Engineering', 'Recipes', 'Strategic Planning'],
        }
    }
    return _render_dashboard_page(request, "index", "Main Dashboard", context)


def chat_view(request):
    return _render_dashboard_page(request, "chat", "Chat Assistant")


def kpi_analysis_view(request):
    return _render_dashboard_page(request, "kpi_analysis", "KPI Analysis")


def hr_solutions_view(request):
    return _render_dashboard_page(request, "hr_solutions", "HR Solutions")


def beverage_view(request):
    return _render_dashboard_page(request, "beverage", "Beverage Management")


def menu_engineering_view(request):
    return _render_dashboard_page(request, "menu_engineering", "Menu Engineering")


def recipes_view(request):
    return _render_dashboard_page(request, "recipes", "Recipe Management")


def cost_analysis_view(request):
    return _render_dashboard_page(request, "cost_analysis", "Cost Analysis")


def strategic_planning_view(request):
    return _render_dashboard_page(request, "strategic_planning", "Strategic Planning")


def kpi_dashboard_view(request):
    return _render_dashboard_page(request, "kpi_dashboard", "KPI Dashboard")


def modern_kpi_dashboard_view(request):
    return _render_dashboard_page(request, "modern_kpi_dashboard", "Modern KPI Dashboard")
