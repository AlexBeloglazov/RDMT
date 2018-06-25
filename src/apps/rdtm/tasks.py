import glob
from os import path
from json import dumps

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from django.conf import settings
from rdtm.models import HyperParamters


def _read_dataset():
    dataset_dir = path.join(settings.SRC_DIR, 'dataset')
    data, labels = [], []

    for class_name, class_id in HyperParamters.classes.items():
        for file_ in glob.glob(path.join(dataset_dir, class_name, '*')):
            with open(file_, 'r') as stream:
                data.append(stream.read())
                labels.append(class_id)

    return data, labels


def train_and_update_db():
    data, labels = _read_dataset()

    pipeline = Pipeline([
        ('tfidf-vect', TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
                                       encoding='utf-8', ngram_range=(1, 2),
                                       stop_words='english')),
        ('model', LogisticRegression()),
    ])

    train_data, test_data, train_label, test_label = train_test_split(
        data, labels, random_state=0, test_size=0.2)

    print(' Training dataset: %d' % len(train_data))
    print(' Testing dataset: %d' % len(test_data))

    classifier = pipeline.fit(train_data, train_label)

    prediction = classifier.predict(test_data)
    model = classifier.named_steps['model']

    parameters = dumps({
        'coef_': model.coef_.tolist(),
        'intercept_': model.intercept_.tolist(),
        'penalty': model.penalty,
        'C': model.C
    })

    HyperParamters.objects.update_or_create(id=1, defaults={
        'parameters': parameters})

    return np.mean(prediction == test_label) * 100
