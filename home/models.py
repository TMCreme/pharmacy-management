from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

"""
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250,db_index=True)
	phone_number = models.IntegerField(default=0)
	designation = models.CharField(max_length=300, default='', blank=True)
	profile_picture = models.ImageField(blank=True, null=True)

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
"""
class MedicineCategory(models.Model):
	category = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, db_index=True)
	description = models.TextField()

	class Meta:
		ordering = ('category',)
		verbose_name = 'medicinecategory'
		verbose_name_plural = 'medicinecategories'

	def __str__(self):
		return self.category


class Medicine(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=250, db_index=True)
	category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250, db_index=True)
	purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
	selling_price = models.DecimalField(max_digits=10, decimal_places=2)
	store_box = models.CharField(max_length=250)
	quantity = models.PositiveIntegerField()
	generic_name = models.CharField(max_length=250)
	company = models.CharField(max_length=250)
	side_effects = models.CharField(max_length=250)
	expiry_date = models.DateTimeField(null=True)
	quantity_left = models.IntegerField(null=True)

	class Meta:
		index_together = (('id', 'slug'))

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home:medicine_detail', args=[self.id, self.slug])


class ExpenseCategory(models.Model):
	category = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, db_index=True, unique=True)
	description = models.TextField()

	class Meta:
		verbose_name_plural = 'expensecategories'

	def __str__(self):
		return self.category


class Expense(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250, db_index=True)
	description = models.TextField()
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.category.category

	def get_absolute_url(self):
		return reverse('home:category', args=[self.slug])


class SalesInvoice(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	sub_total = models.DecimalField(max_digits=10, decimal_places=2)
	discount = models.DecimalField(max_digits=10, decimal_places=2)
	grand_total = models.DecimalField(max_digits=10, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return "{:06d}".format(self.id)

class Sale(models.Model):
	invoice_id = models.CharField(max_length=250, db_index=True)
	date = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=250)
	medicine = models.CharField(max_length=250)
	quantity_sold = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	cost = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.medicine



class SystemSettings(models.Model):
	name = models.CharField(max_length=500, db_index=True)
	title = models.CharField(max_length=500, db_index=True)
	address = models.CharField(max_length=500)
	phone_number = models.CharField(max_length=100)
	email = models.EmailField()
	currency = models.CharField(max_length=100)

	def __str__(self):
		return self.name
































# Create your models here.
