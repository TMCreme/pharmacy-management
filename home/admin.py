from django.contrib import admin
from .models import Sale, SalesInvoice, Expense, ExpenseCategory, Medicine, MedicineCategory


class ExpenseAdmin(admin.ModelAdmin):
	list_display = ['date','category','amount']


admin.site.register(Sale)
admin.site.register(SalesInvoice)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseCategory)
admin.site.register(Medicine)
admin.site.register(MedicineCategory)



# Register your models here.
