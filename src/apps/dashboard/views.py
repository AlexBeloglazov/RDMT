from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    View serves main dashboard page
    """

    template_name = 'dashboard/index.html'


class TrainView(TemplateView):
    """
    View serves the page to upload training documents
    """

    template_name = 'dashboard/train.html'


class ClassifyView(TemplateView):
    """
    View serves the page to upload documents to classify
    """

    template_name = 'dashboard/classify.html'
