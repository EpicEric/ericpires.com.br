from django.shortcuts import render, render_to_response

def error404(request):
    context = {
        'error': 'Erro 404',
        'errorname': 'Recurso nao encontrado',
        'errordesc': 'A pagina que voce tentou acessar nao existe ou foi movida.',
    }
    return render_to_response('homepage/error.html', context)

def error500(request):
    context = {
        'error': 'Erro 500',
        'errorname': 'Erro interno de servidor',
        'errordesc': 'Nao foi possivel processar a solicitacao. Por favor, entre em contato com o administrador.',
    }
    return render_to_response('homepage/error.html', context)
