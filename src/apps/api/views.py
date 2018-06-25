from os.path import join
from pickle import loads

import numpy as np
from sklearn.linear_model import LogisticRegression

from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api.mixins import JSONDecodeMixin, JSONResponseMixin
from rdtm.models import Classifier
from rdtm.tasks import _get_dataset_meta, train_and_update_db


@method_decorator(csrf_exempt, name='dispatch')
class Upload(JSONDecodeMixin, JSONResponseMixin, View):

    http_method_names = ['post']

    def post(self, *args, **kwargs):
        for class_ in Classifier.classes:
            uploaded = self._json.get(class_, [])
            if isinstance(uploaded, list):
                for fdata in uploaded:
                    fname = join(settings.DATASET_DIR, class_,
                                 get_random_string(length=32))
                    with open(fname, 'w') as f:
                        f.write(fdata)
            else:
                fname = join(settings.DATASET_DIR, class_,
                             get_random_string(length=32))
                with open(fname, 'w') as f:
                    f.write(uploaded)

        *_, accuracy = train_and_update_db()

        return self.render_to_json_success_response(**{
            'accuracy': accuracy * 100,
            'classes': _get_dataset_meta()
        })


@method_decorator(csrf_exempt, name='dispatch')
class Classify(JSONDecodeMixin, JSONResponseMixin, View):

    http_method_names = ['post']

    def post(self, *args, **kwargs):
        classes = {meta[1]: name for name, meta in Classifier.classes.items()}
        classifier = loads(Classifier.objects.first().classifier)

        result = []

        items = self._json.get('files', [])
        if not isinstance(items, list):
            return self.render_to_json_error_response('List expected')

        for item in items:
            if not isinstance(item, dict):
                return self.render_to_json_error_response(message='Bad item')
            fname = item['name']
            fdata = item['text']

            prediction = [
                {'class': classes[id_], 'confidence': confidence}
                for id_, confidence in enumerate(
                    classifier.predict_proba([fdata]).tolist()[0]
                )
            ]

            result.append({
                'name': fname,
                'prediction': prediction
            })

        return self.render_to_json_success_response(result=result)
