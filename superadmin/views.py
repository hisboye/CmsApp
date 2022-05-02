from django.shortcuts import render
from accounts.models import *
from accounts.decorators import *
from django.contrib.auth.decorators import login_required
from accounts.forms import Create_Order
from accounts.filters import *
from django.forms import inlineformset_factory


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    customer=Customer.objects.all()
    orders=Order.objects.all()
    total_order=orders.count()
    customers=customer.count()
    orders_deliver=orders.filter(status='Delivered').count()
    orders_pending=orders.filter(status='Pending').count()

    context={
        'customer':customer,
        'orders':orders,
        'total_order':total_order,
        'customers':customers,
        'orders_deliver':orders_deliver,
        'orders_pending':orders_pending
    }
    
    return render(request,'dashboard.html',context)

def customer(request,pk_id):
    try:
        customer=Customer.objects.get(id=pk_id)
        orders=customer.order_set.all()      #what does it do
        total_orders=orders.count()
        myFilter=OrderFilter(request.GET,queryset=orders)
        orders=myFilter.qs
    except:
        customer={}
        orders={}
        myFilter={}
        total_orders=""

    context={
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter,
    }
    
    
    return render(request,'customer.html',context)

@login_required(login_url='login')
def product(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'products.html',context)

@login_required(login_url='login')
def orderform(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=2)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(instance=customer)
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
       
    context={
        'formset':formset
    }
    return render(request,'orderform.html',context)

@login_required(login_url='login')
def updates(request,pk):
    order=Order.objects.get(id=pk)  
    form=Create_Order(instance=order)
    if request.method=='POST':
        form=Create_Order(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')


    context={
        'form':form

    }
    return render(request,'orderform.html',context)

@login_required(login_url='login')
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={
        'item':order
    }
    return render(request,'delete.html',context)