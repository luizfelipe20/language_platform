from django.utils.deprecation import MiddlewareMixin

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Aqui você captura TODA requisição antes de chegar na view
        print("➡️ REQUISIÇÃO ENTRANDO:")
        print(f"URL: {request.path}")
        print(f"Método: {request.method}")
        print(f"Headers: {request.headers}")
        print(f"Body: {request.body}")  # cuidado em produção!
        return None

    def process_response(self, request, response):
        # Aqui você captura TODA resposta antes de sair do Django
        print("⬅️ RESPOSTA SAINDO:")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response['Content-Type']}")
        print(f"Body: {response.content}")  # cuidado em produção!
        return response
