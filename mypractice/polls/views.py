from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question

# Create your views here.

def home(request):
    return HttpResponseRedirect("polls/")

def index(request):
    question_list = Question.objects.order_by("-pub_date")
    context = {"question_list" : question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question" : question}
    return render(request, "polls/detail.html", context)
    