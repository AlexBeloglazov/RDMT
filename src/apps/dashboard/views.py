from django.views.generic import TemplateView

from dashboard.models import UnresolvedDocument
from rdmt.models import Classifier
from rdmt.tasks import _get_dataset_meta


class StatsView(TemplateView):
    """
    View serves the page with stats
    """

    template_name = 'dashboard/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        classifier = Classifier.objects.first()

        context.update({
            'stats': {
                'accuracy': classifier.accuracy,
                'dataset': _get_dataset_meta()
            }
        })


class IndexView(TemplateView):
    """
    View serves the page to upload documents to classify
    """

    template_name = 'dashboard/index.html'


class ResolveView(TemplateView):
    """
    View shows resolution page
    """

    http_method_names = ['get']
    template_name = 'dashboard/resolve.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'document': UnresolvedDocument.objects.get(id=self.kwargs['id'])
        })
        return context
