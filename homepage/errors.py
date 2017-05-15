from django.shortcuts import render, render_to_response

# handler400
def bad_request(request):
    return render_to_response(
        'errors/400.html',
        status=400
    )

# handler403
def permission_denied(request):
    return render_to_response(
        'errors/403.html',
        status=403
    )

# handler404
def page_not_found(request):
    return render_to_response(
        'errors/404.html',
        status=404
    )

# handler500
def server_error(request):
    return render_to_response(
        'errors/500.html',
        status=500
    )

