from django.contrib import admin
from .models import Hall, Seance, Order, Movie, Ticket
from django.utils.html import mark_safe


# Register your models here.
class HallAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'row_count', 'place_count')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="120" height="120"')

    get_image.short_description = "Изображение"


class SeanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'movie', 'hall_id')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'description', 'age_limit')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="120" height="120"')

    get_image.short_description = "Изображение"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'ticket', 'customer')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('row_number', 'place_number', 'status', 'seance', )


admin.site.register(Hall, HallAdmin)
admin.site.register(Seance, SeanceAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Ticket, TicketAdmin)
