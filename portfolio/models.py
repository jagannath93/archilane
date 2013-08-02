from django.db import models
from django.contrib.auth.models import User
class Portfolio(models.Model):
	owner = models.ForeignKey(User, related_name = "portfolio_owner")  
	likes = models.IntegerField(max_length=5, default=0)  # Need to change to data type double in future max_length restricted to 5.

class PortfolioMarkedUsers(models.Model):
	portfolio = models.ForeignKey(Portfolio, related_name = "portfolio_pointer")		
	user = models.ForeignKey(User, related_name = "liked_users_list")
	token = models.BooleanField() # whether this user liked/unliked this Portfolio.

class PortfolioGroup(models.Model):
	title = models.CharField(max_length=30)
	desc = models.TextField()
	owner = models.ForeignKey(User, related_name = "group_owner")
	recordlistingID = models.IntegerField(max_length=4) # max_length restricted to 4.

	class Meta:
		ordering = ['recordlistingID']

class PortfolioItem(models.Model):
	content = models.TextField()
	group = models.ForeignKey(PortfolioGroup, on_delete = models.CASCADE, related_name="item_group")
	recordlistingID = models.IntegerField(max_length=4)
	has_image = models.IntegerField(max_length=1, default=0)
	image_path = models.CharField(max_length=20)  
	likes = models.IntegerField(max_length=5, default=0)   # Need to change the datatype and it's max limit.

	class Meta:
		ordering = ['recordlistingID']	

class ItemMarkedUsers(models.Model):
	item = models.ForeignKey(PortfolioItem, related_name = "pitem")
	user = models.ForeignKey(User, related_name = "ILU")
	token = models.BooleanField()
'''
class Picture(models.Model):

    # This is a small demo using just two fields. The slug field is really not
    # necessary, but makes the code simpler. ImageField depends on PIL or
    # pillow (where Pillow is easily installable in a virtualenv. If you have
    # problems installing pillow, use a more generic FileField instead.

    #file = models.FileField(upload_to="pictures")
    file = models.ImageField(upload_to="portfolio/")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)#class PortfolioImages(model.Model):
#	image = models.ImageField()
'''

