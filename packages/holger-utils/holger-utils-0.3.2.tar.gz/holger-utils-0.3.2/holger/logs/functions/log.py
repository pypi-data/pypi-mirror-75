from ..todo import LogToDo


def log(response, status_code, index: str, doc, params=None, headers=None):
    metadata = response.get('metadata')
    status = response.get('status')
    metadata.update({
        'transaction': {
            'status': status,
            'index': index,
        }
    })
    todo = LogToDo(response, status_code, index, doc, headers, params)
    results = todo.process()
    for result in results:
        metadata.update(result)
    return response, status_code
