from django.shortcuts import render_to_response
from django.contrib.auth import logout

def logoutView(request):
  logout(request)
  return render_to_response("logout.html")
