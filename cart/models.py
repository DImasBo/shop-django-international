from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('Дата створення'))
    checked_out = models.BooleanField(default=False, verbose_name=_('Оформленна'))
    
    class Meta:
        app_label="cart"
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзини')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


from svetlyachokshop.models import Product

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Корзина'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('кількість'))
    unit_price = models.DecimalField(blank=True, max_digits=18, decimal_places=2, verbose_name=_('Ціна за одиницю'))

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)
    def __str__(self):
        return str(self.product)

    def save(self,*args,**kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args,**kwargs)

    def get_minus_url(self):
        return reverse('minus_to_cart_url',kwargs={"product_id":self.product.id})
    def get_add_url(self):        
        return reverse('add_to_cart_url',kwargs={"product_id":self.product.id})
    class Meta:
        verbose_name = _('Одиниця товару')
        verbose_name_plural = _('Одиниці товару')
        ordering = ('cart',)
