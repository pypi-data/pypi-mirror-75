from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcViewMixin, NavbarViewMixin, TemplateView):
    template_name = f"{settings.APP_NAME}/bootstrap{settings.EDC_BOOTSTRAP}/home.html"
    navbar_name = "inte_edc"
    navbar_selected_item = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
