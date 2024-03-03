from django.db import models
from django.urls import reverse
from    ckeditor.fields import RichTextField

# Post model
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    images = models.ImageField(null= True, blank=True, upload_to= "images/")
    caption = models.CharField(max_length=50)
    content = RichTextField(blank=True,null= True)
    likes= models.IntegerField(default = 0)

    def __str__(self):
        return self.caption[:]
    
    def get_absolute_url(self):
        return reverse("home")
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = "comments")
    commenter_name = models.CharField(max_length = 30)
    comment = models.TextField(max_length = 150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} {self.commenter_name} : {self.comment}"
    
    def delete_comment(self):
        self.delete()