from django.db import models

# Create your models here.

class TranslateTexts(models.Model):
    TYPE_LANGUAGE_CHOICES = [("en","English"), ("fr","Francais"), ("de", "Deutch"), ("zh-Hans","Chinesse")]
    language_code_origin = models.CharField(max_length=2)
    language_code_destiny = models.CharField(max_length=7, choices= TYPE_LANGUAGE_CHOICES)
    text_to_translate = models.CharField(max_length=255)
    text_translated = models.CharField(max_length=255)

    def __str__ (self):
        return 'el texto traducido es %s %s' % (self.language_code_destiny, self.text_translated)

class SentimentTexts(models.Model):
    text_to_analyze = models.CharField(max_length=255)
    result = models.CharField(max_length=255,blank=True,null=True)

    def __str__ (self):
        return 'el texto analizado es %s %s' % (self.text_to_analyze, self.sentiment_result)


