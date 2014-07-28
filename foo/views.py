from django.shortcuts import render_to_response, Http404
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django import forms
from django.utils.html import escape
from pyke_test.foo.models import Taxon
from pyke import knowledge_engine
import pyke_test.knowledge_base
from pyke_test.ask_django import DjangoAskModule, DjangoAsyncInterrupt
import datetime
import itertools
import re 

# Views

def get_species_choices():
    choices = []
    taxa = Taxon.objects.all()
    for taxon in taxa:
        choices.append((taxon.id, taxon.__unicode__()))
    return choices

class PickSpeciesForm(forms.Form):
    species=forms.MultipleChoiceField(choices=get_species_choices())

def pick_species(request):
    request.session.clear()
    if request.method == 'POST':
        # Form has been submitted
        form = PickSpeciesForm(request.POST)
        if form.is_valid():
            species = []
            for sp_id in form.cleaned_data["species"]:
                species.append(Taxon.objects.get(id=sp_id))
            request.session["species"] = species
            return HttpResponseRedirect("../pick_form")
        else:
            raise Http404("Invalid post request")
    else:
        form = PickSpeciesForm()
        return render_to_response("foo/simple_form.html",
                    { "form": form,
                      "title": "Species Selector",
                      "heading": "Select Specimen Species" })

def display_plan(request, plan, last_review):
    return HttpResponse("<html>%s<p>%s</html>" % (last_review, escape(repr(plan[0]["summary"]))))

def pick_form(request):
    engine = knowledge_engine.engine(
                (None, "pyke_test.knowledge_base.compiled_krb")
                )
    ask = DjangoAskModule(engine, request.session)
    engine.ask_module = ask
    #  engine.activate("q_test")
    engine.activate("permits")
    engine.load_question_cache(request.session.get("q_cache", {}))
    if request.method == "POST":
        if not ask.record_answer(request.POST):
            form = ask.getForm()
            return render_to_response("foo/simple_form.html",
                    {"form": form,
                        "title": "Identify Required Permits",
                        "heading": "Answer the questions to identify the required permits"})
    
    # Read last review message, if there is one.
    if request.session.has_key("last_review"):
        last_review = request.session["last_review"]
        del request.session["last_review"]
    else:
        last_review = None

    try:
        plan = engine.prove_1_goal("permits.actions_require_summary($specieslist, $summary)",
                            specieslist=request.session["species"])
        request.session["q_cache"] = engine.get_question_cache()
        return display_plan(request, plan, last_review)
    except DjangoAsyncInterrupt:
        request.session["q_cache"] = engine.get_question_cache()
        form = ask.getForm()
        return render_to_response("foo/simple_form.html",
                {
                    "form": form,
                    "title": "Identify Required Permits",
                    "heading": "Answer the questions to identify the required permits",
                     "intro_txt": last_review})


