#!/usr/bin/env python

"""Module for loading data.
Various files in this codebase import this file to load data.
"""

import json
import csv
import pickle
import numpy as np
import IPython as ipy
import os
from gensim.models import word2vec

DATA_DIR = os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + "/data/"


def get_idtoloc():
    """ Returns dict: unique_id --> (lat, lng)
    If (None, None): geocode did not return a latitude/longitude

    Response Format:
    {
        u'1fe9adec-46f3-48f8-9fdd-4b715115a091': (38.3401715, -85.6214021),
        u'1fee61a2-571d-4789-ac98-3d670bc9acb3': (39.871075, -84.889905),
        u'1fee61a2-571d-4789-ac98-3d670bc9acb3': (None, None),
        ...
        u'2002c9ca-45a5-49a1-921b-191b2760c89f': (35.3930786, -119.120998),
    }
    """
    return pickle.load(open(DATA_DIR + 'id_to_loc.pickle', 'r'))


def get_naicslist():
    """ Returns list of json naics objects

    Response Format:
    [
        {
            "code": 928120,
            "description": "This industry comprises establishments of U.S. and foreign governments pr...",
            "title": "International Affairs"
        },
        ...
    ]
    """
    ipy.embed
    return json.load(open(DATA_DIR + 'naics_list.json', 'r'))


def get_naics_dict():
    """ Returns dict of json naics code to objects

    Response Format:
    {
        "928120": {
            "code": 928120,
            "description": "This industry comprises establishments of U.S. and foreign governments primarily ...",
            "title": "International Affairs"
        }
    },
    ...
    ]
    """
    naics_dict = {}
    for naics in get_naicslist():
        naics_dict[naics['code']] = naics
    return naics_dict


def get_test_classifiedset():
    """ Returns dictionary of classified NAICS for testing

    Response Format:
    {
        'c7103540-d25d-4f7f-9b4d-984eecf6ff7b': '54',
        'df039e7a-a0b5-4700-9823-1119c771f59f': '51',
        ...
        'fe389cac-3795-4b4c-9d09-39b77e166f5a': '444'
    }
    """
    with open(DATA_DIR + 'classified_set.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        d = {}
        for row in spamreader:
            d[row[0]] = row[1]
    return d


def get_hand_classifiedset():
    """ Returns dictionary of classified NAICS that will be submitted

    Response Format:
    {
        'c7103540-d25d-4f7f-9b4d-984eecf6ff7b': '54',
        'df039e7a-a0b5-4700-9823-1119c771f59f': '51',
        ...
        'fe389cac-3795-4b4c-9d09-39b77e166f5a': '444'
    }
    """
    with open(DATA_DIR + 'hand_classified_set.csv', 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        d = {}
        for row in spamreader:
            d[row[0]] = row[1]
    return d


def get_algo_classifiedset():
    """ Returns dictionary of classified NAICS that will be submitted

    Response Format:
    {
        'c7103540-d25d-4f7f-9b4d-984eecf6ff7b': '54',
        'df039e7a-a0b5-4700-9823-1119c771f59f': '51',
        ...
        'fe389cac-3795-4b4c-9d09-39b77e166f5a': '444'
    }
    """
    with open(DATA_DIR + 'predictions.csv', 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        d = {}
        for row in spamreader:
            d[row[0]] = row[1]
    return d


def reset_algo_classifiedset():
    """
    deletes contents of the predictions
    """
    open(DATA_DIR + 'predictions.csv', 'w').close()


def get_challengeset(chunk=None):
    """ Returns the list of businesses

    Response Format:
    [
        {   u'address': u'2136 PLEASANT HILL RD, MARION OH 43302',
            u'description': u'If you are looking for the best prices on any of the Amsoil Prod...',
            u'name': u'marion amsoil dealer',
            u'unique_id': u'ed6ad152-a7d3-4fdc-b3d9-aff1094d3ea5',
            u'website': [u'http://www.amsoil.com']
        },
        ...
    ]
    """
    challenge_set = json.load(open(DATA_DIR + 'challenge_set.json', 'r'))
    if chunk == 0:
        return challenge_set[:3333]
    elif chunk == 1:
        return challenge_set[3333:6666]
    elif chunk == 2:
        return challenge_set[6666:]
    else:
        return challenge_set


def get_business_types():
    """ Returns dict: unique_id --> type
    If None: could not get a type

    Response Format:
    {
        u'1fe9adec-46f3-48f8-9fdd-4b715115a091': restaurant,
        u'1fee61a2-571d-4789-ac98-3d670bc9acb3': cafe,
        u'1fee61a2-571d-4789-ac98-3d670bc9acb3': None,
        ...
        u'2002c9ca-45a5-49a1-921b-191b2760c89f': museum,
    }
    """
    try:
        return pickle.load(open(DATA_DIR + 'business_types.pickle', 'r'))
    except IOError:
        return {}

def get_naics_data_for_level(code_length):
    """
    :param code_length: length in digits of NAICS code 1-6
    :return: all the NAICS objects with 'code_length' digits
    """
    naics_data = get_naicslist()
    results = []
    for naics_item in naics_data:
        if len(str(naics_item['code'])) == code_length:
            results.append(naics_item)
    return results


def get_unclassified_business_ids():
    """
    :return: all ids for unclassified_busniesses
    """
    businesses = get_challengeset()
    unclassified_ids = []
    ids = get_classified_business_ids()
    for b in businesses:
        if b['unique_id'] not in ids:
            unclassified_ids.append(b['unique_id'])
    return unclassified_ids


def get_word2vecmodel():
    return word2vec.Word2Vec.load(DATA_DIR + "word2vec_model")


def get_word2vecmodel_brown():
    return word2vec.Word2Vec.load(DATA_DIR + "brown_model")


def get_word2vecmodel_reuters():
    return word2vec.Word2Vec.load(DATA_DIR + "reuters_model")


def get_classified_business_ids():
    """
    :return: all business_ids that are classified
    """
    test_classified_set = get_test_classifiedset()
    hand_classified_set = get_hand_classifiedset()
    return list(set(test_classified_set.keys()) | set(hand_classified_set.keys()))


def write_row_classified_set(business_uid, naics_code):
    with open(DATA_DIR + 'classified_set.csv', 'a') as classified_set:
        wr = csv.writer(classified_set)
        wr.writerow((business_uid, naics_code))


def write_row_hand_classified_set(business_uid, naics_code):
    with open(DATA_DIR + 'hand_classified_set.csv', 'a') as hand_classified_set_file:
        wr = csv.writer(hand_classified_set_file)
        wr.writerow((business_uid, naics_code))


def write_row_algo_classified_set(business_uid, naics_code):
    with open(DATA_DIR + 'predictions.csv', 'a') as algo_classified_set:
        wr = csv.writer(algo_classified_set)
        wr.writerow((business_uid, naics_code))

def write_rows_algo_classified_set(rows):
    with open(DATA_DIR + 'predictions.csv', 'a') as algo_classified_set:
        wr = csv.writer(algo_classified_set)
        for business_uid, naics_code in rows:
            wr.writerow((business_uid, naics_code))

def get_id_to_index():
    return pickle.load(open(DATA_DIR + "classification/id_to_index.pickle", "r"))


def get_index_to_id():
    return pickle.load(open(DATA_DIR + "classification/index_to_id.pickle", "r"))


def get_id_to_bizid():
    return pickle.load(open(DATA_DIR + "classification/id_to_bizid.pickle", "r"))


def dump_business_dict(b_dict):
    pickle.dump(b_dict, open(DATA_DIR + 'business_types.pickle', 'w'))


def get_industry_counts():
    """
    :return: returns a dictionary of each NAICS code to its respective number of business
    """
    industry_counts = {}
    with open(DATA_DIR + 'industry_counts.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            industry_counts[int(row[0])] = int(row[1])
    return industry_counts


def get_normalized_industry_counts():
    industry_counts = get_industry_counts()
    new_industry_counts = dict()
    x = reduce(lambda a, b: a + b, industry_counts.values())
    for k in industry_counts.keys():
        new_industry_counts[k] = industry_counts[k] * 1.0 / x
    return new_industry_counts


def get_S():
    """
    :return: list of similarity matrices
    """
    S = []
    for i in xrange(9):
        S.append(np.load(DATA_DIR + "classification/s" + str(i) + ".npy"))
    return S

if __name__ == '__main__':
    ipy.embed()
