from django.views.generic.base import TemplateView
from .clients import EloquaLandingPagesClient


class LandingPageView(TemplateView):
    template_name = "eloqua/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)

        # TODO: add try/catch if page not found?
        e = EloquaLandingPagesClient()
        landing_page = e.get(kwargs['pk'])

        context['landing_page'] = landing_page

        return context
