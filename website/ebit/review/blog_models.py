import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class BlogArticlePost(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=120)
    publish_date = models.DateField()
    slug = models.SlugField(null=True, unique=True)

    description1 = models.TextField(default=None, null=True, blank=True)
    desc_image_url1 = models.CharField(null=True, blank=True, max_length=300)

    description2 = models.TextField(default=None, null=True, blank=True)
    desc_image_url2 = models.CharField(null=True, blank=True, max_length=300)

    description3 = models.TextField(default=None, null=True, blank=True)
    desc_image_url3 = models.CharField(null=True, blank=True, max_length=300)

    description4 = models.TextField(default=None, null=True, blank=True)
    desc_image_url4 = models.CharField(null=True, blank=True, max_length=300)

    # Images
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)
    banner_image_url = models.CharField(null=True, blank=True, max_length=300)

    likes = models.IntegerField(default=0)

    blogger_details = models.TextField(default=None, null=True, blank=True)
    blogger_name = models.CharField(max_length=120, null=True, blank=True)
    blogger_image = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse("blog_article", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, self.publish_date)
        super(BlogArticlePost, self).save(*args, **kwargs)


class BlogEventPost(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=120)
    publish_date = models.DateField()
    venue = models.CharField(max_length=500)

    slug = models.SlugField(null=True, unique=True)

    description1 = models.TextField(default=None, null=True, blank=True)
    desc_image_url1 = models.CharField(null=True, blank=True, max_length=300)

    description2 = models.TextField(default=None, null=True, blank=True)
    desc_image_url2 = models.CharField(null=True, blank=True, max_length=300)

    description3 = models.TextField(default=None, null=True, blank=True)
    desc_image_url3 = models.CharField(null=True, blank=True, max_length=300)

    # Images
    thumbnailImage_url = models.CharField(null=True, blank=True, max_length=300)
    bannerImage_url = models.CharField(null=True, blank=True, max_length=300)

    organiser_name = models.CharField(max_length=120, null=True, blank=True)
    organiser_profile = models.TextField(default=None, null=True, blank=True)

    program_name1 = models.CharField(max_length=200, null=True, blank=True)
    program_time1 = models.TimeField(default=None, null=True, blank=True)
    program_name2 = models.CharField(max_length=200, null=True, blank=True)
    program2_time2 = models.TimeField(default=None, null=True, blank=True)
    program_name3 = models.CharField(max_length=200, null=True, blank=True)
    program_time3 = models.TimeField(default=None, null=True, blank=True)

    suitableFor = models.CharField(null=True, max_length=100)
    fees = models.IntegerField(default=None, null=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return "%s->%s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse("blog_event", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, self.date)
        super(BlogEventPost, self).save(*args, **kwargs)


class BlogInterviewPost(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=120)
    publish_date = models.DateField()
    venue = models.CharField(max_length=500)

    slug = models.SlugField(null=True, unique=True)

    introduction = models.TextField(default=None, null=True, blank=True)

    interviewee_name1 = models.CharField(max_length=120, default=None, null=True, blank=True)
    interviewee_profile1 = models.TextField(default=None, null=True, blank=True)
    interviewee_image1 = models.CharField(null=True, blank=True, max_length=300)

    interviewer_name2 = models.CharField(max_length=120, default=None, null=True, blank=True)
    interviewer_profile2 = models.TextField(default=None, null=True, blank=True)
    interviewee_image2 = models.CharField(null=True, blank=True, max_length=300)

    question1 = models.TextField(default=None, null=True, blank=True)
    response1 = models.TextField(default=None, null=True, blank=True)
    question2 = models.TextField(default=None, null=True, blank=True)
    response2 = models.TextField(default=None, null=True, blank=True)
    question3 = models.TextField(default=None, null=True, blank=True)
    response3 = models.TextField(default=None, null=True, blank=True)
    question4 = models.TextField(default=None, null=True, blank=True)
    response4 = models.TextField(default=None, null=True, blank=True)
    question5 = models.TextField(default=None, null=True, blank=True)
    response5 = models.TextField(default=None, null=True, blank=True)

    conclusion = models.TextField(default=None, null=True, blank=True)

    likes = models.IntegerField(default=0)

    def __str__(self):
        return "%s->%s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse("blog_interview", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, self.date)
        super(BlogInterviewPost, self).save(*args, **kwargs)

