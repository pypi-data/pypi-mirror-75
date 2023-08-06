import json

import pkg_resources
from nlp_utils.preprocess.clean.chars_replace import CharsReplace
from nlp_utils.preprocess.lookup_table import LookupTable
from nlp_utils.preprocess.text_preprocess import TextPreprocess
from nlp_utils.preprocess.padding import SequencePaddding
from nlp_utils.chars import variety_to_normal


def get_pipeline(max_length=None):
    data_file = pkg_resources.resource_filename(__name__, "./resources/dict.json")
    with open(data_file) as fd:
        data = json.load(fd)

    padding = "<PAD>"
    oov_key = "<UNK>"
    lookup_table = [oov_key] + [padding] + data

    char_replace = {
        **variety_to_normal.small_to_full_punc,
        **variety_to_normal.zht_to_zhs,
        **variety_to_normal.number_to_normal,
        **variety_to_normal.fullwidth_to_halfwidth,
    }

    char_replace_src = list(char_replace.keys())
    char_replace_target = list(char_replace.values())

    char_replace_component = CharsReplace(char_replace_src, char_replace_target)
    lookup_table_component = LookupTable(lookup_table, oov_key=oov_key)
    sequence_padding_component = SequencePaddding(padding, max_length)

    if max_length is None:
        pipeline = [
            char_replace_component,
            lookup_table_component,
        ]
    else:
        pipeline = [
            char_replace_component,
            sequence_padding_component,
            lookup_table_component,
        ]
    tp = TextPreprocess(pipeline)
    return tp
