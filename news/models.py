from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    userRating = models.IntegerField(default=0)
    def update_rating(self):
        # Рейтинг всех постов автора
        postRat = self.post_set.all().aggregate(postRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postRating')

        # Рейтинг всех комментариев автора
        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        # # Рейтинг всех комментариев поста
        # postCommentRat = self.authorUser.post.comment_set.all().aggregate(postCommentRating=Sum('commentRating'))
        # pcRat = 0
        # pcRat += postCommentRat.get('postCommentRating')

        self.userRating += pRat * 3 + cRat
        self.save()

class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NW'
    CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]
    choice = models.CharField(max_length=2, choices=CHOICES, default=ARTICLE)
    createDate = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=255)
    postText = models.TextField()
    postRating = models.IntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()
    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.postRating[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    dateCreate = models.DateTimeField()
    commentRating = models.IntegerField()

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
