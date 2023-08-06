#!/usr/bin/env python

"""Tests for `nlp_dict` package."""


from nlp_dict import nlp_dict

def test_get_pipeline():
    data = ["明天天气", "「‘한글"]
    preprocess = nlp_dict.get_pipeline(5)
    result = preprocess(data)
    print(result)

    preprocess = nlp_dict.get_pipeline()
    result = preprocess(data)
    print(result)
