import os
import json
import logging


def upper_dir(path=None, level=1):
    path = path or os.getcwd()
    for _ in range(level):
        path = os.path.dirname(path)
    return path


def find_and_replace_all(str_to_find, str_to_replace, path=None, include_files=True, include_dirs=False):
    path = path or os.getcwd()
    counter_dirs = 0
    counter_files = 0
    for (root, dirs, files) in os.walk(path, topdown=False):
        if include_dirs:
            for dir_ in dirs:
                if str_to_find in dir_:
                    current_name = os.path.join(root, dir_)
                    new_name = dir_.replace(str_to_find, str_to_replace)
                    while os.path.exists(os.path.join(root, new_name)):
                        new_name += '(1)'
                    new_name = os.path.join(root, new_name)
                    os.rename(current_name, new_name)
                    counter_dirs += 1
        if include_files:
            for file_ in files:
                if str_to_find in file_:
                    current_name = os.path.join(root, file_)
                    name, ext = os.path.splitext(file_)
                    new_name = name.replace(str_to_find, str_to_replace)
                    while os.path.isfile(os.path.join(root, new_name+ext)):
                        new_name += '(1)'
                    new_name = os.path.join(root, new_name+ext)
                    os.rename(current_name, new_name)
                    counter_files += 1
    return f'{counter_dirs} directories were renamed and {counter_files} files were renamed.'


def write_json_file(pyton_dic: dict, file_name: str) -> bool:
    """Generate file.json from a python dictionary.
    ex. json_to_file(pyton_dictionary ,'c:\\file.json')
    """
    try:
        with open(file_name, 'w') as fp:
            json.dump(pyton_dic, fp, indent=2)
        return True
    except Exception:
        logging.exception("Exception occurred")
        return False


def load_json_file(file_name: str) -> dict:
    """Load dictionary object from a file.json file.
    ex. file_to_python('c:\\file.json')
    """
    try:
        with open(file_name) as jf:
            try:
                return json.load(jf)
            except:
                logging.exception("Exception occurred")
                return None
    except Exception:
        logging.exception("Exception occurred")
        return None
