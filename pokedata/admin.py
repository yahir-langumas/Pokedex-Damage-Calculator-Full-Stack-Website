from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms 
from django.db import models 
from .models import Species
from .models import Moves
from .models import Learnset
from .models import Type

# Must use python manage.py makemigrations in the python terminal every time you make a change to any database model. 
# After that use python manage.py migrate to apply the changes to the database. 

# Use a custom admin form for the all model to display the JSONField in a more user-friendly way.
class SpeciesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": forms.Textarea(attrs={"rows": 20, "cols": 80})},
    }
    readonly_fields = ["formatted_types", "formatted_stats"]
    fields = ["name", "pokedex_id", "height", "weight", "base_experience", "formatted_types", "abilities", "formatted_stats", "total_stats", "sprite"]

    def formatted_types(self, obj):
        return ", ".join(obj.types)

    def formatted_stats(self, obj):
        return ", ".join(f"{stat}: {value}" for stat, value in obj.stats.items())

admin.site.register(Species, SpeciesAdmin)

class MovesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": forms.Textarea(attrs={"rows": 20, "cols": 80})},
    }
admin.site.register(Moves, MovesAdmin)

class LearnsetAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": forms.Textarea(attrs={"rows": 20, "cols": 80})},
    }
    readonly_fields = ["formatted_moves"]
    fields = ["name", "formatted_moves", "species_id"]

    def formatted_moves(self, obj):
        return ", ".join(obj.moves)

admin.site.register(Learnset, LearnsetAdmin)

class TypeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": forms.Textarea(attrs={"rows": 20, "cols": 80})},
    }
    readonly_fields = ["formatted_type_data"]
    fields = ["name", "formatted_type_data"]

    def formatted_type_data(self, obj):
        lines = [f"{relation}: {', '.join(values) if values else 'none'}" for relation, values in obj.type_data.items()]
        return mark_safe("<br>".join(lines))

admin.site.register(Type, TypeAdmin)