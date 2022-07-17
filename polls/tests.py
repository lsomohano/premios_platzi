import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question
# Create your tests here.

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    #Challenge
    def test_was_published_recently_with_past_question(self):
        #Cambie la suma por la resta para que la publicacion se publique al pasado
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)#tiene que retornar false
    
    #Challenge
    def test_was_published_recently_with_now_question(self):
        #Simulamos que la publiación se acaba depublicar
        time = timezone.now()
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)#Tiene que devolver true 


def create_question(question_text, days):
    """
    Create a question wtih the given "question_text", and published thi given
    number of days offset to now (negative fiorquestions published in the past,
    positive for questions thant have yet to be published )
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return  Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_questions(self):
        """
        Quetions with  a pub_date in the future aren't displayed on the index page
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[]) 

    def test_past_questions(self):
        """
        Quetions with  a pub_date in the past are displayed on the index page
        """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context["latest_question_list"],['<Question: Past question>']) 

    def test_future_question_and_past_question(self):
        """
        Even if both  past and future question exist, only past questions are displayed
        """
        past_question = create_question("Past question", -30)
        future_question = create_question("Future question", +30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], ['<Question: Past question>'])

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        past_question1 = create_question("Past question 1", -30)
        past_question2 = create_question("Past question 2", -35)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], ['<Question: Past question 1>', '<Question: Past question 2>'])

    #Challenge
    def test_no_questions_future(self):
        """ Verifica que no se publiqen preguntas del futuro """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(1,"¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        future_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

class QuestionDetailViewsTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the ffuture
        returns a 404 error no found
        """
        future_question = create_question("Future question", +30)
        url = reverse("polls:detail",args=(future_question.id,))    
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        display the question's text
        """
        past_question = create_question("Past question", -30)
        url = reverse("polls:detail",args=(past_question.id,))    
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)