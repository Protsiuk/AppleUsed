"""
Custom signals sent during the creation and updated ads.
"""

from django.dispatch import Signal


# A new user has registered.
# user_registered = Signal(providing_args=["user", "request"])
#
# # A user has activated his or her account.
# user_activated = Signal(providing_args=["user", "request"])

# A new ad has created.
ad_created = Signal(providing_args=["user", "advertisement", "request"])
