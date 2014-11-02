from django.shortcuts import render,render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from clients.models import Client
from invoices.models import Invoice, Item

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
	clients = Client.objects.all()
	t = loader.get_template('clients/index.html')
	c = RequestContext(request,{'clients': clients})
	return HttpResponse(t.render(c))

@login_required
def detail(request, id):
	client = Client.objects.get(pk=id)
	invoices = Invoice.objects.filter(client_id=id).order_by('-id')
	data = {'client': client, 'invoices':invoices}
	t = loader.get_template('clients/detail.html')
	c = RequestContext(request,data)
	return HttpResponse(t.render(c))

def edit(request, id):
	if request.method == "POST":
		client_id = request.POST['input_id']
		client = Client.objects.get(pk=client_id)
		client.name = request.POST['input_name']
		client.rut = request.POST['input_rut']
		client.address = request.POST['input_address']
		client.phone = request.POST['input_phone']
		client.save()
		return HttpResponseRedirect("/clients/%s/"%client_id)
	else:
		client = Client.objects.get(pk=id)
		t = loader.get_template('clients/edit.html')
		c = RequestContext(request,{'client': client})
		return HttpResponse(t.render(c))

@login_required
def create(request):
	next_page = 'clients/create.html'
	if request.method == 'POST':
		name = str(request.POST['input_name'])
		rut = str(request.POST['input_rut'])
		address = str(request.POST['input_address'])
		phone = str(request.POST['input_phone'])
		if not name or not rut or not address:
			raise Exception('Campos obligatorios')
		c = Client(
			name = name,
			rut = rut,
			address = address,
			phone = phone
			)
		c.save()
		next_page = 'clients/index.html'
		return HttpResponseRedirect("/clients/")

	t = loader.get_template(next_page)
	c = RequestContext(request)
	return HttpResponse(t.render(c))