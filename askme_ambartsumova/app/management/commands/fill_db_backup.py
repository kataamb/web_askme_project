from django.core.management.base import BaseCommand, CommandError
from app.models import *
import random

from django.db.models import F


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        '''

        USER_DATA = [User( username=f"username{i}", password=f"password{i}" ) for i in range(ratio)]
        User.objects.bulk_create(USER_DATA)

        #create users (profiles)
        USER_PROFILES = User.objects.all()
        USERS = [ Profile( login=f"login_user{i}", email=f"user{i}@mail.ru",
                           user=USER_PROFILES[i])
                  for i in range( ratio ) ]

        #create tags
        TAGS = [ Tag( name=f"tag{i}" ) for i in range(ratio) ]

        ##############################################
        Profile.objects.bulk_create(USERS)
        Tag.objects.bulk_create(TAGS)

        # create questions

        QUESTIONS = [Question( title = f"Question number {i}", text_body = f"Question text {i}",
                               likes_count = 0)
                     for i in range(ratio * 10)]

        Question.objects.bulk_create(QUESTIONS)


        # create answers
        QUESTIONS = Question.objects.all()
        q_len = len(QUESTIONS)
        ANSWERS = [Answer( text_body = f"This is answer body {i}",
                           question = QUESTIONS[ random.randint(0, q_len-1) ],
                           likes_count = 0) for i in range(ratio * 100 )]

        Answer.objects.bulk_create(ANSWERS)

        '''

        '''
        #create question likes

        QuestionLike.objects.all().delete()


        USERS = Profile.objects.all()
        QUESTIONS = Question.objects.all()
        user_question = set()
        QUESTION_LIKES = []

        UPDATED_QUESTIONS = dict()

        i = 0
        j = 0
        q_len = len(QUESTIONS)
        u_len = len(USERS)
        while ( i < ratio * 100):
            random.seed( j+1 )
            user_id = random.randint(0, u_len) % u_len
            question_id = random.randint(0, q_len) % q_len
            pair = (user_id, question_id)


            if not (pair in user_question):

                user_question.add( pair )

                question = QUESTIONS[question_id]

                if not(question in UPDATED_QUESTIONS):
                    UPDATED_QUESTIONS[question] = 0

                UPDATED_QUESTIONS[question] += 1

                question_like = QuestionLike( user= USERS[user_id], question = QUESTIONS[question_id], value = 1)
                QUESTION_LIKES.append( QuestionLike( user= USERS[user_id], question = QUESTIONS[question_id], value = 1) )

                i+=1

            j+=1

        #add likes
        QuestionLike.objects.bulk_create(QUESTION_LIKES) #!!!!
        #update questions
        UPD_QUESTIONS = []
        for item in UPDATED_QUESTIONS:
            item.likes_count = UPDATED_QUESTIONS[ item ]
            UPD_QUESTIONS.append( item )

        Question.objects.bulk_update(list(set(UPD_QUESTIONS)),
                                     ["likes_count" for i in range(len( UPD_QUESTIONS ) )])

        '''

        # create answer likes

        # AnswerLike.objects.all().delete()

        print("DELETED")

        USERS = Profile.objects.all()
        ANSWERS = Answer.objects.all()
        user_answer = set()
        ANSWER_LIKES = []

        UPDATED_ANSWERS = dict()

        i = 0
        j = 0
        a_len = len(ANSWERS)
        u_len = len(USERS)
        while (i < ratio * 100):
            random.seed(j + 1)
            user_id = random.randint(0, u_len) % u_len
            answer_id = random.randint(0, a_len) % a_len
            pair = (user_id, answer_id)

            if not (pair in user_answer):

                user_answer.add(pair)

                answer = ANSWERS[answer_id]

                if not (answer in UPDATED_ANSWERS):
                    UPDATED_ANSWERS[answer] = 0

                UPDATED_ANSWERS[answer] += 1

                # question_like = QuestionLike( user= USERS[user_id], question = QUESTIONS[question_id], value = 1)
                ANSWER_LIKES.append(AnswerLike(user=USERS[user_id], answer=ANSWERS[answer_id], value=1))

                i += 1

            j += 1

        print("GENERATED")
        # add likes
        # AnswerLike.objects.bulk_create(ANSWER_LIKES) #!!!!
        print("ADDED")
        # update questions
        UPD_ANSWERS = []
        for item in UPDATED_ANSWERS:
            item.likes_count = UPDATED_ANSWERS[item]
            UPD_ANSWERS.append(item)

        UPD_ANSWERS = list(set(UPD_ANSWERS))

        print("LEN UPD_ANSWERS:", len(UPD_ANSWERS))

        likes_change = ["likes_count" for i in range(len(UPD_ANSWERS))]

        # Answer.objects.bulk_update(UPD_ANSWERS,likes_change, 1000)

        print("UPDATED")