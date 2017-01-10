from django.db import models
from django.db import utils 
from django.template.defaultfilters import slugify #section 7.3
from django.contrib.auth.models import User #section 9

from django.db.models.signals import post_save #for custom user profile
from django.dispatch import receiver #for custom user profile

# Create your models here.
class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        views = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        print("slugField = ", models.SlugField)
        slug = models.SlugField()

        def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default =0)

    def __unicode__(self):
        return self.title

class PoeUser(User):
    poe_sessid = models.CharField(max_length = 32, primary_key = True)
        
    def __unicode__(self):
        return self.username
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            try:
                print("ERROR0 ", "type(instance) ", type(instance), "=>", instance)
                PoeUser.objects.create(user=instance)
                print("instance.poeprofile.poe_sessid", instance.poeprofile.poe_sessid)
            except utils.IntegrityError as e:
                print ("ERROR2 poe_sessid ", instance.poeprofile.poe_sessid)
            try:
                instance.poeprofile.save()
            except AttributeError as e:
                print("ERROR3 ", "type(ssesid) ", type(instance), "=>", instance)
                pass
            except utils.IntegrityError as e:
                #print (" poe_sessid ", instance.poeprofile.poe_sessid)
                print("ERROR2 ", e, instance.poeprofile.poe_sessid) #ß, poe_sessid)

