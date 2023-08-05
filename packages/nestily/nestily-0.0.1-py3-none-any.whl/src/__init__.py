""" nested helpers """


def get_(obj, field, default=None):
    if callable(field):
        return field(obj)
    if isinstance(obj, dict):
        return obj.get(field, default)
    return getattr(obj, field, default)


def set_(obj, field, value):
    if isinstance(obj, dict):
        obj[field] = value
    else:
        setattr(obj, field, value)


def nget(dic, keys, _default=None):
    for key in keys[:-1]:
        dic = get_(dic, key, {})
    return get_(dic, keys[-1], _default)


def nexists(dic, keys):
    _dic = dic
    for key in keys:
        if key not in _dic:
            return False
        _dic = _dic[key]
    return True


def nset(dic, keys, val):
    """ Set a nested key-value pair - in-place.
    No-op when a value already exists.
    Example:
        x = {}
        nset(x, ['a', 'b', 'c'], 0)
        print(x)
        > {'a': {'b': {'c': 0}}}

    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = dic.setdefault(keys[-1], val)
    return dic


def ninc(dic, keys):
    """ increments a counter nested within dic """
    cur = nget(dic, keys, 0)
    nset(dic, keys, cur + 1)


def nappend(dic, keys, val):
    """
    Example:
        x = {}
        nappend(x, ['a', 'b'], 1)
        nappend(x, ['a', 'b'], 2)
        print(x)
        > {'a': {'b': [1, 2]}}
    """
    dic = nset(dic, keys, [])
    dic[keys[-1]].append(val)


def nconcat(dic, keys, val_arr):
    dic = nset(dic, keys, [])
    dic[keys[-1]] += val_arr


def nget_obj_vals(obj, keys):
    obj_vals = [get_(obj, key) for key in keys if get_(obj, key) is not None]
    if len(obj_vals) != len(keys):
        return None
    return obj_vals


def get_map(objs, fields, mult=True, get_val=None):
    """ creates a map from a list of objects
    Args:
        objs (arr of dicts): array of dicts to turn into mapping
        fields (arr of strings): keys of dict to use in forming mapping
        mult (bool): whether the mapped values should be unique (a single value) or multiple (an array of values)
        get_val (func): a function, if true the mapped value is computed by applying the function to the mapped dict
    Returns:
        A mapping
    """
    ret_map = {}
    for obj in objs:
        obj_keys = nget_obj_vals(obj, fields)
        if obj_keys:
            obj_val = get_(obj, get_val) if get_val else obj
            if mult:
                nappend(ret_map, obj_keys, obj_val)
            else:
                nset(ret_map, obj_keys, obj_val)
    return ret_map


def nflatten_map(_map):
    """ Flattens the nested mapping and returns an array of the values
    Args:
        _map (dict): output of get_map
    Returns:
        (arr): an array of the values within nflatten_map
    """
    values = []
    if isinstance(_map, dict):
        values += [nflatten_map(val) for val in _map.values()]
    elif isinstance(_map, list):
        values += _map
    return values


def get_groups(objs, fields, include_keys=False):
    """ gets groups from a list of objecst with matching values for fields
    Args:
        objs (arr of dicts): array of dicts to turn into mapping
        fields (arr of strings): keys of dict to use in forming groups
        include_keys (bool, optional): if True, the tuple of keys found from `fields` will
            be returned as the first value of a tuple with the grouping as the second value
    Returns:
        (arr): if include_keys is False, returns an array of arrays of groups
               if include_keys is True, returns an array of tuples with the first value of
                    each tuple being the keys found from `fields` and the second value of
                    the tuple being the group
    """
    groups_dict = {}
    for obj in objs:
        key = tuple(nget_obj_vals(obj, fields))
        nappend(groups_dict, [key], obj)
    ret_groups = []
    for group_key, groups_arr in groups_dict.items():
        if include_keys:
            ret_groups.append((group_key, groups_arr))
        else:
            ret_groups.append(groups_arr)
    return ret_groups


def nmerge_concat(master_dic, dic_or_arr, prev_key=None):
    if isinstance(dic_or_arr, dict):
        if prev_key:
            master_dic = master_dic.setdefault(prev_key, {})
        for key, val in dic_or_arr.items():
            nmerge_concat(master_dic, val, prev_key=key)
    else:
        master_dic[prev_key] = master_dic.setdefault(prev_key, [])
        master_dic[prev_key] += dic_or_arr


if __name__ == "__main__":
    pass
