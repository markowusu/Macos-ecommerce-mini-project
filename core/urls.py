from django.urls import path
# from .views import item_list 
from . import views


app_name = 'core'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='item_list'),
     path('product-page/<category_slug>/<product_slug>/', views.ProductDetailView.as_view(), name='items-detail'),
     path('checkout-page/',views.CheckoutPageView.as_view(), name="checkoutpage" ),
     path('order-summary/<slug>/',views.OrderSummaryView.as_view(), name='order-summary' ),
     path('search_results/',views.SearchResultView.as_view(), name='search_results' ),
     path('about',views.aboutView, name='about' ),

     path('order-summary/',views.OrderSummaryView.as_view(), name='order-summary' ),
     path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
     path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
     path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
     path('payment/<payment_option>/',views.PaymentView.as_view(),name="payment")
 ]
 