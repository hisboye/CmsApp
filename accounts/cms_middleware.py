from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CmsMiddleware(MiddlewareMixin):
   
    def process_view(self,request,view_func,*args,**kwargs):
        module=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type=='1':
                if module == 'superadmin.views' or module == 'accounts.views' or module == 'django.contrib.auth.views':                    
                    pass
                else:
                    messages.error(request,'You dont have access to this page')
                    return redirect(reverse('dashboard'))

            elif user.user_type == '2':
                if module == 'superadmin.views':
                        messages.error(request,'You dont have access to this Resources')
                        return redirect(reverse('cms'))

            else:
                return redirect(reverse('login'))

        # else:
        #     if module=='superadmin.views' or module == 'user':
        #         messages.error(request,'You need to login ')
        #         return redirect(reverse('login'))

           


                



