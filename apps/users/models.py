from django.contrib.auth.models import AbstractUser
from django.db import models


# this model defines system roles used for access control
class Role(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name
    
# this model defines what a role is allowed to do in a specific context
class RolePermission(models.Model):

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    # link permission to a context
    context = models.ForeignKey(
        'contexts.Context',
        on_delete=models.CASCADE,
        related_name='role_permissions'
    )

    # indicates if the role can resolve identity in this context
    can_resolve_identity = models.BooleanField(default=False)

    # stores when the permission was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ensure one permission per role per context
        unique_together = ('role', 'context')

        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"

    def __str__(self):
        # return readable representation of permission
        return f"{self.role.name} → {self.context.name} ({self.can_resolve_identity})"



# this model defines which contexts are available for each role
class RoleContext(models.Model):

    # link role to context
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_contexts'
    )

    # link context to role
    context = models.ForeignKey(
        'contexts.Context',
        on_delete=models.CASCADE,
        related_name='role_contexts'
    )

    # stores when the mapping was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ensure one mapping per role per context
        unique_together = ('role', 'context')

        verbose_name = "Role Context"
        verbose_name_plural = "Role Contexts"

    def __str__(self):
        # return readable mapping
        return f"{self.role.name} → {self.context.name}"
    


# this is the custom user model used in the system
class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True
    )

    # unique identifier for users which is auto-generated based on role
    student_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Official student ID"
    )

    # indicates if user is verified
    is_verified = models.BooleanField(default=False)

    # stores when the user was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        # return username
        return self.username

    # auto-generate student_id based on role
    def save(self, *args, **kwargs):

        # generate id only if it does not exist and user has a role
        if not self.student_id and self.role:
            prefix_map = {
                "Student": "STD",
                "Lecturer": "LEC",
                "Registry Officer": "REG",
                "Admin System": "ADM"
            }

            # get prefix based on role
            prefix = prefix_map.get(self.role.name, "USR")

            # get last user with same prefix
            last_user = User.objects.filter(
                student_id__startswith=prefix
            ).order_by('-id').first()

            # generate next number
            if last_user and last_user.student_id:
                last_number = int(last_user.student_id.replace(prefix, ""))
                new_number = last_number + 1
            else:
                new_number = 1000

            # assign new generated id
            self.student_id = f"{prefix}{new_number}"

        # save user normally
        super().save(*args, **kwargs)