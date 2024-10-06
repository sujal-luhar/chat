from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]

        """
        Return the last five published questions
        (Not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        # request.POST["choice"] -> 5 (the value of selected radio button)
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select the choice",
            },
        )
    
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # reverse("polls:results", args=(question.id,)) -> "/polls/3/results/"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# from django.db.models import F
# from django.shortcuts import render, get_object_or_404
# from django.urls import reverse

# # Create your views here.
# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader

# from .models import Question, Choice

# # def index(request):
# #     latest_question_list = Question.objects.order_by("-pub_date")[:5]
# #     template = loader.get_template("polls/index.html")
# #     context = {
# #         "latest_question_list": latest_question_list
# #     }
# #     return HttpResponse(template.render(context, request))

# def index(request):
#     """
#     The shortcut
#     """
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = { "latest_question_list": latest_question_list }
#     return render(request, "polls/index.html", context)

# # def detail(request, question_id):
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist!")
# #     return render(request, "polls/detail.html", {"question": question})

# def detail(request, question_id):
#     question = get_object_or_404(Question , pk=question_id)
#     return render(request, "polls/detail.html", {"question": question}) 

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})
