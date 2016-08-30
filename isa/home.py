from django.http import HttpResponse

def index(request):
	httpcode = """
<html>
<head>
	<link rel=\"stylesheet\" type=\"text/css\" href=\"/static/admin/css/base.css\"/>
</head>
<body>
	<div id=\"container\"><div id=\"header\"><div id=\"branding\">
		<h1>Hello World!</h1>
	</div></div></div>
</body>
</html>
"""
	return HttpResponse(httpcode)
