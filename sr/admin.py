from django.contrib import admin

from .models import Girl, GirlRank, GirlComment, Stream


admin.site.register(Girl)
admin.site.register(GirlRank)
admin.site.register(GirlComment)
admin.site.register(Stream)
