from django.core.management.base import BaseCommand, CommandError
from app.models import *
import random

from django.db.models import F


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        AnswerLike.objects.all().delete()
        QuestionLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        print("Database cleaned successfully")

        USER_DATA = [User( username=f"username{i}", password=f"password{i}" ) for i in range(ratio)]
        #User.objects.bulk_create(USER_DATA)
        batch_s = 100
        for i in range(len(USER_DATA) // batch_s):
            qs_sl = USER_DATA[i * batch_s: (i + 1) * batch_s]
            User.objects.bulk_create(qs_sl)
            #print(f"Success added {i}-s part users")
        print("ADDED USERS")

        #create users (profiles)

        USER_PROFILES = User.objects.all()
        print(ratio, len(USER_PROFILES))
        USERS = [ Profile( login=f"login_user{i}", email=f"user{i}@mail.ru",
                           user=USER_PROFILES[i])
                  for i in range( ratio ) ]

        #create tags
        TAGS = [ Tag( name=f"tag{i}" ) for i in range(ratio) ]

        ##############################################
        #Profile.objects.bulk_create(USERS)
        batch_s = 100
        for i in range(len(USERS) // batch_s):
            qs_sl = USERS[i * batch_s: (i + 1) * batch_s]
            Profile.objects.bulk_create(qs_sl)
            print(f"Success added {i}-s part profiles")
        print("ADDED Profiles")


        #Tag.objects.bulk_create(TAGS)
        batch_s = 100
        for i in range(len(TAGS) // batch_s):
            qs_sl = TAGS[i * batch_s: (i + 1) * batch_s]
            Tag.objects.bulk_create(qs_sl)
            print(f"Success added {i}-s part TAGS")
        print("ADDED TAGS")

        # create questions
        PROFILES = Profile.objects.all()

        QUESTIONS = [Question( title = f"Question number {i}", text_body = f"Question text {i}",
                               likes_count = 0, user = PROFILES[i % len(PROFILES)])
                     for i in range(ratio * 10)]

        #Question.objects.bulk_create(QUESTIONS)
        batch_s = 100
        for i in range(len(QUESTIONS) // batch_s):
            qs_sl = QUESTIONS[i * batch_s: (i + 1) * batch_s]
            Question.objects.bulk_create(qs_sl)
            print(f"Success added {i}-s part QUESTIONS")
        print("ADDED QUESTIONS")


        # create answers
        QUESTIONS = Question.objects.all()
        q_len = len(QUESTIONS)

        PROFILES = Profile.objects.all()
        ANSWERS = [Answer( text_body = f"This is answer body {i}",
                           question = QUESTIONS[ random.randint(0, q_len-1) ],
                           likes_count = 0, user = PROFILES[i % len(PROFILES)]) for i in range(ratio * 100 )]

        #Answer.objects.bulk_create(ANSWERS)
        batch_s = 100
        for i in range(len(ANSWERS) // batch_s):
            qs_sl = ANSWERS[i * batch_s: (i + 1) * batch_s]
            Answer.objects.bulk_create(qs_sl)
            #print(f"Success added {i}-s part ANSWERS")
        print("ADDED ANSWERS")




        #create question likes

        #QuestionLike.objects.all().delete()

        #print("DELETED")


        USERS = Profile.objects.all()
        QUESTIONS = Question.objects.all()

        print("QUESTINS", len(QUESTIONS))
        user_question = set()
        QUESTION_LIKES = []

        UPDATED_QUESTIONS = dict()

        i = 0
        j = 0
        q_len = len(QUESTIONS)
        u_len = len(USERS)
        while ( i < ratio * 200):
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


        # add likes
        # AnswerLike.objects.bulk_create(ANSWER_LIKES) #!!!!
        batch_s = 100
        for i in range(len(QUESTION_LIKES) // batch_s):
            qs_sl = QUESTION_LIKES[i * batch_s: (i + 1) * batch_s]
            QuestionLike.objects.bulk_create(qs_sl)
            #print(f"Success added {i}-s part QUESTION_LIKES")
        print("ADDED QUESTION_LIKES")


        #update questions
        UPD_QUESTIONS = []
        for item in UPDATED_QUESTIONS:
            item.likes_count = UPDATED_QUESTIONS[ item ]
            UPD_QUESTIONS.append( item )

        # !!! batching
        batch_s = 100

        likes_change = ["likes_count" for i in range(batch_s)]

        for i in range(len(QUESTIONS) // batch_s):
            qs_sl = UPD_QUESTIONS[i * batch_s: (i + 1) * batch_s]
            Question.objects.bulk_update(qs_sl, likes_change, batch_size=batch_s)
            print(f"Success updated {i}-s part QUESTIONS")





        # create answer likes

        #AnswerLike.objects.all().delete()

        #print("DELETED")

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

                ANSWER_LIKES.append(AnswerLike(user=USERS[user_id], answer=ANSWERS[answer_id], value=1))

                i += 1

            j += 1

        print("GENERATED")
        # add likes
        #AnswerLike.objects.bulk_create(ANSWER_LIKES) #!!!!
        batch_s = 100
        for i in range(len(ANSWER_LIKES) // batch_s):
            ans_sl = ANSWER_LIKES[i * batch_s: (i + 1) * batch_s]
            AnswerLike.objects.bulk_create(ans_sl)
            print(f"Success added {i}-s part ANSWER_LIKES")
        print("ADDED ANSWER_LIKES")
        # update questions
        UPD_ANSWERS = []
        for item in UPDATED_ANSWERS:
            item.likes_count = UPDATED_ANSWERS[item]
            UPD_ANSWERS.append(item)

        UPD_ANSWERS = list(set(UPD_ANSWERS))

        print("LEN UPD_ANSWERS:", len(UPD_ANSWERS))


        #!!! batching
        batch_s = 100

        likes_change = ["likes_count" for i in range(batch_s)]

        for i in range(len(ANSWERS) // batch_s):
            ans_sl = UPD_ANSWERS[i * batch_s: (i + 1) * batch_s]
            Answer.objects.bulk_update(ans_sl, likes_change, batch_size=batch_s)
            print(f"Success updated {i}-s part ANSWERS")


        # Answer.objects.bulk_update(UPD_ANSWERS,likes_change, 1000)

        print("UPDATED ANSWERS")



        #TAGS AND QUESTIONS UPDATE

        TAGS = Tag.objects.all()

        QUESTIONS = Question.objects.all()

        print(QUESTIONS[56].title, QUESTIONS[56].likes_count)


        print(len(QUESTIONS))

        for i in range(len(QUESTIONS)):
            lenn = len(TAGS) - 1
            tags = [  TAGS[i % lenn], TAGS[(i+1) % lenn], TAGS[(i+2) % lenn] ]
            QUESTIONS[ i ].tags.add(*tags)
            print(f"Sucess update {i} question", tags)

        #batch_s = 100

        #tags_change = ["tags" for i in range(batch_s)]

        #for i in range(len(QUESTIONS) // batch_s):
         #   q_sl = QUESTIONS[i * batch_s: (i + 1) * batch_s]
          #  Question.objects.bulk_update(q_sl, tags_change, batch_size=batch_s)
           # print(f"Success updated {i}-s part")








