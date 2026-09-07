from django.shortcuts import render
from .models import Species
from .models import Moves 


def home(request):
    species_count = Species.objects.count()
    return render(request, "home.html", {"species_count": species_count})


def pokemon_table(request):
    species_list = Species.objects.all().order_by("pokedex_id")
    return render(request, "pokemon_table.html", {"species_list": species_list})


def team_builder(request):
    species_list = Species.objects.all().order_by("pokedex_id")
    return render(request, "team_builder.html", {"species_list": species_list})

def Moves(request):
    moves_list = Moves.objects.all().order_by("id")
    return render(request, "moves.html", {"moves_list": moves_list})
