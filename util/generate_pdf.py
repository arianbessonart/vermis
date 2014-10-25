from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter, A4
from io import BytesIO


class GeneratePdf(object):
	"""docstring for GeneratePdf"""

	# def generate_pdf(**kwargs):
	def generate_pdf(self, **kwargs):
		client = kwargs['client']
		invoice = kwargs['invoice']
		items = kwargs['items']
		# pdf_file_name = '/tmp/test.pdf'

		buffer = BytesIO()
		c = canvas.Canvas(buffer, pagesize=A4)
		c.setFont('Helvetica', 12, leading = None)

		x_rut = 14.5*cm
		x_address = 3*cm
		x_name = 3*cm
		x_iva_tag = 15.1*cm
		x_item_detail = 2*cm
		x_right_column = 17*cm

		y_rut = 26.1*cm
		y_date = 24.2*cm
		y_name = 24.8*cm
		y_address = 24.2*cm
		y_item = 22.5*cm
		y_sub_total = 17.9*cm
		y_iva = 17.2*cm
		y_iva_tag = 17.2*cm
		y_total = 16.4*cm

		coordinates = {'x_rut':x_rut,'x_address':x_address,'x_name':x_name,'x_iva_tag':x_iva_tag,
		'x_item_detail':x_item_detail,'x_right_column':x_right_column,
		'y_rut':y_rut,'y_date':y_date,'y_name':y_name,'y_address':y_address,
		'y_item':y_item,'y_sub_total':y_sub_total,'y_iva':y_iva,'y_iva_tag':y_iva_tag,
		'y_total':y_total}

		y_rut_cp_client = 10.6*cm
		y_date_cp_client = 8.6*cm
		y_name_cp_client = 9.3*cm
		y_address_cp_client = 8.6*cm
		y_item_cp_client = 7*cm
		y_sub_total_cp_client = 2.3*cm
		y_iva_cp_client = 1.6*cm
		y_iva_tag_cp_client = 1.6*cm
		y_total_cp_client = 0.9*cm

		coordinates_cp_client = {'y_rut':y_rut_cp_client,'y_date':y_date_cp_client,
		'y_name':y_name_cp_client,'y_address':y_address_cp_client,'y_item':y_item_cp_client,
		'y_sub_total':y_sub_total_cp_client,'y_iva':y_iva_cp_client,'y_iva_tag':y_iva_tag_cp_client,
		'y_total':y_total_cp_client}

		#Print Rut
		# rut = '213227550018'
		rut = client.rut
		#Print Date
		date = str(invoice.date_created)
		#Print Name
		name = client.name
		#Print Address
		address =client.address

		# sub_total = '213443.32'
		sub_total = str(invoice.sub_total)
		iva_tag = '22'
		# iva = '2314.40'
		iva = str(invoice.iva)
		# total = '2134325.56'
		total = str(invoice.total)

		# Se itera para la copia cliente.
		for i in xrange(0,2):
			y_item_tmp = coordinates['y_item']
			c.drawString(coordinates['x_rut'],coordinates['y_rut'], rut)
			c.drawString(coordinates['x_right_column'],coordinates['y_date'], date)
			c.drawString(coordinates['x_name'],coordinates['y_name'], name)
			c.drawString(coordinates['x_address'],coordinates['y_address'], address)

			#Print items
			for item in items:
				c.drawString(coordinates['x_item_detail'], y_item_tmp, item.description)
				c.drawString(coordinates['x_right_column'], y_item_tmp, str(item.price))
				y_item_tmp -= 0.5*cm

			#Print Values
			c.drawString(coordinates['x_right_column'],coordinates['y_sub_total'], sub_total)
			c.drawString(coordinates['x_right_column'],coordinates['y_iva'], iva)
			c.drawString(coordinates['x_iva_tag'],coordinates['y_iva_tag'], iva_tag)
			c.drawString(coordinates['x_right_column'],coordinates['y_total'], total)

			coordinates = dict(coordinates.items() + coordinates_cp_client.items())

		c.showPage()
		c.save()
		pdf = buffer.getvalue()
		buffer.close()
		return pdf
