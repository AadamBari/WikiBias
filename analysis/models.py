from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name + ' - ' + self.code


