from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db import DatabaseError

import requests
from requests.exceptions import RequestException
import logging

from .models import Poll, Question, Choice, Answer


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(settings.LOG_FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by("-pub_date")[:settings.NUM_INDEX_POLLS]


class QuestionListView(generic.ListView):
    template_name = 'polls/question_list.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        poll_id = self.kwargs['pk']
        return Question.objects.filter(poll_id=poll_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poll"] = Poll.objects.get(pk=self.kwargs['pk'])  # Get the poll object using the pk from the URL
        return context


class ResultsView(generic.DetailView):
    model = Poll
    template_name = "polls/results.html"

    def dispatch(self, request, *args, **kwargs):
        # Apply the cache_page decorator to the dispatch method
        return cache_page(settings.CACHE_SECONDS)(super().dispatch)(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Get the Poll object
            poll = self.object
        except DatabaseError as e:
            logger.error(f"Database related error: {str(e)}")
            raise 
        
        # Fetch the total attendees using the API endpoint
        attendees_url = f"{settings.API_BASE_URL}/polls/{poll.id}/attendees"
        try:
            attendees_response = requests.get(attendees_url)
            attendees_response.raise_for_status()  # Raise an exception for non-2xx status codes
            total_attendees = attendees_response.json().get('total_attendees')
            context['total_attendees'] = total_attendees
        except RequestException as e:
            # Handle any request errors (e.g., connection error, timeout)
            logger.error(f"Error fetching total attendees: {e}")
            context['total_attendees'] = None

        # Fetch the choice statistics using the API endpoint
        choice_statistics_url = f"{settings.API_BASE_URL}/polls/{poll.id}/choice_statistics"
        try:
            choice_statistics_response = requests.get(choice_statistics_url)
            choice_statistics_response.raise_for_status()  # Raise an exception for non-2xx status codes
            question_votes = choice_statistics_response.json().get('question_votes')
            context['question_votes'] = question_votes
        except RequestException as e:
            # Handle any request errors (e.g., connection error, timeout)
            logger.error(f"Error fetching choice statistics: {e}")
            context['question_votes'] = None

        return context     


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        for question in poll.question_set.all():
            choice_id = request.POST.get(f"choice{question.id}")
            selected_choice = question.choice_set.get(pk=choice_id)
            answer = Answer(question=question, choice=selected_choice)
            answer.save()
            
        # Invalidate the cache for poll results
        cache.delete(f"views.decorators.cache.cache_page.{request.path_info}")

    # Error handling
    except (KeyError, Question.DoesNotExist, Choice.DoesNotExist):
        return render(
            request,
            "polls/question_list.html",
            {
                "poll": poll,
                "question_list": poll.question_set.all(),
                "error_message": "Invalid choice selection.",
            },
        )
    return HttpResponseRedirect(reverse("polls:results", args=(poll.id,)))