from django.shortcuts import render, render_to_response

def error404(request):
    context = {
        'error': 'Erro 404',
        'errorname': 'Recurso não encontrado',
        'errordesc': 'A página que voce tentou acessar não existe ou foi movida.',
    }
    return render_to_response('homepage/error.html', context)

def error500(request):
    context = {
        'error': 'Erro 500',
        'errorname': 'Erro interno de servidor',
        'errordesc': 'Nao foi possível processar a solicitação. Por favor, entre em contato com o administrador.',
    }
    return render_to_response('homepage/error.html', context)
