from typing import Dict
from .labo import Variable
import ast


def state_to_variable(current_var: Dict) -> Variable:
    current_kind = ""
    current_once = None
    current_array = None
    current_start = None
    current_end = None
    current_step = None

    for child in current_var["props"]["children"]:
        if child["props"]["id"] == "var-kind-select":
            current_kind = child["props"]["value"]

    if current_kind == "once":
        once = [child["props"]["value"] for child in current_var["props"]["children"]
                if child["props"]["id"] == "var-input-once"]
        current_once = float(once[0]) if len(once) > 0 else None

    if current_kind == "array":
        array = [child["props"]["value"] for child in current_var["props"]["children"]
                 if child["props"]["id"] == "var-input-array"]
        current_array = ast.literal_eval(array[0]) if len(array) > 0 else None

    if current_kind == "range":
        start = [child["props"]["value"] for child in current_var["props"]["children"]
                 if child["props"]["id"] == "var-input-start"]
        end = [child["props"]["value"] for child in current_var["props"]["children"]
               if child["props"]["id"] == "var-input-end"]
        step = [child["props"]["value"] for child in current_var["props"]["children"]
                if child["props"]["id"] == "var-input-step"]

        current_start = float(start[0]) if len(start) > 0 else None
        current_end = float(end[0]) if len(end) > 0 else None
        current_step = float(step[0]) if len(step) > 0 else None

    # defaults
    current_once = current_once or 0.0
    current_array = current_array or [0.0]
    current_start = current_start or 0.0
    current_end = current_end or 1.0
    current_step = current_step or 1.0

    name = [child["props"]["value"] for child in current_var["props"]["children"]
            if child["props"]["id"] == "var-name"]

    current_name = str(name[0]) if len(name) > 0 else ""

    if current_kind == "once":
        current_var = Variable(current_name, current_kind, fixed=current_once)
    elif current_kind == "array":
        current_var = Variable(current_name, current_kind, fixed=current_array)
    elif current_kind == "range":
        current_var = Variable(current_name, current_kind, start=current_start, end=current_end, step=current_step)

    return current_var

