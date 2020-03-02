import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
        helper to create questions
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text,
        pub_date=time
    )

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
            Display message if no questions exist.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        """
            Questions with a pub_date in the past are displayed on the index
            page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
            Questions with a pub_date in the future aren't displayed on the
            index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(
            response,
            "No polls are available."
        )
        self.assertQuerysetEqual(
            response.context['question_list'], []
        )

    def test_future_question_and_past_question(self):
        """
            Display only past question if both are present.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
            Display more than one quesions from the past.
        """
        create_question(question_text="Past1", days=-30)
        create_question(question_text="Past2", days=-60)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            [
                '<Question: Past1>',
                '<Question: Past2>',
            ]
        )

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(
            future_question.was_published_recently(),
            False
        )
    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(
            old_question.was_published_recently(),
            False
        )
    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently() returns True for questions whose pub_date
            is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(
            recent_question.was_published_recently(),
            True
        )