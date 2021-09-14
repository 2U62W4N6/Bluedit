from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

# ---------------------------------- Forum Model ------------------------------------- #
class Forum(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    created = models.DateField(default=now, blank=False, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                                related_name='owner',
                                related_query_name='owners')

    FORUM_TYPES = [
        ('F', 'Funny'),
        ('N', 'NSFW'),
        ('E', 'Educational'),
        ('S', 'Sport'),
        ('A', 'Art'),
        ('', '')
    ]

    type = models.CharField(max_length=1,
                            choices=FORUM_TYPES,
                            default=""
                            )


    # Gibt die Anzahl der Subscriber zurück
    def getAboCount(self):
        return len(Abo.objects.filter(forum=self))

    class Meta:
        ordering = ['name']
        verbose_name = 'Forum'
        verbose_name_plural = 'Foren'

# ----------------------------------- Abo Model -------------------------------------- #
class Abo(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='subscriber',
                             related_query_name='subscribers',
                             )
    ROLE_TYPES = [
        ('O', 'Owner'),
        ('A', 'Admin'),
        ('S', 'Supervisor'),
        ('N', 'Normal'),
        ('B', 'Banned')
    ]
    type = models.CharField(max_length=1, choices=ROLE_TYPES, default='N')

    class Meta:
        verbose_name = 'Abo'
        verbose_name_plural = 'Abos'

# ---------------------------------- Post Model -------------------------------------- #
class Post(models.Model):
    title = models.CharField(max_length=300, blank=False)
    text = models.TextField(max_length=5000, blank=True, default='')
    media = models.URLField(default='')
    created = models.DateTimeField(default=now, blank=False, null=False)
    votes = models.IntegerField(default=0, null=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                             related_name='ops',
                             related_query_name='op',
                             )
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    # Gibt die Anzahl der Kommentare zurück 
    def getCommentCount(self):
        return len(Comment.objects.filter(post=self))

    # Updated den Vote-Count 
    def updateVotes(post):
        upvotes = len(PostVote.objects.filter(post=post, value=1))
        downvotes = len(PostVote.objects.filter(post=post, value=0))
        votes = upvotes - downvotes
        Post.objects.filter(id=post.id).update(votes=votes)

# -------------------------------- PostVote Model ------------------------------------ #
class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                             related_name='postvoter',
                             related_query_name='postvoters',
                             )
    value = models.IntegerField(null=False)

    # Prüft ob der User schon gevoted hat
    def contains(user_id, post):
        if PostVote.objects.filter(user=user_id, post=post).exists():
            return True
        else:
            return False

    # Schaut welchen Wert in die Tabelle eingetragen wird
    def vote(user, post_id, vote):
        post = Post.objects.get(id=post_id)
        if PostVote.contains(user, post):
            if PostVote.objects.get(user=user, post=post).value == vote:
                PostVote.objects.get(user=user, post=post).delete()
            else:
                PostVote.objects.filter(user=user, post=post).update(value=vote)
        else:
            PostVote.objects.create(user=user, post=post, value=vote)

    class Meta:
        verbose_name = 'postvote'
        verbose_name_plural = 'postvotes'

# -------------------------------- Comment Model ------------------------------------ #
class Comment(MPTTModel):
    text = models.TextField(max_length=5000, blank=False)
    created = models.DateField(default=now, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0, null=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                             related_name='authors',
                             related_query_name='authors',
                             )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # Updated den Vote-Count 
    def updateVotes(comment_id):
        upvotes = len(CommentVote.objects.filter(comment=comment_id, value=1))
        downvotes = len(CommentVote.objects.filter(comment=comment_id, value=0))
        votes = upvotes - downvotes
        Comment.objects.filter(id=comment_id).update(votes=votes)

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        ordering = ['-created']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


# ------------------------------ CommentVote Model ---------------------------------- #
class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                             related_name='commentvoter',
                             related_query_name='commentvoters',
                             )
    value = models.IntegerField(null=False)

    # Prüft ob der User schon gevoted hat
    def contains(user_id, comment):
        exist = len(CommentVote.objects.filter(user=user_id, comment=comment))
        if exist == 0:
            return False
        else:
            return True

    # Schaut welchen Wert in die Tabelle eingetragen wird
    def vote(user_id, comment_id, vote):
        comment = Comment.objects.get(id=comment_id)

        if CommentVote.contains(user_id, comment):
            if CommentVote.objects.get(user=user_id, comment=comment).value == vote:
                CommentVote.objects.get(user=user_id, comment=comment).delete()
            else:
                CommentVote.objects.filter(user=user_id, comment=comment).update(value=vote)
        else:
            CommentVote.objects.create(user=user_id, comment=comment, value=vote)

    class Meta:
        verbose_name = 'commentvote'
        verbose_name_plural = 'commentvotes'

