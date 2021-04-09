from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import MedicineCategory, Medicine,ExpenseCategory,Expense,Sale,SalesInvoice, SystemSettings



class UserLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =['username', 'password']

class MedicineCategoryForm(forms.ModelForm):

	class Meta:
		model = MedicineCategory
		fields = ['category', 'description']

class MedicineForm(forms.ModelForm):
	quantity_left = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	class Meta:
		model = Medicine
		fields = [
		'name','category','purchase_price','selling_price','store_box',
		'quantity', 'generic_name', 'company','side_effects','expiry_date','quantity_left',
		]

class ExpenseCategoryForm(forms.ModelForm):
	class Meta:
		model = ExpenseCategory
		fields = ['category','description']

class ExpenseForm(forms.ModelForm):
	class Meta:
		model = Expense
		fields = ['category','description', 'amount','user']


class SalesInvoiceForm(forms.ModelForm):
	class Meta:
		model = SalesInvoice
		fields = ['sub_total','discount','grand_total', 'user']



class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ['category','medicine','quantity_sold','price','cost']

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField()
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class MedicineQuantityUpdateForm(forms.Form):
	medicine = forms.CharField()
	quantity = forms.IntegerField()


class SystemSettingsForm(forms.ModelForm):
	class Meta:
		model = SystemSettings
		fields = ['name','title','address','phone_number','email','currency']



class ReportingForm(forms.Form):
	date_from = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	date_to = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datepicker'}))












"""
class RegistrationForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'password1',
		'password2',
		'is_service_provider',
		]

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user
"""
