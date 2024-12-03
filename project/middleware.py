from django.shortcuts import resolve_url

class AppBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/project/'):
            request.session['login_redirect'] = resolve_url('recipe_list')
        return self.get_response(request)
