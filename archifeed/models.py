from django.db import models

class ArchiFeed(models.Model):
  title = models.CharField(max_length=100)
  des = models.TextField()
  has_image = models.BooleanField()
  image_path = models.CharField(max_length=70)
  #item = models.TextField()
  pub_date = models.CharField(max_length=10)
  channel = models.CharField(max_length=20)
  source = models.CharField(max_length=30)
  link = models.CharField(max_length=200)
  
  def __unicode__(self):
     return self.title
'''
class related_news(models.Model):
  item = models.ManyToManyField(news_feeds)
  main_item = models.ForeignKey(news_feeds, related_name="main_items")
  related_items = models.ForeignKey(news_feeds, related_name="related_names") '''
