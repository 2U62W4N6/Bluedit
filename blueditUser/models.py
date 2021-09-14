from django.db import models
from datetime import datetime
from django.utils.timezone import now
from subBluedit.models import Post, Comment
from django.contrib.auth.models import AbstractUser

class BlueditUser(AbstractUser):

    # User-Klasse wird erweitert
    profilePicture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png', blank=True, null=True)
    create = models.DateField(default=now, blank=False, null=False)
    bio = models.TextField(default="", max_length=5000, blank=True)
    bewertung = models.IntegerField(default=0, null=False)
    post_votes = models.IntegerField(default=0)
    comment_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def update_votes(user):
        allPost = Post.objects.filter(creator=user)
        postVotes = 0
        for post in allPost:
            postVotes = postVotes + post.votes

        allComment = Comment.objects.filter(creator=user)
        commentVotes = 0
        for comment in allComment:
            commentVotes = commentVotes + comment.votes


        BlueditUser.objects.filter(id=user.id).update(post_votes=postVotes)
        BlueditUser.objects.filter(id=user.id).update(comment_votes=commentVotes)

