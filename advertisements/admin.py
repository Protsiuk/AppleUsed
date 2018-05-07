from django.contrib import admin
from advertisements.models import Advertisement

# from solo.admin import SingletonModelAdmin
# from config.models import SiteConfiguration

# Register your models here.
# admin.site.register(Advertisement)

# admin.site.register(SiteConfiguration, SingletonModelAdmin)
#


@admin.register(Advertisement)
class AdminAdvertisement(admin.ModelAdmin):
    list_display = ['title', 'price', 'author']
    # сортування за замовчуванням -додання на сайт, або можна задати своє сортування
    # тут по ціні -від найбільшого до найменшого
    ordering = ["-price"] #['name'] по імені


# # There is only one item in the table, you can get it this way:
# from .models import SiteConfiguration
# config = SiteConfiguration.objects.get()
#
# # get_solo will create the item if it does not already exist
# config = SiteConfiguration.get_solo()