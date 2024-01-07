from django.db import models

# Create your models here.

class Thesis(models.Model):
    
    
    title = models.CharField(max_length=500)
    abstract = models.CharField(max_length=5000)
    page_no = models.IntegerField()
    write_date = models.DateField(blank=True, null=True)
    sub_date = models.DateField(auto_now_add=True, blank=True, null=True)
    
    author = models.ForeignKey("account.User", on_delete=models.DO_NOTHING, related_name="author", db_constraint=False)
    supervisor = models.ForeignKey("account.User", on_delete=models.DO_NOTHING, related_name="supervisor", db_constraint=False)
    cosupervisor = models.ForeignKey("account.User", on_delete=models.DO_NOTHING, related_name="cosupervisor", blank=True, null=True, db_constraint=False)
    institute = models.ForeignKey("panel.Institute", on_delete=models.DO_NOTHING, db_constraint=False)
    type = models.ForeignKey("panel.Type", on_delete=models.DO_NOTHING, db_constraint=False)
    language = models.ForeignKey("panel.Language", on_delete=models.DO_NOTHING, db_constraint=False)
    
    subjects = models.ManyToManyField("panel.Subject", blank=True, null=True)
    keywords = models.ManyToManyField("panel.Keyword", blank=True, null=True)
    

class University(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name

class Institute(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey("panel.University", on_delete=models.DO_NOTHING, db_constraint=False)
    
    def __str__(self):
        return self.university.name + " / " + self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    heading = models.CharField(max_length=255)
    
    def __str__(self):
        return self.heading

class Keyword(models.Model):
    description = models.CharField(max_length=50)