from django.contrib import admin
from .models import Player


# Define a custom action to reset mu and sigma to defaults
def reset_mu_sigma(modeladmin, request, queryset):
    queryset.update(mu=25.0, sigma=8.33)  # Reset to default values
    modeladmin.message_user(request, "Selected players' mu and sigma have been reset to defaults.")


reset_mu_sigma.short_description = "Reset selected players' mu and sigma to defaults"


# Register the Player model
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mu', 'sigma', 'rank', 'avatar')
    search_fields = ('name',)
    list_filter = ('mu', 'sigma',)

    # Add the reset action
    actions = [reset_mu_sigma]

    # Fields to display and edit in the player form
    fields = ['name', 'avatar', 'mu', 'sigma', 'rank']

    # Enable file upload for the avatar
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['avatar'].widget.attrs['accept'] = 'image/*'  # Limit to image files for avatars
        return form
