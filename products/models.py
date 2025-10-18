from django.db import models
from django.utils import timezone


class Product(models.Model):
    title = models.CharField(max_length=255, help_text="It will be displayed as the product name on the card")
    link = models.URLField(help_text="Link to the product page")
    show_for_youtube = models.BooleanField(default=True, verbose_name="Show for YouTube", help_text="If checked, the product will be shown for YouTube domain")
    show_for_tiktok = models.BooleanField(default=True, verbose_name="Show for TikTok", help_text="If checked, the product will be shown for TikTok domain")
    show_for_instagram = models.BooleanField(default=True, verbose_name="Show for Instagram", help_text="If checked, the product will be shown for Instagram domain")
    is_pinned = models.BooleanField(default=False, verbose_name="Pin?", help_text="If checked, the product will be pinned at the top of the list")
    file = models.FileField(upload_to='products/', help_text="Upload a file related to the product (e.g., image, gif)")
    order = models.FloatField(verbose_name="Order", help_text="The order of the product", null=True, blank=True)
    published_at = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="Published At", help_text="The date and time when the product was published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_pinned', 'order', '-published_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if self.order is None:
            last_product = Product.objects.order_by('-order').first()
            self.order = (last_product.order + 1) if last_product else 1
        super().save(*args, **kwargs)