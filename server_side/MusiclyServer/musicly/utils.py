from json import loads as load_json


def unpack_common_filters(request, category):
    order_by = 'id'
    top = None

    if category == 'playlist':
        timestamp_name = 'modification_timestamp'
    else:
        timestamp_name = 'status_timestamp'

    if request.body:
        params = load_json(request.body)
        if 'chronological_order' in params.keys():
            if params['chronological_order'] == 'asc':
                order_by = timestamp_name
            elif params['chronological_order'] == 'desc':
                order_by = f'-{timestamp_name}'
        if 'top' in params.keys():
            top = params['top']
    return order_by, top
