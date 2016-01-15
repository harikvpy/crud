import random
import datetime
import logging

from django.core.management.base import BaseCommand, CommandError
from polls.models import *

# some random questions, taken from
# http://www.cfcl.com/vlb/Memes/Questionaires/random_1.html
QUESTIONS = [
        "Grab the book nearest to you, turn to page 18, and find line 4.",
        "Stretch your left arm out as far as you can, What can you touch?",
        "Before you started this survey, what were you doing?",
        "What is the last thing you watched on TV?",
        "Without looking, guess what time it is",
        "Now look at the clock. What is the actual time?",
        "With the exception of the computer, what can you hear?",
        "When did you last step outside? What were you doing?",
        "Did you dream last night?",
        "Do you remember your dreams?",
        "When did you last laugh?",
        "Do you remember why / at what?",
        "What is on the walls of the room you are in?",
        "Seen anything weird lately?",
        "What do you think of this quiz?",
        "What is the last film you saw?",
        "If you could live anywhere in the world, where would you live?",
        "If you became a multi-millionaire overnight, what would you buy?",
        "Tell me something about you that most people don't know.",
        "If you could change one thing about the world, regardless of guilt or politics, what would you do?",
        "Do you like to dance?",
        "Would you ever consider living abroad?",
        "Does your name make any interesting anagrams?",
        "Who made the last incoming call on your phone?",
        "What is the last thing you downloaded onto your computer?",
        "Last time you swam in a pool?",
        "Type of music you like most?",
        "Type of music you dislike most?",
        "Are you listening to music right now?",
        "What color is your bedroom carpet?",
        "If you could change something about your home, without worry about expense or mess, what would you do?",
        "What was the last thing you bought?",
        "Have you ever ridden on a motorbike?",
        "Would you go bungee jumping or sky diving?",
        "Do you have a garden?",
        "Do you really know all the words to your national anthem?",
        "What is the first thing you think of when you wake up in the morning?",
        "If you could eat lunch with one famous person, who would it be?",
        "Who sent the last text message you received?",
        "Which store would you choose to max out your credit card?",
        ]

AUTHORS = [
        "Ramachandra Guha",
        "Chetan Bagat",
        "Catherine Lim",
        "VS Naipaul",
        "LKY",
        "Michael Chriton",
        "Louis Lamour",
        "Ian Fleming",
        "Arundati Roy",
        "Sugatha Kumari",
        "OMV Kurup",
        "Rajan Pothanikkad",
        "MT Vasudevan Nair",
        "Ezhuthachan",
        "Kumaran Aasaan",
        ]

class Command(BaseCommand):
    help = "Loads the test app 'polls' with Author and Question records for testing."

    def add_arguments(self, parser):
        # optional argument specifying number of authors & questions
        parser.add_argument('--authors',
                dest='authors',
                type=int,
                action='store',
                default=20,
                help="Number of author records to create, defaults to 20")

        parser.add_argument('--questions',
                dest='questions',
                type=int,
                action='store',
                default=50,
                help="Number of question records to create, defaults to 50")

    def handle(self, *args, **options):
        try:
            # remove all records for Author and Question tables
            Author.objects.all().delete()
            Question.objects.all().delete()

            no_of_authors = options.get('authors', 20)
            no_of_questions = options.get('questions', 50)

            logging.getLogger("general").info(
                    "Creating %d authors, %d questions" %
                    (no_of_authors, no_of_questions))

            # init random no generator
            random.seed()

            # create author objects
            authors = []
            for index in range(0, no_of_authors):
                authname = AUTHORS[random.randint(1, len(AUTHORS)-1)]
                logging.getLogger("general").info("Creating author %d: %s" %
                    (index, authname))
                authors.append(Author.objects.create(
                    name=authname))

            qlen = len(QUESTIONS)
            authlen = len(authors)
            # create 1000 Questions
            for index in range(0, no_of_questions):
                qtext = QUESTIONS[random.randint(0, qlen-1)]
                logging.getLogger("general").info("Creating question %d: %s" % (index, qtext))
                question = Question.objects.create(
                        question_text=qtext,
                        pub_date=datetime.datetime.now(),
                        author=authors[random.randint(0, authlen-1)])

            logging.getLogger("general").info("Created test records -- %d authors, %d questions!" %
                    (no_of_authors, no_of_questions))
        except Exception:
            logging.getLogger("general").error("Exception while creating test data")
            pass

