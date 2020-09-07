from django.db import models
from django.db.models.aggregates import Count
from django.contrib.auth.models import User, Group
from picklefield.fields import PickledObjectField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.conf import settings
import random
import json
from random import randint, SystemRandom
import numpy as np
from simple_history.models import HistoricalRecords


# Create your models here.
class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200, blank=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.label

    def __str__(self):
        return "%s" % self.label


class OnlineClass(models.Model):
    name = models.CharField(max_length=200, blank=False)
    chapter = models.ManyToManyField(Chapter)
    class_code = models.CharField(unique=True, max_length=200, null=True)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = 'OnlineClasses'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "%s" % self.name


class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prof_class = models.ManyToManyField(OnlineClass)
    assistant = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.user

    def __str__(self):
        return "%s" % self.user


class UserProfile(models.Model):
    PROGRAMMING = (("yes", "Yes"),
                   ("no", "No"))
    STRATEGIES = (("random", "random"),
                  ("eer", "eer"),
                  ("sequential", "sequential"))
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT,
                                  null=True, blank=True)
    programming = models.CharField(max_length=3, choices=PROGRAMMING)
    accepted = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    strategy = models.CharField(max_length=10, choices=STRATEGIES)
    seed = models.CharField(max_length=81)
    user_class = models.ForeignKey(OnlineClass, on_delete=models.PROTECT,
                                   null=True)
    sequential = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return "%s" % self.user


class Cluster(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=50, blank=False)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return "%d - %s" % (self.id, self.label)


class ProblemManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Problem(models.Model):
    QUESTION_TYPES = (("C", "Code"),
                      ("M", "Multiple Choice"),
                      ("T", "Text"))

    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default="C")
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    options = models.TextField(blank=True)
    difficulty = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True)
    retrieved_date = models.DateTimeField(blank=True)
    crawler = models.CharField(max_length=200, blank=True)
    hint = models.TextField(blank=True)
    objects = ProblemManager()
    chapter = models.ManyToManyField(Chapter)
    test_case_generator = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return "%d - %s" % (self.id, self.title)


class Solution(models.Model):
    content = models.TextField(blank=False)
    header = models.TextField(blank=True, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    link = models.URLField(blank=True, null=True)
    retrieved_date = models.DateTimeField(blank=False)
    ignore = models.BooleanField(default=False)
    tip = models.TextField(blank=True,
                           default="#Start your python function here")
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.problem.title

    def __str__(self):
        return self.problem.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    content = models.TextField(blank=False)
    history = HistoricalRecords()


class UserLog(models.Model):
    OUTCOMES = (("F", "Failed"),
                ("P", "Passed"),
                ("S", "Skipped"))
    ERROR_TYPE = (("C", "Conceptual"),
                  ("S", "Syntax"),
                  ("D", "Distraction"),
                  ("I", "Interpretation"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution = models.TextField(blank=True)
    outcome = models.CharField(max_length=2, choices=OUTCOMES)
    console = models.TextField(blank=True)
    seconds_in_code = models.IntegerField()
    seconds_in_page = models.IntegerField()
    seconds_to_begin = models.IntegerField()
    solution_lines = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    error_type = models.CharField(max_length=2, choices=ERROR_TYPE,
                                  default="D")


class UserLogView(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    final_outcome = models.CharField(max_length=2)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False


class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distribution = PickledObjectField()

    def __unicode__(self):
        return self.user

    def __str__(self):
        return "%s" % self.user


@receiver(post_save, sender=User)
def create_user_model(sender, instance, created, **kwargs):
    if created:
        # Create profile
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()

        # Create user model
        model = UserModel()
        model.user = instance
        # TODO: UPDATE!
        # Fixed in number of problems and topics (54 x 3)
        model.distribution = np.zeros(settings.DOC_TOPIC_SHAPE)
        model.save()


@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Generate data for the random fields of UserProfile
        instance.strategy = random.choice(settings.STRATEGIES)
        alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        generator = SystemRandom()
        instance.seed = u''.join(generator.choice(alphabet) for _ in range(81))
        instance.save()


@receiver(post_save, sender=OnlineClass)
def create_class_code(sender, instance, created, **kwargs):
    if created:
        # Generate random string code to identify OnlineClass
        unique_id = get_random_string(length=9)
        instance.class_code = '-'.join([
            unique_id[i:i+3] for i in range(0, len(unique_id), 3)])
        instance.save()


@receiver(post_save, sender=Professor)
def add_professor_group(sender, instance, created, **kwargs):
    group = Group.objects.get(name="Professor")
    instance.user.groups.add(group)
    instance.user.save()


@receiver(post_delete, sender=Professor)
def delete_professor_group(sender, instance, **kwargs):
    group = Group.objects.get(name="Professor")
    instance.user.groups.remove(group)
    instance.user.save()


@receiver(post_save, sender=Problem)
def create_test_cases(sender, instance, created, **kwargs):
    # If generate test case is provided with the Problem, generate and
    # save the test cases
    if instance.test_case_generator is not None and \
            instance.test_case_generator != '':

        # Transform solution into python function
        function_obj = compile(instance.test_case_generator,
                               'generate', 'exec')
        exec(function_obj)

        # Generate test cases
        test_cases = eval('generate')()

        # If valid test cases
        if test_cases:
            # Delete old ones
            old_test_cases = TestCase.objects.filter(problem=instance)
            old_test_cases.delete()

            # Add new ones
            for item in test_cases:
                test_case = TestCase()
                test_case.problem = instance
                test_case.content = json.dumps(item)
                test_case.save()
