from django.contrib import admin
from .models import App, Review

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name','category','rating','installs','reviews_count')
    search_fields = ('name','category','genres')
    ordering = ('-installs',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('short','app','author','status','created_at','supervisor')
    list_filter = ('status','sentiment')
    search_fields = ('text','author__username','app__name')
    actions = ['bulk_approve']

    def short(self, obj):
        return obj.text[:75]
    short.short_description = 'Review'

    def bulk_approve(self, request, queryset):
        from django.utils import timezone
        sup = request.user
        count = 0
        for r in queryset.filter(status='PENDING'):
            r.status='APPROVED'
            r.approved_at = timezone.now()
            r.supervisor = sup
            r.save()
            count += 1
        self.message_user(request, f"Approved {count} reviews.")
    bulk_approve.short_description = "Approve selected pending reviews"
