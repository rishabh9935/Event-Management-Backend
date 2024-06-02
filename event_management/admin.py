from django.contrib import admin
from .models import CustomUser, Event, Role, RoleManagement, Donor, DonorManagement, Auction, AccessAttempt


class EventTypeFilter(admin.SimpleListFilter):
    title = 'Event Type'
    parameter_name = 'is_raffle'

    def lookups(self, request, model_admin):
        return (
            (True, 'Raffle'),
            (False, 'Non-Raffle'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_raffle=self.value())
        return queryset

class IsPrivateFilter(admin.SimpleListFilter):
    title = 'Visibility'
    parameter_name = 'is_private'

    def lookups(self, request, model_admin):
        return (
            (True, 'Private'),
            (False, 'Public'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_private=self.value())
        return queryset

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_private', 'is_raffle')
    list_filter = ('date', EventTypeFilter, IsPrivateFilter)
    search_fields = ('name', 'location', 'description', 'details')
    list_editable = ('is_private',)

admin.site.register(Event, EventAdmin)



admin.site.register(CustomUser)
# admin.site.register(Event)
admin.site.register(Role)
admin.site.register(RoleManagement)
admin.site.register(DonorManagement)
admin.site.register(Donor)
admin.site.register(Auction)
admin.site.register(AccessAttempt)


