from django.shortcuts import render, render_to_response

# handler400
def bad_request(request):
    response = render_to_response(
        'errors/400.html',
    )
    response.status_code = 400
    return response

# handler403
def permission_denied(request):
    response = render_to_response(
        'errors/403.html',
    )
    response.status_code = 403
    return response

# handler404
def page_not_found(request):
    response = render_to_response(
        'errors/404.html',
    )
    response.status_code = 404
    return response

# handler500
def server_error(request):
    response = render_to_response(
        'errors/500.html',
    )
    response.status_code = 500
    return response
