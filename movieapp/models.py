from django.db import models


# Post model
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    caption = models.CharField(max_length=50)
    content = models.TextField()
    likes= models.IntegerField(default = 0)

    def __str__(self):
        return self.caption[:]
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = "comments")
    commenter_name = models.CharField(max_length = 30)
    comment = models.TextField(max_length = 150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} {self.commenter_name} : {self.comment}"
    
    def delete_comment(self):
        self.delete()