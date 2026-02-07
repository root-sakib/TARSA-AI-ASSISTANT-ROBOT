import json
import numpy as np

def vector_to_string(vector):
    return json.dumps(vector.tolist())

def string_to_vector(string):
    return np.array(json.loads(string))
