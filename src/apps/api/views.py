from random import choice

from os.path import join
from pickle import loads

from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.urls import reverse

from api.mixins import JSONDecodeMixin, JSONResponseMixin
from dashboard.models import UnresolvedDocument
from rdmt.models import Classifier
from rdmt.tasks import _get_dataset_meta, train_and_update_db


class Stats(JSONResponseMixin, View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return self.render_to_json_success_response(**{
            'accuracy': Classifier.objects.first().accuracy,
            'dataset': _get_dataset_meta()
        })


@method_decorator(csrf_exempt, name='dispatch')
class Classify(JSONDecodeMixin, JSONResponseMixin, View):

    http_method_names = ['post']

    pocs = [
        'John Doe <xyz@email.com>',
        'Jane Doe <zyx@email.com>'
    ]

    def post(self, *args, **kwargs):

        regions = {meta[1]: name for name, meta in Classifier.regions.items()}
        lobs = {meta[1]: name for name, meta in Classifier.lobs.items()}
        categories = {meta[1]: name for name, meta in Classifier.categories.items()}

        classifiers = Classifier.objects.first()

        region_classifier = loads(classifiers.region)
        lob_classifier = loads(classifiers.lob)
        cat_classifier = loads(classifiers.category)

        result = []

        items = self._json.get('files', [])
        if not isinstance(items, list):
            return self.render_to_json_error_response('List expected')

        for item in items:
            if not isinstance(item, dict):
                return self.render_to_json_error_response(message='Bad item')
            fname = item['name']
            fdata = item['text']

            prediction = {
                'region': [
                    {'name': regions[id_], 'confidence': confidence}
                    for id_, confidence in enumerate(
                        region_classifier.predict_proba([fdata]).tolist()[0]
                    )
                ],
                'lob': [
                    {'name': lobs[id_], 'confidence': confidence}
                    for id_, confidence in enumerate(
                        lob_classifier.predict_proba([fdata]).tolist()[0]
                    )
                ],
                'category': [
                    {'name': categories[id_], 'confidence': confidence}
                    for id_, confidence in enumerate(
                        cat_classifier.predict_proba([fdata]).tolist()[0]
                    )
                ],
            }

            document = UnresolvedDocument.objects.create(
                name=fname,
                content=fdata,
                region=max(prediction['region'],
                           key=lambda x: x['confidence'])['name'],
                lob=max(prediction['lob'],
                        key=lambda x: x['confidence'])['name'],
                category=max(prediction['category'],
                             key=lambda x: x['confidence'])['name']
            )

            result.append({
                'id': document.id,
                'resolve_url': reverse('dashboard_resolve', args=[document.id]),
                'name': fname,
                'poc': choice(self.pocs),
                'prediction': prediction
            })

        return self.render_to_json_success_response(result=result)


@method_decorator(csrf_exempt, name='dispatch')
class Resolve(JSONDecodeMixin, JSONResponseMixin, View):

    http_method_names = ['post']

    def post(self, *args, **kwargs):
        resolved_id = self._json['id']
        document = UnresolvedDocument.objects.get(id=resolved_id)

        fname = join(settings.DATASET_DIR, document.region, document.lob,
                     document.category, get_random_string(length=32))

        with open(fname, 'w') as f:
            f.write(document.content)

        accuracy = Classifier.objects.first().accuracy
        # *_, accuracy = train_and_update_db()

        document.delete()

        return self.render_to_json_success_response(**{
            'accuracy': accuracy * 100,
            'dataset': _get_dataset_meta()
        })
