
from django.conf import settings 
from django.shortcuts import render, get_object_or_404
from .models import Items, OrderItem,Order,BillingAddress,Payment
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .forms import CheckoutForm


import stripe
stripe.api_key = settings.STRIPE_SECRETE_KEY


# Create your views here.
Item_global_= ""

def aboutView (request):
    return render(request, 'about.html')


class SearchResultView(ListView):
    model= Items
    template_name = 'search_results.html'


    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Items.objects.filter(Q( title__icontains=query) | Q(description__icontains=query)
        )
        return object_list
    




class HomeListView(ListView):
    model = Items
    paginate_by = 8
    ordering = ['id']
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try: 
            order = Order.objects.get(user = self.request.user, ordered= False)
            context={
                'object': order
            }
            return render(self.request, 'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,'You dont have any active orders')
            return redirect("/")


class ProductDetailView(DetailView):
    model = Items
    context_object_name  = "product"
    # slug_url_kwarg = 'slug'    

    def get_object(self):
        # slug =self.kwargs.get('slug')
        
        item= Items.objects.filter(category=self.kwargs['category_slug']).get(slug=self.kwargs['product_slug'])
        Item_global_ = item
        return item
       

# class ProductDetailView(DetailView):
#     model = Items
    
#     context = {'cart_product_form': cart_product_form}
#     def get_object(self, queryset=None):
#         for topic in Items.objects.all():
#             queryset = topic
#             return topic
            
              
# def productdetail(request,slug):

#     product = Items.objects.get(slug = slug)
#     return render(request, 'product.html', {'product': product})                

   


class  CheckoutPageView(View):
    def get(self,*args, **kwargs):
        form = CheckoutForm()
        context ={
            'form': form
        }
        return render(self.request, "checkout-page.html", context)



    def post(self,*args, **kwargs):
        form = CheckoutForm(self.request.POST or None )
        try: 
            order = Order.objects.get(user = self.request.user, ordered= False)
            if form.is_valid():
                print(form.cleaned_data)
                # print("The form is valid ")
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')

                # TODO: add functionality for these fields 
                # same_billing_address = form.cleaned_data.get('save_billing_address')
                # same_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                apartment_address = form.cleaned_data.get('apartment_address')
                
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address  =  street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()

            # TODO: add a redirect to selected payment 
                if payment_option == 's':
                    return redirect( 'core:payment',payment_option= 'stripe' )
                elif payment_option == 'p':
                    return redirect( 'core:payment',payment_option= 'paypal' )
                else:
                    messages.warning(self.request,"Invalid payemt option ")
                    return redirect( 'core:checkoutpage')
                    
            return redirect('core:checkoutpage')    
            return render(self.request, 'order_summary.html',context)

        except ObjectDoesNotExist:
            messages.error(self.request,'You dont have any active orders')
            return redirect("core:order-summary")
        # print(self.request.POST)
        






@login_required
def add_to_cart(request,slug,):
    # item = get_object_or_404(Items,slug = slug)
    item = Items.objects.filter(slug=slug).first()
    # item = Item_global_
    order_item, _ = OrderItem.objects.get_or_create(item = item)   # A single underscore shows that it insignificant
    order_qs = Order.objects.filter(user= request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1 
            order_item.save() 
            messages.info(request, 'Cart succesfuly updated')
            return redirect("core:order-summary")      

            
        else: 
            order.items.add(order_item)
            messages.info(request, 'Item sucesfuly added')
            return redirect("core:order-summary", slug = slug)      


         

    else: 
        ordered_date = timezone.now()
        order = Order.objects.create(user= request.user, order_date = ordered_date)
        
        order.items.add(order_item)
        messages.info(request, 'Item sucessfuly added')
        return redirect("core:order-summary", slug = slug)      


    return redirect("core:order-summary", slug = slug)      


@login_required
def remove_from_cart(request,slug):
    # item = get_object_or_404(Items,slug = slug)
    item = Items.objects.filter(slug=slug).first()

    # order_item, _ = OrderItem.objects.get_or_create(item = item)   # A single underscore shows that it insignificant
    order_qs = Order.objects.filter(user= request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item= item)[0] 
            
            order.items.remove(order_item)
            messages.info(request, 'Item removed from cart')
            return redirect("core:order-summary") 


        else:
            messages.info(request, 'Item was not in your cart')

            return redirect("core:order-summary", slug = slug) 
            
    else: 
        # ordered_date = timeorder_itemzone.now()
        # order = Order.objects.create(user= request.user, order_date = ordered_date)
        
        messages.info(request, 'You do not have an activate order')

        return redirect("core:product", slug = slug) 
        # order.items.add(order_item)
    return redirect("core:product", slug = slug) 



@login_required
def remove_single_item_from_cart(request,slug):
    # item = get_object_or_404(Items,slug = slug)
    item = Items.objects.filter(slug=slug).first()

    # order_item, _ = OrderItem.objects.get_or_create(item = item)   # A single underscore shows that it insignificant
    order_qs = Order.objects.filter(user= request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item= item)[0] 

            if( order_item.quantity >1):
                order_item.quantity -= 1 
                order_item.save() 
            else:
                order.items.remove(order_item)
            messages.info(request, 'Item quantity reduced ')
            return redirect("core:order-summary") 


        else:
            messages.info(request, 'Item was not in your cart')

            return redirect("core:product", slug = slug) 
            
    else: 
        # ordered_date = timeorder_itemzone.now()
        # order = Order.objects.create(user= request.user, order_date = ordered_date)
        
        messages.info(request, 'You do not have an activate order')

        return redirect("core:product", slug = slug) 
        # order.items.add(order_item)
    return redirect("core:product", slug = slug) 


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user,ordered= False)
        context={
            'order': order
        }
        return render(self.request,"payment.html",context)

    def post(self,*args, **kwargs):

        order = Order.objects.get(user=self.request.user,ordered= False)
        token = self.request.POST.get('stripeToken')
        # print(self.request.POST)
        # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
        amount= int(order.get_total_price() * 100)

        try:
            # Use Stripe's library to make requests...
            
            charge = stripe.Charge.create(
            
            currency="usd",
            source= token,
            description="My First Test Charge (created for API docs)"
            )

            order.ordered= True
        # create payment
            payment = Payment()

            payment.stripe_charge_id =  charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price() 
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            
            # assign payment to the order 
            order.ordered = True 
            order.payment = payment 
            order.save()

            
            
            messages.success(self.request,"Your order was successful")
            
            return redirect("/")
        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request,"Ratelimit error")
            return redirect("/")
            
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request,"Invalid Request error")
            return redirect("/")
            
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request,"Not authenticated")
            return redirect("/")
            
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request,"Network connection error")
            return redirect("/")
            
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Stripe error.You were not charged try again")
            return redirect("/")
            
        except Exception as e:
            # send an email to your seld
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request,"We have been notified. Error!")
            

       




