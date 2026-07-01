from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Product, Category
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.contrib import messages

class ProductListView(ListView):
   model = Product
   template_name = "catalog/product_list.html"
   context_object_name = "products"
   paginate_by = 4

   def get_queryset(self):
       qs = (Product.objects.filter(is_active=True,stock__gt = 0).select_related("category", "seller")
           .order_by("-created_at"))
       q = self.request.GET.get("q", "").strip()
       if q:
           qs = qs.filter(
               Q(name__icontains=q) |
               Q(short_description__icontains=q) |
               Q(description__icontains=q))
       cat_slug = self.request.GET.get("category", "").strip()
       if cat_slug:
           cat = Category.objects.filter(slug=cat_slug).first()
           if cat:
               child_ids = list(cat.children.values_list("id", flat=True))
               qs = qs.filter(category_id__in=[cat.id] + child_ids)
       min_price = self.request.GET.get("min_price", "").strip()
       max_price = self.request.GET.get("max_price", "").strip()
       try:
           if min_price:
               qs = qs.filter(price__gte=Decimal(min_price))
           if max_price:
               qs = qs.filter(price__lte=Decimal(max_price))
       except InvalidOperation:
           messages.warning(self.request, "Narx maydoniga faqat son kiriting (masalan: 100 yoki 99.99) ⚠️")
       # 4) Sort: sort
       sort = self.request.GET.get("sort", "latest")
       if sort == "price_asc":
           qs = qs.order_by("price")
       elif sort == "price_desc":
           qs = qs.order_by("-price")
       else:
           qs = qs.order_by("-created_at")
       return qs
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Category dropdown uchun categorylar
       context["categories"] = Category.objects.filter(parent__isnull=True).order_by("name")
       # Hozirgi filter qiymatlarini template’ga qaytarish (input’larda saqlash uchun)
       context["q"] = self.request.GET.get("q", "").strip()
       context["category"] = self.request.GET.get("category", "").strip()
       context["min_price"] = self.request.GET.get("min_price", "").strip()
       context["max_price"] = self.request.GET.get("max_price", "").strip()
       context["sort"] = self.request.GET.get("sort", "latest")
       # Pagination bosilganda query yo‘qolmasin: page dan boshqa hammasini saqlaymiz
       params = self.request.GET.copy()
       params.pop("page", None)
       context["querystring"] = params.urlencode()
       return context
   


        
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    