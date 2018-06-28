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
from rdmt.models import Classifier


def _get_dataset_meta():
    dataset_dir = settings.DATASET_DIR
    info = []

    for reg_name, reg_meta in Classifier.regions.items():
        reg = {
            'name': reg_name,
            'description': reg_meta[0],
            'lobs': [],
            'size': 0
        }
        info.append(reg)
        if reg_name == 'Unknown':
            size = len(glob.glob(path.join(dataset_dir, reg_name, '*')))
            reg['size'] += size
        else:
            for lob_name, lob_meta in Classifier.lobs.items():
                lob = {
                    'name': lob_name,
                    'description': lob_meta[0],
                    'regions': [],
                    'size': 0
                }
                reg['lobs'].append(lob)
                if lob_name == 'Unknown':
                    size = len(glob.glob(path.join(dataset_dir, reg_name, lob_name, '*')))
                    lob['size'] += size
                else:
                    for cat_name, cat_meta in Classifier.categories.items():
                        size = len(
                            glob.glob(path.join(dataset_dir, reg_name,
                                                lob_name, cat_name, '*'))
                        )
                        reg['size'] += size
                        lob['size'] += size
                        lob['regions'].append({
                            'name': cat_name,
                            'size': size,
                            'description': cat_meta[0]
                        })
    return info


def _get_dataset():
    dataset_dir = settings.DATASET_DIR
    reg_data, reg_labels = [], []
    lob_data, lob_labels = [], []
    cat_data, cat_labels = [], []

    for reg_name, reg_meta in Classifier.regions.items():
        if reg_name == 'Unknown':
            for file_ in glob.glob(path.join(dataset_dir, reg_name, '*')):
                with open(file_, 'r', errors='ignore') as stream:
                    content = stream.read()
                reg_data.append(content)
                reg_labels.append(reg_meta[1])
        else:
            for lob_name, lob_meta in Classifier.lobs.items():
                if lob_name == 'Unknown':
                    for file_ in glob.glob(path.join(dataset_dir, reg_name, lob_name, '*')):
                        with open(file_, 'r', errors='ignore') as stream:
                            content = stream.read()
                        lob_data.append(content)
                        lob_labels.append(lob_meta[1])
                else:
                    for cat_name, cat_meta in Classifier.categories.items():
                        for file_ in glob.glob(
                            path.join(
                                dataset_dir, reg_name, lob_name, cat_name, '*')):
                            with open(file_, 'r', errors='ignore') as stream:
                                content = stream.read()
                            reg_data.append(content)
                            reg_labels.append(reg_meta[1])
                            lob_data.append(content)
                            lob_labels.append(lob_meta[1])
                            cat_data.append(content)
                            cat_labels.append(cat_meta[1])

    return reg_data, reg_labels, lob_data, lob_labels, cat_data, cat_labels


def _get_pipeline():
    return Pipeline([
        ('tfidf-vect', TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
                                       encoding='utf-8', ngram_range=(1, 2),
                                       stop_words='english')),
        ('model', LogisticRegression()),
    ])

def train_and_update_db():
    reg_data, reg_labels, lob_data, lob_labels, cat_data, cat_labels = _get_dataset()

    reg_pipeline = _get_pipeline()
    lob_pipeline = _get_pipeline()
    cat_pipeline = _get_pipeline()

    tr_reg_data, test_reg_data, tr_reg_label, test_reg_label = train_test_split(
        reg_data, reg_labels, random_state=0, test_size=0.2)

    tr_lob_data, test_lob_data, tr_lob_label, test_lob_label = train_test_split(
        lob_data, lob_labels, random_state=0, test_size=0.2)

    tr_cat_data, test_cat_data, tr_cat_label, test_cat_label = train_test_split(
        cat_data, cat_labels, random_state=0, test_size=0.2)

    reg_classifier = reg_pipeline.fit(tr_reg_data, tr_reg_label)
    lob_classifier = lob_pipeline.fit(tr_lob_data, tr_lob_label)
    cat_classifier = cat_pipeline.fit(tr_cat_data, tr_cat_label)

    reg_prediction = reg_classifier.predict(test_reg_data)
    lob_prediction = lob_classifier.predict(test_lob_data)
    cat_prediction = cat_classifier.predict(test_cat_data)

    accuracy = np.mean([
        np.mean(reg_prediction == test_reg_label),
        np.mean(lob_prediction == test_lob_label),
        np.mean(cat_prediction == test_cat_label)
    ])

    Classifier.objects.update_or_create(id=1, defaults={
        'accuracy': accuracy,
        'region': dumps(reg_classifier),
        'lob': dumps(lob_classifier),
        'category': dumps(cat_classifier)
    })

    return len(tr_reg_data), len(test_reg_data), accuracy
