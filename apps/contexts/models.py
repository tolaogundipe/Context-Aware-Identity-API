from django.db import models

# this model represents a system or environment where identity is used
# for example, learning portal, registry, student portal, library system, etc
class Context(models.Model):

    # name of the context 
    name = models.CharField(
        max_length=150,
        unique=True
    )

    # optional description of the context
    description = models.TextField(
        blank=True
    )

    # indicates whether the context is active or not
    is_active = models.BooleanField(
        default=True
    )

    # stores when the context was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # order contexts alphabetically by name
        ordering = ['name']

        # name shown in django admin
        verbose_name = "Context"

        # plural name shown in django admin
        verbose_name_plural = "Contexts"

    def __str__(self):
        # return the name of the context for display
        return self.name