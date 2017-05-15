from django.shortcuts import render_to_response

# handler400
def bad_request(request):
    response = render_to_response(
        'homepage/error.html',
        {
            'error': 'Erro 400',
            'errorname': 'Pedido invalido',
            'errordesc': 'O servidor nao pode processar o seu pedido devido a sintaxe incorreta.'
        }
    )
    response.status_code = 400
    return response

# handler403
def permission_denied(request):
    response = render_to_response(
        'homepage/error.html',
        {
            'error': 'Erro 403',
            'errorname': 'Acesso proibido',
            'errordesc': 'O servidor nao permite acesso ao recurso requisitado.'
        }
    )
    response.status_code = 403
    return response

# handler404
def page_not_found(request):
    response = render_to_response(
        'homepage/error.html',
        {
            'error': 'Erro 404',
            'errorname': 'Recurso nao encontrado',
            'errordesc': 'A pagina que voce tentou acessar nao existe ou foi movida.'
        }
    )
    response.status_code = 404
    return response

# handler500
def server_error(request):
    response = render_to_response(
        'homepage/error.html',
        {
            'error': 'Erro 500',
            'errorname': 'Erro interno de servidor',
            'errordesc': 'Nao foi possivel processar a solicitacao. Por favor, entre em contato com o administrador.'
        }
    )
    response.status_code = 500
    return response

