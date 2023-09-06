from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    userRating = models.IntegerField(default=0)

    def __str__(self):
        return self.authorUser.username
    def update_rating(self):
        self.userRating = 0
        # Рейтинг всех постов автора
        postRat = self.post_set.aggregate(postRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postRating')

        # Рейтинг всех комментариев автора
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        # Рейтинг всех комментариев поста автора
        postComments = self.post_set.annotate()
        pcRat = 0
        for i in postComments:
            postCommentRat = i.comment_set.aggregate(postCommentRating=Sum('commentRating'))
            pcRat += postCommentRat.get('postCommentRating')

        self.userRating += pRat * 3 + cRat + pcRat
        self.save()

class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.categoryName

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

    def __str__(self):
        return f'Пост "{self.postTitle}" от {self.author.authorUser.username}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()


    def preview(self):
        return self.postText[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.categoryName

class UserCategory(models.Model):
    userUC = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryUC = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.categoryUC.categoryName

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    dateCreate = models.DateTimeField(auto_now_add=True)
    commentRating = models.IntegerField(default=0)

    def __str__(self):
        return f'Комментарий к посту "{self.post.postTitle}" от {self.user.username}'
    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
