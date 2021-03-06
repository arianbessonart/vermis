from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext 
from django.contrib.auth import logout
from django.core.context_processors import csrf

def index(request):
  c = {}
  c.update(csrf(request))
  if request.GET.has_key('next'):
      return render_to_response('auth/login.html', {'next':request.GET['next']}, context_instance=RequestContext(request))
  return render_to_response('auth/login.html',c)

def auth_view(request):
  username = password = ''
  print str(request.POST)
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print "User:"+str(user)
    if user is not None:
        if user.is_active:
            login(request, user)
            print "Logeando"
            print "Post:"+str(request.POST)
            if request.POST.has_key('next'):
              print "Logeando1"
              return redirect(request.POST['next'])
            print "Logeando2"
            return HttpResponseRedirect('/clients/')
        else:
            return render_to_response('auth/login.html', {'result':2}, 
                                    context_instance=RequestContext(request))
    else:
        return render_to_response('auth/login.html', {'result':1}, 
                                    context_instance=RequestContext(request))
  else:
    c = {}
    return render_to_response('auth/login.html',c)

def logout_view(request):
  print "DesLogeando"
  logout(request)
  return HttpResponseRedirect('/')