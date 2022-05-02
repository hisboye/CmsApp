from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomerForm

from accounts.forms import CustomUserForm

# Create your views here.

@login_required(login_url='login')
def cms(request):
    try:
        order=request.user.customer.order_set.all()
        total_order=order.count()
        orders_deliver=order.filter(status='Delivered').count()
        orders_pending=order.filter(status='Pending').count()
    except:
        order={}
        total_order=''
        orders_deliver=''
        orders_pending=''

    context={
        'order':order,
        'total_order':total_order,
        'orders_deliver':orders_deliver,
        'orders_pending':orders_pending
    }
    return render(request,"cms.html",context)



@login_required(login_url='login')
def accountsettings(request):
    try:
        customer=request.user.customer          # Who is the Customer
    except:
        customer={}
    print(customer)
    form=CustomerForm(instance=customer)
    if request.method == "POST":
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={
        'form':form

    }
    return render(request,'account.html',context)