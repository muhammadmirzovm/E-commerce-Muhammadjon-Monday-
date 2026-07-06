from django.contrib.auth.mixins import UserPassesTestMixin

class SellerRequiredMixin(UserPassesTestMixin):
   # Faqat seller kirishi uchun (role == "SELLER")
   def test_func(self):
       user = self.request.user
       return user.is_authenticated and getattr(user, "role", None) == "SELLER"


