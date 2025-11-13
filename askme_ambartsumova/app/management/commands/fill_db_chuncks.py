from django.core.management.base import BaseCommand, CommandError
from app.models import *
import random

from django.db.models import F



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options[ 'ratio' ]


        #create answer likes

        #AnswerLike.objects.all().delete()

        ANSWERS = Answer.objects.all()

        for answer in ANSWERS:
            answer.likes_count = 0

        print(len(ANSWERS))

        batch_s = 100

        likes_change = ["likes_count" for i in range(batch_s)]

        for i in range( len(ANSWERS) // batch_s ):
            ans_sl = ANSWERS[ i*batch_s : (i+1)*batch_s ]
            Answer.objects.bulk_update(ans_sl, likes_change, batch_size=batch_s)
            print(f"Success updated {i}-s part")