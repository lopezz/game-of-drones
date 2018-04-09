from django.template.response import SimpleTemplateResponse

def home(request):
    """Renders the home template"""
    template_name = 'ui/home.html'
    return SimpleTemplateResponse(template_name, {})