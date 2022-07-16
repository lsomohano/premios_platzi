import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        #Cambie la suma por la resta para que la publicacion se publique al pasado
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)#tiene que retornar false

    def test_was_published_recently_with_now_question(self):
        #Simulamos que la publiación se acaba depublicar
        time = timezone.now()
        future_question = Question("¿Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)#Tiene que devolver true 