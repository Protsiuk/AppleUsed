# from django.db import models
# from django.db.models import Q
# from appleused_project import settings
# from advertisements.models import Advertisement
# # Create your models here.
#
#
# class SearchManager(models.Manager):
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query is not None:
#             or_lookup = (Q(title__icontains=query) |
#                          Q(description__icontains=query)|
#                          Q(id__icontains=query)
#                         )
#             qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
#         return qs
#
#
# class ObjectSearch(models.Model):
#     # object_search = models.ForeignKey(Advertisement)
#     object_search = models.ForeignKey(settings.OBJECT_SEARCH)
#
#     objects = SearchManager()
