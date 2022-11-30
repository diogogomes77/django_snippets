from random import choice
from drm import models
from drm.management.commands.base import CreateDataBaseCommand
from drm.models import Attachment, License, Organization, Role
import factory
from faker import Faker
import datetime

fake = Faker()


def get_random_policy():
    pks = models.Policy.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    random_object = models.Policy.objects.get(pk=random_pk)
    return random_object


class Command(CreateDataBaseCommand):

    help = "Add policies"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        model_classes = [Organization, License, Role]
        for model_class in model_classes:
            self.stdout.write(f"Adding {self.number} policies to {model_class} ...")

            for obj in model_class.objects.all():

                for n in range(1, self.number):
                    done = False
                    while not done:
                        policy = get_random_policy()
                        print("policy: ", policy)
                        try:
                            obj.attachments.create(policy=policy)
                            done = True
                            # attachment = Attachment.objects.create(entity=obj, )
                        except Exception as e:
                            print("Exception: ", e)
