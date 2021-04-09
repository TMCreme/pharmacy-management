from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
import datetime
import time
from .models import MedicineCategory, Medicine,ExpenseCategory,Expense,Sale,SalesInvoice, SystemSettings
#from .forms import UserLogin

def baseview(request):
	try:
		sys_vars = SystemSettings.objects.latest('id')
		com_date = datetime.datetime.fromtimestamp(time.time()+86400000)
		exp_medds = Medicine.objects.filter(expiry_date__lte=com_date).order_by('-id')
		exp_medds_count = Medicine.objects.filter(expiry_date__lte=com_date).count()
		stock_medds = Medicine.objects.filter(quantity_left__lte = 10)
		stock_medds_count = Medicine.objects.filter(quantity_left__lte = 10).count()
		return {'sys_vars':sys_vars,'exp_medds':exp_medds, 'stock_medds':stock_medds, 'exp_medds_count':exp_medds_count,'stock_medds_count':stock_medds_count}
	except:
		pass
	





