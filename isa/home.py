from django.http import HttpResponse

def index(request):
	httpcode = "Hello, world!\n"
	return HttpResponse(httpcode)
