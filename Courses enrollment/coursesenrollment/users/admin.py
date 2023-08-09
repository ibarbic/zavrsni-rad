from django.contrib import admin
from users.models import *

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Post)
