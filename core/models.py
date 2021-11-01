from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image
from io import BytesIO
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
# Create your models here.

CATEGORY_CHOICES= (
    ('S','Shirt'),
    ('Sw','ShirtWeater'),
    ('Ow','Outwear')
)

LABEL_CHOICES =(
    ('p','primary'),
    ('S','secondary'),
    ('D','danger')

)


class Category(models.Model):
    
    name = models.CharField( max_length=255)
    slug = models.SlugField(max_length = 255, unique = True)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
        ordering = ("-name", )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Items(models.Model):
    title = models.CharField( max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank= True, null=True)
    description = models.TextField(null=True)
    brand = models.CharField(max_length=50,null=True)
    sku = models.CharField(max_length=50)
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag')

    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    # label = models.CharField(choices= LABEL_CHOICES, max_length=2)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,null= True) 
    quantity = models.IntegerField(default=1)
    # image = models.ImageField(blank=True, null=True )
    image = models.ImageField(upload_to='uploads/', blank =True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank = True, null= True)
    image_url = models.URLField( max_length=200,blank=True,null=True)
    product_content = models.TextField(blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # return reverse("core:items-detail", kwargs={'category_slug': (self.category.slug.replace("/", "-").lower()).replace(",",""), 'product_slug': (self.slug.replace("/", "-").lower()).replace(",","")})
        # return reverse("core:product", kwargs={'id': (self.id)})
        return f'/{self.category.id}/{self.slug}/'


    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})


    def remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})     
         
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url 
        return None

    def get_thumbnail_image(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' +   self.thumbnail.url 
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image) 
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url 
            else :
                return None

    def make_thumbnail(self,image ,size=(300,200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG', quality=85)

        thumbnail = File(thumb_io,name=image.name)

        return thumbnail

# This gets the imageurl and then saves the image inthe local diretory before display from the local 
# directory not the website. 
# This code does the files saving automatically when the image url is added 
    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}", File(img_temp))
        super(Items, self).save(*args, **kwargs)  

class OrderItem(models.Model):
    
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price


    def get_total_item_price(self):
        return self.quantity * self.item.price   


    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price() 

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_item_price()           



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default= False) 
    start_date = models.DateTimeField( auto_now=True, )
    order_date = models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    billing_address = models.ForeignKey("BillingAddress",on_delete=models.SET_NULL, null=True, blank=True )
    payment = models.ForeignKey("Payment",on_delete=models.SET_NULL, null=True, blank=True )
    def __str__(self):
        return self.user.username       


    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField( max_length=100)
    apartment_address = models.CharField( max_length=100)
    country = CountryField(multiple= False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.SET_NULL, blank=True, null= True )
    amount = models.FloatField()
    timestamp = models.DateField( auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.user.username