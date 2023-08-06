import path
import json
import sys
# sys.path.insert(1, '../../NER_v2')
from ne_def import *


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Enter path to buffer for .conllu files, raw text file and annotation file, output path")
        exit()
    elif len(sys.argv) < 3:
        print("Text from file: " + sys.argv[1])
        print("Enter the annotation file")
        exit()
    elif len(sys.argv) < 4:
        print("Text from file: " + sys.argv[1])
        print("Annotation from file: " + sys.argv[2])
        print("Enter output path")
        exit()
    else:
        print("Text from file: " + sys.argv[1])
        print("Annotation from file: " + sys.argv[2])
        print("Output is written to: " + sys.argv[3])

    txt_path = sys.argv[1]
    ann_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(txt_path) as input_file:
        whole_doc = input_file.read()

    all_persons, all_others, all_relations = path.get_ne_rl(ann_path)
    all_entities = all_persons + all_others

    """
    var collData = {
        entity_types: [ {
                type   : 'Person',
                labels : ['Person', 'Per'],
                bgColor: '#7fa2ff',
                borderColor: 'darken'
        } ]
    };

    var docData = {
        text     : "Ed O'Kelley was the man who shot the man who shot Jesse James.",
        entities : [
            ['T1', 'Person', [[0, 11]]],
            ['T2', 'Person', [[20, 23]]],
            ['T3', 'Person', [[37, 40]]],
            ['T4', 'Person', [[50, 61]]],
        ],
        relations : [
            // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
            ['R1', 'Anaphora', [['Person', 'T2'], ['Person', 'T1']]],
            ['R2', 'Anaphora', [['Person', 'T2'], ['Person', 'T3']]]
        ],
    };
    """

    brat_json = {}
    brat_json["text"] = whole_doc

    brat_json["entities"] = []
    for entity in all_entities:
        brat_json["entities"].append(['T' + str(entity.id), inv_label_mapping[entity.type], [entity.span]])

    brat_json["relations"] = []
    for rel in all_relations:
        brat_json["relations"].append(['R'+str(rel.id), rel.type, [ \
            [inv_label_mapping[rel.arg1.type], 'T' + str(rel.arg1.id)], \
            [inv_label_mapping[rel.arg2.type], 'T' + str(rel.arg2.id)] ]])

    with open(out_path, 'w') as outfile:
        json.dump(brat_json, outfile)
