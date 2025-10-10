from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, help_text="It will be displayed as the product name on the card")
    link = models.URLField(help_text="Link to the product page")
    show_for_youtube = models.BooleanField(default=True, verbose_name="Show for YouTube", help_text="If checked, the product will be shown for YouTube domain")
    show_for_tiktok = models.BooleanField(default=True, verbose_name="Show for TikTok", help_text="If checked, the product will be shown for TikTok domain")
    show_for_instagram = models.BooleanField(default=True, verbose_name="Show for Instagram", help_text="If checked, the product will be shown for Instagram domain")
    is_pinned = models.BooleanField(default=False, verbose_name="Pin?", help_text="If checked, the product will be pinned at the top of the list")
    file = models.FileField(upload_to='products/', help_text="Upload a file related to the product (e.g., image, gif)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_pinned',   '-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"