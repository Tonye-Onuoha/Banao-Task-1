from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Category(models.Model):
    """Model representing a Category Model"""

    name = models.CharField(max_length=50, help_text="Enter a category")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        """String representation of a category"""

        return f"{self.name}"


class Post(models.Model):
    """Model representing a Blog Post Model"""

    title = models.CharField(max_length=50, help_text="Enter a title for the post")
    image = models.ImageField(upload_to="blog_images")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField(
        max_length=300, help_text="Enter a brief description of the post"
    )
    content = models.TextField(
        max_length=1000, help_text="Enter the content of the post"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False, null=False, blank=True)

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    def __str__(self):
        """String representation of a post"""

        return f"{self.title}"
