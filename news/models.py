from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    author_rank = models.IntegerField(default=0)

    def update_rating(self):
        for post in self.posts.all():
            self.author_rank += post.post_rank * 3
            for comment in post.comments.all():
                self.author_rank += comment.comment_rank
        for user in self.author.comments.all():
            self.author_rank += user.comment_rank
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=125, unique=True)


class Post(models.Model):
    """
    post_type (article or news) = 0 if its article, 1 if its news
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.BooleanField()
    post_pub_time = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rank = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rank += 1
        self.save()

    def dislike(self):
        self.post_rank -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:125]} ...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    comment_pub_time = models.DateTimeField(auto_now_add=True)
    comment_rank = models.IntegerField(default=0)

    def like(self):
        self.comment_rank += 1
        self.save()

    def dislike(self):
        self.comment_rank -= 1
        self.save()
