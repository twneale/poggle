from django.shortcuts import render
from django.views.generic.base import TemplateView


class GameView(TemplateView):

    template_name = "frontend/game.html"