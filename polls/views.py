from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

class IndexView(generic.ListView):
    def get_queryset(self):
        """
            Return the last five published questions (not including those set
            to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay form
        return render(
            request,
            'polls/detail.html',
            {
                'question' : question,
                'error_message' : "Please select a choice",
            }
        )
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # prevent multiple post's by redirecting back to details page
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))