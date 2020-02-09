from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Promise
from .models import Family
from .models import User


admin.site.register(Promise)
admin.site.register(Family)
admin.site.register(User, UserAdmin)
