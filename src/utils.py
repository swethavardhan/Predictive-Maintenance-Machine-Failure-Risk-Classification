import pickle
import os

def save_object(file_path, obj):
    """
    Save a Python object to a file using pickle.
    Creates directories if they don't exist.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)
