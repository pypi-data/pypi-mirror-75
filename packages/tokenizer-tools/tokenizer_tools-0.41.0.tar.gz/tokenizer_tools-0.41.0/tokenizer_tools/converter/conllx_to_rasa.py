import json

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.converter.conllx_to_offset import conllx_to_offset


def conllx_to_rasa(conllx_file, output_rasa):
    rasa_data = {
        "rasa_nlu_data": {
            "common_examples": [],
            "regex_features": [],
            "lookup_tables": [],
            "entity_synonyms": [],
        }
    }

    rasa_exmaples = rasa_data["rasa_nlu_data"]["common_examples"]

    corpus = Corpus.read_from_file(conllx_file)

    for doc in corpus:
        example = {
            "text": "".join(doc.text),
            "intent": doc.intent,
            "entities": [
                {"start": i.start, "end": i.end, "value": i.value, "entity": i.entity}
                for i in doc.span_set
            ],
        }

        rasa_exmaples.append(example)

    with open(output_rasa, "wt") as fd:
        json.dump(rasa_data, fd, ensure_ascii=False)
