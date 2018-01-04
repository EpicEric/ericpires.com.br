from django.shortcuts import render_to_response

def error404(request, exception):
    context = {
        'error': 'Erro 404',
        'errorname': 'Recurso não encontrado',
        'errordesc': 'A página "{}" que você tentou acessar não existe ou foi removida.'.format(request.path),
    }
    return render_to_response('homepage/error.html', context, status=404)

def error500(request):
    context = {
        'error': 'Erro 500',
        'errorname': 'Erro interno de servidor',
        'errordesc': 'Não foi possível processar a solicitação. Por favor, entre em contato com o administrador.',
    }
    return render_to_response('homepage/error.html', context, status=500)
