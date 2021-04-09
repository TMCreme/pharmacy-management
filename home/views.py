from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, F
from django.contrib import messages
from django.forms import formset_factory
from .cart import Cart
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import (
	Medicine, MedicineCategory, Expense, ExpenseCategory, Sale, SalesInvoice, SystemSettings)
from .forms import (
	UserLogin, MedicineCategoryForm, MedicineForm, ExpenseForm, ExpenseCategoryForm,
	SalesInvoiceForm, SaleForm, CartAddProductForm,MedicineQuantityUpdateForm,
	SystemSettingsForm, ReportingForm)

from io import BytesIO
from reportlab.pdfgen import canvas
import datetime
import time
import json

def is_dispenser(user):
	return user.groups.filter(name='Dispenser').exists()

@login_required
def index(request):
	return render(request, 'home/index.html')


def LoginView(request):
	#This is handling user login since I want to include other stuff in my view
	#So I didn't use the builtin auth in the urls.
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, 'You have successfully logged in')
				return redirect('home:index')
			else:
				messages.error(request, 'User entered is not active')
				return redirect('home:login')
				#print('User is None')
		else:
			messages.error(request,'User credentials entered does not exist')
			#print('User is None')
			return redirect('home:login')
	user_login_form = UserLogin
	return render(request, 'home/login.html', {'form':user_login_form})

@login_required
def add_medicine_cat(request):
	if request.method == 'POST':
		form = MedicineCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home:index')
		else:
			messages.error(request, "Form validation failed. Check required form inputs!!!")
			return redirect('home:add_medicine_category')
	form = MedicineCategoryForm
	return render(request, 'home/add_medicine_cat.html', {'form':form})

@login_required
def medicine_cat_view(request):
	med_cat = MedicineCategory.objects.all().order_by('-id')
	return render(request, 'home/medicine_category.html', {'med_cat':med_cat})

@login_required
def add_medicine(request):
	if request.method == 'POST':
		form = MedicineForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Medicine added successfully!!!")
			return redirect('home:medicine_list')
		else:
			messages.eror(request, "Form validation failed. Check required form inputs!!!")
			return redirect('home:add_medicine')
	form = MedicineForm
	return render(request, 'home/add_medicine.html', {'form':form})


@login_required
def medicine_view(request):
	med_list = Medicine.objects.all().order_by('-id')
	com_date = datetime.datetime.fromtimestamp(time.time()+864000)
	if request.method == 'POST':
		#Updating Quantity in motion here---not done yet
		form = MedicineQuantityUpdateForm(request.POST)
		if form.is_valid():
			fmed = form.cleaned_data['medicine']
			fquant = form.cleaned_data['quantity']
			new_med = Medicine.objects.get(name=fmed)
			new_med.quantity = F('quantity')+int(fquant)
			new_med.quantity_left = F('quantity_left') +int(fquant)
			new_med.save()
			messages.success(request, "Quantity loaded successfully")
			return redirect('home:medicine_list')
		else:
			print(form.errors)
			messages.error(request, "Form validation failed")
			return redirect('home:medicine_list')
	form = MedicineQuantityUpdateForm()
	return render(request, 'home/medicine_list.html', {'med_list':med_list,'form':form,'com_date':com_date})

@login_required
def edit_medicine(request, id):
	medicine = get_object_or_404(Medicine, id=id)
	form = MedicineForm(instance=medicine)
	if request.method == 'POST':
		form = MedicineForm(request.POST, instance=medicine)
		if form.is_valid():
			form.save()
			messages.success(request, "Medicine has been edited successfully!!")
			return redirect('home:medicine_list')
		else:
			messages.error(request, "Form validation failed!!!")
			return redirect('home:medicine_list')
	return render(request, 'home/edit_medicine.html', {'medicine':medicine, 'form':form})

@login_required
def edit_medicine_cat(request, id):
	medicine = get_object_or_404(MedicineCategory, id=id)
	form = MedicineCategoryForm(instance=medicine)
	if request.method == 'POST':
		form = MedicineCategoryForm(request.POST, instance=medicine)
		if form.is_valid():
			form.save()
			messages.success(request, "Medicine Category has been edited successfully!!!")
			return redirect('home:medicine_category')
		else:
			messages.error(request, "Form is not valid")
			print(form.errors)
			return redirect('home:medicine_category')
	return render(request, 'home/edit_medicine_cat.html', {'form':form, 'medicine':medicine})		


@login_required
def add_expense_cat(request):
	if request.method == 'POST':
		form = ExpenseCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Expense Category added successfully!!!")
			return redirect('home:expense_category_view')
		else:
			messages.error(request, "Form validation faliled.")
			return redirect('home:add_expense_category')
	form = ExpenseCategoryForm
	return render(request, 'home/add_expense_category.html',{'form':form})

@login_required
def edit_expense_cat(request, id):
	expense_cat = get_object_or_404(ExpenseCategory, id=id)
	form = ExpenseCategoryForm(instance=expense_cat)
	if request.method == 'POST':
		form = ExpenseCategoryForm(request.POST, instance=expense_cat)
		if form.is_valid():
			form.save()
			return redirect('home:expense_category_view')
			messages.success(request, "%s Expense Category has been edited successfully!!!"%expense_cat.category)
		else:
			messages.error(request, "Form is not valid!!!")
			return redirect('home:expense_category_view')
	return render(request, 'home/edit_expense_cat.html', {'form':form})


@login_required
def add_expense(request):
	my_user = {'user':request.user}
	if request.method == 'POST':
		form = ExpenseForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Expense item added successfully!!!")
			return redirect('home:expenses_view')
		else:
			print(form.errors)
			messages.error(request, "Form validation failed!!!")
			return redirect('home:expenses_view')
	form = ExpenseForm(initial=my_user)
	return render(request, 'home/add_expense.html', {'form':form,'user':request.user})

@login_required
def expense_cat_view(request):
	expense_cat = ExpenseCategory.objects.all()
	return render(request, 'home/expense_category.html', {'expense_cat':expense_cat})

@login_required
def expense_view(request):
	expense = Expense.objects.all().order_by('-id')
	return render(request, 'home/expense.html', {'expense':expense})

@login_required
def edit_expense(request, id):
	expense = get_object_or_404(Expense, id=id)
	form = ExpenseForm(instance=expense)
	if request.method == 'POST':
		form = ExpenseForm(request.POST, instance=expense)
		if form.is_valid():
			form.save()
			messages.success(request, "Expense item edited successfully!!!")
			return redirect('home:expenses_view')
		else:
			messages.error(request, "Form validation failed!!!")
			return redirect('home:expenses_view')
	return render(request, 'home/edit_expense.html', {'form':form})

@login_required
@user_passes_test(is_dispenser)
def pos(request):
	my_meds = Medicine.objects.all()
	if request.method == 'POST':
		#print(request.session['pos_select_dict'])
		my_count = request.POST['my_count']
		extras = int(SalesInvoice.objects.latest('id').id+1)
		my_id = "{:06d}".format(extras)
		SalesFormSet = modelformset_factory(Sale, form=SaleForm, extra=my_count)
		formset = SalesFormSet(request.POST or None)
		form = SalesInvoiceForm(request.POST)
		if form.is_valid() and formset.is_valid():
			instances = formset.save(commit=False)
			form.save()
			for instance in instances:
				instance.invoice_id = my_id
				print(instance.quantity_sold)
				instance.save()
				my_sale_quant = sum(Sale.objects.filter(medicine=instance.medicine).values_list('quantity_sold', flat=True))
				my_med_quant = sum(Medicine.objects.filter(name=instance.medicine).values_list('quantity', flat=True))
				Medicine.objects.filter(name=instance.medicine).update(quantity_left = my_med_quant-my_sale_quant)
			return redirect('home:point-of-sales-submit')
		else:
			print(formset.errors)
			print(form.errors)	
			messages.error(request, "Form validation failed!!!")
			return redirect('home:point-of-sales')
	form = SalesInvoiceForm(initial={'user':request.user})
	saleformset = formset_factory(SaleForm, extra=2)
	args ={'my_meds':my_meds, 'saleformset':saleformset,'user':request.user,'form':form}
	return render(request, 'home/pos.html', args)


@login_required
def allsales_view(request):
	allsales = SalesInvoice.objects.all().order_by('-id')
	return render(request, 'home/allsales.html', {'allsales':allsales})

@login_required
def pos_submit_view(request):
	pos_recc = SalesInvoice.objects.latest('id')
	return render(request, 'home/pos_submit.html')

@login_required
def pdf_display(request):
	pos_recc = SalesInvoice.objects.latest('id')
	new_id = "{:06d}".format(pos_recc.id)
	my_sales = Sale.objects.filter(invoice_id=new_id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
	buffer = BytesIO()
	p = canvas.Canvas(buffer)
	try:
		sys_name = SystemSettings.objects.latest('id')
		p.drawString(40, 800, sys_name.title)
		p.drawString(40, 780, sys_name.address)		
	except:
		p.drawString(40, 800, 'Pharmacy.')
		p.drawString(40, 780, 'Address.')
	p.drawString(40, 760, 'Receipt: #'+"{:06d}".format(pos_recc.id))
	p.drawString(40, 740, 'Date: '+str(pos_recc.date.strftime('%Y-%m-%d %H:%M:%S')))
	p.drawString(30, 720, 'Name ')
	p.drawString(130, 720, 'Unit Price')
	p.drawString(200, 720, 'Quantity')
	p.drawString(250, 720, 'Total')
	yp = 700
	for item in my_sales:
		p.drawString(30, yp, item.medicine)
		p.drawString(130, yp, str(item.price))
		p.drawString(200, yp, str(item.quantity_sold))
		p.drawString(250, yp, str(item.cost))
		yp -= 20
	yp -= 30
	p.drawString(80, yp, 'Sales Total: GH '+str(pos_recc.sub_total))
	p.drawString(80, yp-20, 'Discount: GH '+str(pos_recc.discount))
	p.drawString(80, yp-40, 'Total: GH '+str(pos_recc.grand_total))
	p.drawString(80, yp-60, 'Dispenser: '+request.user.username)
	p.showPage()
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response


@login_required
def systemsettings_view(request): 
	# if request.user.is_superuser:
	if not request.user.groups.filter(name='Dispenser').exists():
		try:
			settin = SystemSettings.objects.latest('id')
			form = SystemSettingsForm(instance=settin)
		except:
			form = SystemSettingsForm()
		if request.method == 'POST':
			try:
				settin = SystemSettings.objects.latest('id')
				form = SystemSettingsForm(request.POST,instance=settin)
			except Exception as e:
				form = SystemSettingsForm(request.POST)
				print(e)
			if form.is_valid():
				form.save()
				return redirect('home:systemsettings')
			else:
				print(form.errors)
		return render(request, 'home/settings.html', {'form':form})
	return HttpResponse('<h2>You don\'t have the neccesary pernmissions</h2>')

		
@login_required
def reporting_view(request):
	data_dict = {}
	summ_dict = {}
	if request.method == 'POST':
		form = ReportingForm(request.POST)
		if form.is_valid():
			date_from= form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			sales_data = Sale.objects.filter(date__range=(date_from, date_to))
			for sal in sales_data:
				if sal.medicine not in data_dict:
					data_dict[sal.medicine] = {}
					data_dict[sal.medicine]['qty'] = []
					data_dict[sal.medicine]['qty'].append(int(sal.quantity_sold))
					[(pur_d, sell_d)] = Medicine.objects.filter(name=sal.medicine).values_list('purchase_price','selling_price')
					data_dict[sal.medicine]['purchase'] = pur_d
					data_dict[sal.medicine]['selling'] = sell_d
				else:
					data_dict[sal.medicine]['qty'].append(int(sal.quantity_sold))
					[(pur_d, sell_d)] = Medicine.objects.filter(name=sal.medicine).values_list('purchase_price','selling_price')
					data_dict[sal.medicine]['purchase'] = pur_d
					data_dict[sal.medicine]['selling'] = sell_d
			for item in list(data_dict):
				data_dict[item]['qty'] = sum(data_dict[item]['qty'])
				data_dict[item]['purchase'] = int(data_dict[item]['qty'])*float(data_dict[item]['purchase'])
				data_dict[item]['selling'] = int(data_dict[item]['qty'])*float(data_dict[item]['selling'])
				if not 'sub_sale' in summ_dict:
					summ_dict['sub_sale'] = []
					summ_dict['sub_sale'].append(float(data_dict[item]['selling']))
				else:
					summ_dict['sub_sale'].append(float(data_dict[item]['selling']))
				if not 'sub_purchase' in summ_dict:
					summ_dict['sub_purchase'] = []
					summ_dict['sub_purchase'].append(float(data_dict[item]['purchase']))
				else:
					summ_dict['sub_purchase'].append(float(data_dict[item]['purchase']))
			disc_d = SalesInvoice.objects.filter(date__range=(date_from, date_to)).aggregate(Sum('discount'))
			summ_dict['discount'] = float(disc_d['discount__sum'])
			summ_dict['sub_sale'] = sum(summ_dict['sub_sale'])
			summ_dict['sub_purchase'] = sum(summ_dict['sub_purchase'])
			summ_dict['gross_sale'] = summ_dict['sub_sale'] - summ_dict['discount']

			my_exp = Expense.objects.filter(date__range=(date_from, date_to))
			exp_dict = {}
			for exp in my_exp:
				if not str(ExpenseCategory.objects.get(id=exp.category_id)) in exp_dict:
					exp_dict[str(ExpenseCategory.objects.get(id=exp.category_id))] = []
					exp_dict[str(ExpenseCategory.objects.get(id=exp.category_id))].append(float(exp.amount))
				else:
					exp_dict[str(ExpenseCategory.objects.get(id=exp.category_id))].append(float(exp.amount))

			for item in exp_dict:
				exp_dict[item] = sum(exp_dict[item])

			tot_exp = []
			for value in exp_dict:
				tot_exp.append(exp_dict[value])
			tot_exp = [sum(tot_exp)]

			profit = [summ_dict['gross_sale']-tot_exp[0]-summ_dict['sub_purchase']]

			print(data_dict)

			exp_dict = json.dumps(exp_dict)
			data_dict = json.dumps(data_dict)
			summ_dict = json.dumps(summ_dict)
	else:
		form = ReportingForm
		data_dict = {}
		summ_dict = {}
		exp_dict = {}
		profit = []
		tot_exp = []
	args = {'form':form, 'data_dict':data_dict, 
	'summ_dict':summ_dict, 'exp_dict':exp_dict,
	'tot_exp':tot_exp,'profit':profit}	
	return render(request, 'home/reporting.html', args)


@login_required
def expirealert_view(request):
	now_date = datetime.datetime.now()
	com_date = datetime.datetime.fromtimestamp(time.time()+864000)
	exp_meds = Medicine.objects.filter(expiry_date__lte=com_date).order_by('-id')
	return render(request, 'home/expirealert.html',{'exp_meds':exp_meds})

@login_required
def stockalert_view(request):
	stock_meds = Medicine.objects.filter(quantity_left__lte = 10)
	return render(request, 'home/stockalert.html', {'stock_meds':stock_meds})


























"""
@require_POST
def cart_add(request, medicine_id):
	cart = Cart(request)
	medicine = get_object_or_404(Medicine, id=medicine_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(medicine=medicine, quantity=cd['quantity'],update_quantity=cd['update'])

	return redirect('home:medicine_detail')


def cart_remove(self, medicine_id):
	cart = Cart(request)
	medicine = get_object_or_404(Medicine, id=medicine_id)
	cart.remove(medicine)
	return redirect('home:medicine_detail')


def medicine_detail(request):
	my_meds = Medicine.objects.all()
	cart = Cart(request)
	return render(request, 'home/pos.html', {'cart':cart,'my_meds':my_meds})
"""


















# Create your views here.
