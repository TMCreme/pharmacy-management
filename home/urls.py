from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/home/login/'}, name='logout'),
    path('add_medicine_category/', views.add_medicine_cat, name='add_medicine_category'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_list/', views.medicine_view, name='medicine_list'),
    path('edit-medicine/<int:id>/', views.edit_medicine, name='edit-medicine'),
    path('medicine_category/', views.medicine_cat_view, name='medicine_category'),
    path('edit-medicine-category/<int:id>/', views.edit_medicine_cat, name='edit-medicine-category'),
    path('add_expense_category/', views.add_expense_cat, name='add_expense_category'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_category_view/', views.expense_cat_view, name='expense_category_view'),
    path('edit-expense-category/<int:id>/', views.edit_expense_cat, name='edit-expense-category'),
    path('expenses_view/', views.expense_view, name='expenses_view'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit-expense'),
    #path('medicine_detail/', views.medicine_detail, name='medicine_detail'),
    #path('add/<int:id>/', views.cart_add, name='cart_add'),
    #path('remove/<int:id>/', views.cart_remove, name='cart_remove'),
    path('point-of-sales/', views.pos, name='point-of-sales'),
    path('point-of-sales-submit/', views.pos_submit_view, name='point-of-sales-submit'),
    path('pdf-display', views.pdf_display, name='pdf-display'),
    path('allsales', views.allsales_view, name='allsales'),
    path('financial-reporting/', views.reporting_view, name='financial-reporting'),
    path('expire-alert/', views.expirealert_view, name='expire-alert'),
    path('stock-alert/', views.stockalert_view, name='stock-alert'),
    path('systemsettings/', views.systemsettings_view, name='systemsettings'),

]
