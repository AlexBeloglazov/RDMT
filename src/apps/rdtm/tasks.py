import glob
from os import path
from pickle import dumps

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from django.conf import settings
from rdtm.models import Classifier


def _get_dataset_meta():
    dataset_dir = settings.DATASET_DIR
    info = []

    for class_name, class_meta in Classifier.classes.items():
        info.append({
            'name': class_name,
            'size': len(glob.glob(path.join(dataset_dir, class_name, '*'))),
            'description': class_meta[0]
        })

    return info


def _get_dataset():
    dataset_dir = settings.DATASET_DIR
    data, labels, class_names = [], [], []

    for class_name, class_meta in Classifier.classes.items():
        for file_ in glob.glob(path.join(dataset_dir, class_name, '*')):
            with open(file_, 'r') as stream:
                data.append(stream.read())
            labels.append(class_meta[1])
            class_names.append(class_name)

    return data, labels


def train_and_update_db():
    data, labels = _get_dataset()

    pipeline = Pipeline([
        ('tfidf-vect', TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
                                       encoding='utf-8', ngram_range=(1, 2),
                                       stop_words='english')),
        ('model', LogisticRegression()),
    ])

    train_data, test_data, train_label, test_label = train_test_split(
        data, labels, random_state=0, test_size=0.2)

    classifier = pipeline.fit(train_data, train_label)

    Classifier.objects.update_or_create(id=1, defaults={
        'classifier': dumps(classifier)
    })

    prediction = classifier.predict(test_data)

    return len(train_data), len(test_data), np.mean(prediction == test_label)
