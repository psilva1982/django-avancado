'''
Middleware serve para processar a informação que seja necessário por
toda aplicação para que não seja necessário repetir o código
'''

class MetaData(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # Hook de middleware a ser utilizada
    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated:
            mensagem2 = 'Olá %s , bom dia' % request.user.username

        else:
            mensagem2 = 'Olá, bom dia'

        request.session['mensagem2'] = mensagem2

        return None