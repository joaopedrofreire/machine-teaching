from django.db import models
from django.db.models.aggregates import Count
from random import randint

# Create your models here.
class ProblemManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

class Problem(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    difficulty = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=False)
    retrieved_date = models.DateTimeField(blank=False)
    crawler = models.CharField(max_length=200, blank=True)
    hint = models.TextField(blank=True)
    objects = ProblemManager()

    def __unicode__(self):
        return self.title

class Solution(models.Model):
    content = models.TextField(blank=False)
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    link = models.URLField(blank=False)
    retrieved_date = models.DateTimeField(blank=False)
    ignore = models.BooleanField(default=False)