def response(status, message, code):
    response_object = {
        'status': status,
        'message': message
    }
    return response_object, int(code)


def success_response(message, code):
    return response('success', message, code)


def fail_response(message, code):
    return response('fail', message, code)
