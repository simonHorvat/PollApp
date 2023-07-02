import json
import random
import os
from datetime import timedelta
import django
from django.utils import timezone

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Configure Django settings
django.setup()

def generate_sample_data(num_polls, max_questions, max_choices, max_answers):
    data = []
    poll_pk, question_pk, question_pk, choice_pk, answer_pk = 1, 1, 1, 1, 1

    for p in range(1, num_polls + 1):
        if p%100 == 0: print(f"pool {p} generated!")
        num_questions_per_poll = random.randint(1, max_questions + 1)
        num_voters_per_poll = random.randint(0, max_answers + 1)
        poll = {
            "model": "polls.poll",
            "pk": poll_pk,
            "fields": {
                "poll_text": f"Sample poll {p}",
                "pub_date": (timezone.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            },
        }
        data.append(poll)
        poll_pk += 1

        for q in range(1, num_questions_per_poll + 1):
            question = {
                "model": "polls.question",
                "pk": question_pk,
                "fields": {
                    "poll": poll_pk - 1,
                    "question_text": f"Sample question {q}",
                },
            }
            data.append(question)
            question_pk += 1

            num_choices = random.randint(2, max_choices)
            for c in range(1, num_choices + 1):
                choice = {
                    "model": "polls.choice",
                    "pk": choice_pk,
                    "fields": {
                        "question": question_pk - 1,
                        "choice_text": f"Choice {c} for question {q}",
                    },
                }
                data.append(choice)
                choice_pk += 1

            # Generate answers for each question
            choice_range = range(choice_pk - num_choices, choice_pk)
            for __ in range(num_voters_per_poll):
                  choice_id = random.choice(choice_range)
                  answer = {
                      "model": "polls.answer",
                      "pk": answer_pk,
                      "fields": {
                          "question": question_pk - 1,
                          "choice": choice_id,
                       },
                  }
                  data.append(answer)
                  answer_pk += 1

    return data


# Generate sample data
sample_data = generate_sample_data(num_polls=500, max_questions=70, max_choices=5, max_answers=50)

# Save the sample_data to a JSON file
with open("sample_data.json", "w") as file:
    json.dump(sample_data, file, indent=4)