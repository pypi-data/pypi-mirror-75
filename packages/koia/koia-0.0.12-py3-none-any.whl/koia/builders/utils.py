from typing import Any, Dict, Iterable, List, Union


def check_for_exist_key(
    query_conf: dict,
    query_operations: list,
    query_items: str,
    exist_key: str,
    replace_key: Union[str, int],
) -> Iterable[Any]:
    if exist_key == "WHERE":
        return [
            element.replace(exist_key, replace_key)
            if len([elem for elem in query_operations if "WHERE" in elem]) > 0
            or key > 0
            else element
            for key, element in enumerate(query_conf[query_items])
        ]
    elif exist_key == "ORDER BY":
        return [
            element.replace(exist_key, replace_key)
            if len([elem for elem in query_operations if "ORDER BY" in elem]) > 0
            or key > 0
            else element
            for key, element in enumerate(query_conf[query_items])
        ]
    elif exist_key == "take":
        return [element for element in query_conf[query_items]]

    return []


def sort_fetched_data(fetch: list, field_names: list) -> List[Dict[str, dict]]:
    sorted_data: List[Dict[str, dict]] = [
        {
            field_names[counter]: fetch[index][counter]
            for counter in range(0, len(field_names))
        }
        for index in range(len(fetch))
    ]
    return sorted_data
