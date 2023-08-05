import pandas as pd
import numpy as np
import base64
import json

from io import BytesIO
from puppettable.utils import dechunkize, chunkize, to_parquet_bytes
from azure.cosmosdb.table import Entity


def generate_entity(data, partition_key, row_key, metadata=None, chunk_size=32495, max_size=649900):
    if metadata is None:
        metadata = {}

    data_value = None
    data_str = None
    data_type = str(type(data).__name__)


    if type(data) in [pd.DataFrame, pd.Series]:
        data_str = str(base64.b64encode(to_parquet_bytes(pd.DataFrame(data))), "ASCII")
    elif type(data) is np.ndarray:
        data_str = json.dumps(data.tolist())
    elif isinstance(data, np.generic):
        data_value = data.item()
        data_type = str(np.generic.__name__)
    elif type(data) in [list, dict, tuple]:
        data_str = json.dumps(data)
    elif type(data) is bytes:
        data_str = str(base64.b64encode(data), "ASCII")
    elif type(data) in [str, int, float]:
        data_value = data
    else:
        raise Exception(f"Data type {type(data)} not understood.")

    if data_value is None and len(data) > max_size:
        raise Exception(f"Max length ({max_size}) exceeeded.")

    element_size = len(data_str.encode("UTF-8")) if data_str else len(str(data_value).encode("UTF-8"))

    chunks = chunkize(data_str, chunk_size=chunk_size)

    if data_value is not None:
        entity_fields = {"X_0": data_value}
    else:
        entity_fields = {
            f"X_{i}": chunk for i, chunk in enumerate(chunks)
        }

    entity_fields.update({
        "type": data_type,
        "PartitionKey": partition_key,
        "RowKey": row_key,
        "metadata": json.dumps(metadata)
    })

    entity = Entity(entity_fields)
    return entity, element_size


def parse_entity(entity):
    chunk_keys = [f"X_{i}" for i in sorted([int(k.split("_")[1]) for k in entity.keys() if k.startswith("X_")])]

    data_str = None
    data_value = None

    if entity["type"] in ["str", "int", "float", "generic"]:
        data_value = entity["X_0"]
    else:
        data_str = dechunkize([entity[key] for key in chunk_keys])

    new_entity = {k: v for k, v in entity.items() if not k.startswith("X_")}
    new_entity['metadata'] = json.loads(new_entity['metadata'])

    if data_value is None:
        if entity["type"] in ["list", "dict", "tuple"]:
            data = json.loads(data_str)
        elif entity["type"] == "Series":
            data = base64.b64decode(data_str)
            data = pd.read_parquet(BytesIO(data), engine='pyarrow').iloc[:, 0]
        elif entity["type"] == "DataFrame":
            data = base64.b64decode(data_str)
            data = pd.read_parquet(BytesIO(data), engine='pyarrow')
        elif entity["type"] == "ndarray":
            data = np.asarray(json.loads(data_str))
        elif entity["type"] == "bytes":
            data = base64.b64decode(data_str)
        else:
            raise Exception(f"Data type not understood {entity['type']}")

        new_entity.update({"X": data})
    else:
        new_entity.update({"X": data_value})

    return new_entity


def parse_elements(raw_elements):
    if len(raw_elements) == 0:
        return raw_elements

    if type(raw_elements) is list and len(raw_elements) > 0:
        parsed_elements = [element['X'] for element in raw_elements]
        metadata = raw_elements[0]['metadata']
        elements_shape = list((len(parsed_elements),)) + list(metadata.get('original_shape', (-1,)))
        grouped = True
    else:
        parsed_elements = raw_elements['X']
        metadata = raw_elements['metadata']
        elements_shape = metadata.get('original_shape', (-1,))
        grouped = False

    if metadata.get('datatype', "unknown") == "numpy_array":      # It is a numpy array
        parsed_elements = np.stack(parsed_elements, axis=0).reshape(elements_shape)

    elif metadata.get('datatype', "unknown") in ["pandas_series", "pandas_dataframe"] and grouped:  # It is a Pandas DataFrame
        parsed_elements = pd.concat([serie.to_frame().T for serie in parsed_elements])

    return parsed_elements


def build_elements(elements, single_element=False):
    if type(elements) is np.ndarray:
        if single_element:
            old_shape = elements.shape
            new_shape = (1, -1)
        else:
            old_shape = elements.shape[1:]
            new_shape = (elements.shape[0], np.cumprod(elements.shape[::-1])[-2])

        elements = elements.reshape(new_shape)
        metadata = {'original_shape': old_shape, 'datatype': "numpy_array"}

    elif type(elements) in [pd.Series, pd.DataFrame]:
        metadata = {'datatype': "pandas_series"}

    elif type(elements) in [list, dict] and not single_element:
        elements = [[element] for element in elements]
        metadata = {}

    else:
        metadata = {}

    return elements, metadata

