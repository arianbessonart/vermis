from django.shortcuts import render,render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from invoices.models import Invoice, Item
from clients.models import Client
from util.generate_pdf import GeneratePdf
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
	invoices = Invoice.objects.all().order_by('-id')
	clients = Client.objects.all()
	data = {'invoices': invoices, 'clients':clients}
	t = loader.get_template('invoices/index.html')
	c = RequestContext(request,data)
	return HttpResponse(t.render(c))

@login_required
def create(request):
	next_page = 'invoices/create.html'
	clients = Client.objects.all()
	if request.method == 'POST':
		client = Client.objects.get(pk=request.POST['input_client'])
		reference_name = request.POST['input_reference_name']
		reference_number = -1 if 'input_reference_number' not in request.POST or request.POST['input_reference_number'] == '' else request.POST.get('input_reference_number', -1)
		items_description = request.POST.getlist('input_description')
		items_price = request.POST.getlist('input_price')
		if len(items_description) == 0 or len(items_price) == 0:
			message = 'Debe especificar al menos un item'
			level = 'danger'
			return render(request,'invoices/create.html',{'message': message,'message_level':level})
		input_date = request.POST['input_date_created']
		if input_date == '':
			message = 'Debe especificar la fecha'
			level = 'danger'
			return render(request,'invoices/create.html',{'clients':clients,'message': message,'message_level':level})
		else:
			date_formated = datetime.datetime.strptime(input_date,'%d/%M/%Y').strftime('%Y-%M-%d')

		i = Invoice(
			sub_total = request.POST['input_subtotal'],
			iva = request.POST['input_iva'],
			total = request.POST['input_total'],
			date_created = date_formated,
			reference_number = reference_number,
			reference_name = reference_name,
			client = client
			)
		i.save()
		print items_description
		for index in xrange(0,len(items_description)):
			item = Item(description = items_description[index], price = items_price[index], invoice = i)
			item.save()

		return HttpResponseRedirect('/invoices/%s/'%i.id)
	else:
		selected_client = request.GET.get('client_id','')

	t = loader.get_template(next_page)
	c = RequestContext(request,{'clients':clients, 'selected_client':selected_client})
	return HttpResponse(t.render(c))

@login_required
def detail(request, id):
	invoice = Invoice.objects.get(pk=id)
	items = Item.objects.filter(invoice_id=id).order_by('id')
	client = Client.objects.get(pk=invoice.client.id)
	t = loader.get_template('invoices/detail.html')
	c = RequestContext(request,{'invoice': invoice, 'items': items, 'client':client})
	return HttpResponse(t.render(c))

@login_required
def edit(request, id):
	if request.method == "POST":
		client = Client.objects.get(pk=request.POST['input_client'])
		date_formated = datetime.datetime.strptime(request.POST['input_date_created'], '%d/%M/%Y').strftime('%Y-%M-%d')
		reference_name = request.POST['input_reference_name']
		reference_number = -1 if 'input_reference_number' not in request.POST or request.POST['input_reference_number'] == '' else request.POST.get('input_reference_number', -1)
		i = Invoice.objects.get(pk=id)
		i.sub_total = request.POST['input_subtotal']
		i.iva = request.POST['input_iva']
		i.total = request.POST['input_total']
		i.date_created = date_formated
		i.reference_name = reference_name
		i.reference_number = reference_number
		i.client = client
		i.save()
		Item.objects.filter(invoice_id=i.id).delete()
		items_description = request.POST.getlist('input_description')
		items_price = request.POST.getlist('input_price')
		for index in xrange(0,len(items_description)):
			item = Item(description = items_description[index], price = items_price[index], invoice = i)
			item.save()
		
		return HttpResponseRedirect('/invoices/%s/'%i.id)

	invoice = Invoice.objects.get(pk=id)
	clients = Client.objects.all()
	items = Item.objects.filter(invoice_id=id).order_by('id')
	t = loader.get_template('invoices/edit.html')
	c = RequestContext(request,{'invoice': invoice,'clients':clients, 'items': items, 'selected_client':invoice.client.id})
	return HttpResponse(t.render(c))

@login_required
def generate_pdf(request,id):
	if request.method == 'GET':
		invoice = Invoice.objects.get(pk=id)
		client = Client.objects.get(pk=invoice.client.id)
		items = Item.objects.filter(invoice_id=invoice.id).order_by('id')
		filename = "[%s]%s"%(client.name,datetime.datetime.now().strftime('%Y-%m-%d'))

		try:
			pdf = GeneratePdf().generate_pdf(invoice=invoice, client=client, items=items)
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Length'] = len(response.content)
			response['Content-Disposition'] = 'attachment; filename=%s.pdf'%(filename)
			return response
		except Exception, e:
			print str(e)

	return HttpResponseRedirect('/invoices/')


@login_required
def set_charged_invoice(request,id):
	if request.is_ajax():
		charged_invoice = True if request.POST['charged'] == 'true' else False
		date_formated = None
		if charged_invoice:
			date_formated = datetime.datetime.strptime(request.POST['date_charged'], '%d/%M/%Y').strftime('%Y-%M-%d')
		i = Invoice.objects.get(pk=id)
		i.date_charged = date_formated
		i.charged = charged_invoice
		i.save()
		print str(request.POST.getlist('optionsCharge'))
		return HttpResponseRedirect('/invoices/')
	else:
		print 'is not ajax'

