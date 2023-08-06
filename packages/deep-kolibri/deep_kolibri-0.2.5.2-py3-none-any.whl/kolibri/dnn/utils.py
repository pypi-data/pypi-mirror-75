# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: helpers.py
@time: 2019-05-17 11:37

"""
import json
import os
import pathlib
import pydoc
import random
import time
from typing import List, Optional, Dict

import tensorflow
from tensorflow.python import keras, saved_model

custom_objects = tensorflow.keras.utils.get_custom_objects()
# from kolibri.dnn.embeddings.base_embedding import Embedding
from kolibri.dnn.layers.crf import ConditionalRandomField as CRF


# from kolibri.dnn.tasks.classification.base_model import BaseTextClassificationModel
# from kolibri.dnn.tasks.labeling.base_model import BaseLabelingModel


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    c = list(zip(a, b))
    random.shuffle(c)
    a, b = zip(*c)
    return list(a), list(b)


def get_list_subset(target: List, index_list: List[int]) -> List:
    return [target[i] for i in index_list if i < len(target)]


def custom_object_scope():
    return tensorflow.keras.utils.custom_object_scope(custom_objects)


def load_model(model_path: str,
               load_weights: bool = True):
    """
    Load saved model from saved model from `model.save` function
    Args:
        model_path: model folder path
        load_weights: only load model structure and vocabulary when set to False, default True.

    Returns:

    """
    with open(os.path.join(model_path, 'model_info.json'), 'r') as f:
        model_info = json.load(f)

    model_class = pydoc.locate(f"{model_info['module']}.{model_info['class_name']}")
    model_json_str = json.dumps(model_info['tf_model'])

    model = model_class()
    model.tf_model = tensorflow.keras.models.model_from_json(model_json_str, custom_objects)
    if load_weights:
        model.tf_model.load_weights(os.path.join(model_path, 'model_weights.h5'))

    embed_info = model_info['embedding']
    embed_class = pydoc.locate(f"{embed_info['module']}.{embed_info['class_name']}")
    embedding = embed_class._load_saved_instance(embed_info,
                                                 model_path,
                                                 model.tf_model)

    model.embedding = embedding

    if type(model.tf_model.layers[-1]) == CRF:
        model.layer_crf = model.tf_model.layers[-1]

    return model


def load_indexer(model_path: str):
    """
    Load indexer from model
    When we using tf-serving, we need to use model's indexer to pre-process texts
    Args:
        model_path:

    Returns:

    """
    with open(os.path.join(model_path, 'model_info.json'), 'r') as f:
        model_info = json.load(f)

    indexer_info = model_info['embedding']['indexer']
    indexer_class = pydoc.locate(f"{indexer_info['module']}.{indexer_info['class_name']}")
    indexer = indexer_class(**indexer_info['config'])
    return indexer


def convert_to_saved_model(model,
                           model_path: str,
                           version: str = None,
                           inputs: Optional[Dict] = None,
                           outputs: Optional[Dict] = None):
    """
    Export model for tensorflow serving
    Args:
        model: Target model
        model_path: The path to which the SavedModel will be stored.
        version: The model version code, default timestamp
        inputs: dict mapping string input names to tensors. These are added
            to the SignatureDef as the inputs.
        outputs:  dict mapping string output names to tensors. These are added
            to the SignatureDef as the outputs.
    """
    pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)
    if version is None:
        version = round(time.time())
    export_path = os.path.join(model_path, str(version))

    if inputs is None:
        inputs = {i.my_name: i for i in model.tf_model.inputs}
    if outputs is None:
        outputs = {o.my_name: o for o in model.tf_model.outputs}
    sess = keras.backend.get_session()
    saved_model.simple_save(session=sess,
                            export_dir=export_path,
                            inputs=inputs,
                            outputs=outputs)

    with open(os.path.join(export_path, 'model_info.json'), 'w') as f:
        f.write(json.dumps(model.info(), indent=2, ensure_ascii=True))
        f.close()


def load_data_object(data, **kwargs):
    """
    Load Object From Dict
    Args:
        data:
        **kwargs:

    Returns:

    """
    module_name = f"{data['__module__']}.{data['__class_name__']}"
    obj = pydoc.locate(module_name)(**data['config'], **kwargs)
    if hasattr(obj, '_override_load_model'):
        obj._override_load_model(data)

    return obj


if __name__ == "__main__":
    path = '/Users/brikerman/Desktop/python/kolibri.dnn/tests/classification/saved_models/' \
           'kolibri.dnn.tasks.classification.models/BiLSTM_Model'
    p = load_indexer(path)

    print(p.label2idx)
    print(p.token2idx)
