
from django.core.management.base import BaseCommand
import random

from advertisements.models import Advertisement
from accounts.models import MyCustomUser

# at this will be generation of moderated Advertisements
class Command(BaseCommand):
    def handle(self, *args, **options):
        users = MyCustomUser.objects.all().values_list("id", flat=True)
        rand_user = random.choice(users)
        rend_price = random.randrange(270, 350)

        for ads in range(1000):
            Advertisement.objects.create(
                title="iPhone",
                description="Some description about",
                category_equipment='iPhone',
                price=rend_price,
                is_visible = True,
                is_moderated = True,
                author=MyCustomUser.objects.get(pk=rand_user),
                # main_image="advertisement/f9eaf973-5585-4aa7-82b3-222ed2122e22.jpg"
                                       )
