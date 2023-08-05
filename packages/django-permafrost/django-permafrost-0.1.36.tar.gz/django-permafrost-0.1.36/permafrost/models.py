from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.managers import CurrentSiteManager

from jsonfield import JSONField     # Using this instead of the PSQL one for portability


###############
# CHOICES
###############

# CATEGORIES = getAttr(settings, "PERMAFROST_CATEGORIES", {})
# CATEGORY_CHOICES = getAttr(settings, "PERMAFROST_CATEGORY_CHOICES", [])

###############
# UTILITIES
###############

def lable_from_choice_value(choices, value):
    return [x[1] for x in choices if x[0] == value][0]

def make_iterable(value):
    '''
    Takes whatever is passed in and tries to return it as a list
    '''
    if isinstance(value, list):
        return value

    if isinstance(value, models.query.QuerySet):
        return value

    if not value:
        return []

    return [value]

def get_permission_models(permissions):
    return [ permission_from_string(p) for p in make_iterable(permissions) ]

def permission_from_string(permission):
    values = permission.split(".")
    return Permission.objects.get(codename=values[1], content_type__app_label=values[0])

def get_current_site(*args, **kwargs):
    return settings.SITE_ID


###############
# MANAGERS
###############

class CategoryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class PermafrostRoleManager(models.Manager):
    def get_by_natural_key(self, slug, site):
        return self.get(slug=slug, site=site)


###############
# MODELS
###############

class PermafrostCategory(models.Model):
    '''
    This holds the list of permissions that are available to be configured
    in the given category.  It contains both the "permissions", which are
    client configurable and the "includes" which are always included.

    TODO: Need to add localization support

    The permissions are kept in a JSON formatted list in the following structure:
    [
        {"perm":"permafrost.add_permafrostrole", "label":"Can add Permafrost Role"},
        {"perm":"permafrost.update_permafrostrole", "label":"Can update Permafrost Role"}
    ]

    They provide the ability to have a lables that are more human readable.

    The includes are kept in a JSON formatted list in the following structure:
    [
        "permafrost.view_permafrostrole",
        "permafrost.update_permafrostrole"
    ]

    As they are always present in a role of that Category Type, they don't 
    have a lable and are just a simple string list.

    Lists, rather than foreign keys, are used because there is no garuntee
    that a migration will not break the relationships.  Since this is rarely
    accessed, it is probably OK to take the DB hit to query this way.
    '''

    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), blank=True, null=True)
    level = models.IntegerField(_("Security Level"), default=1)     # Scale 1-100, low to high security role category.
    permissions = JSONField(default=list, blank=True)
    includes = JSONField(default=list, blank=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Permafrost Category")
        verbose_name_plural = _("Permafrost Categories")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        result = super().save(*args, **kwargs)
        return result

    def get_include_models(self):
        return [ permission_from_string(permission) for permission in self.includes ]


class PermafrostRole(models.Model):
    '''
    PermafrostRole is Client Defineable and "manages" a Django Group adding a
    user to this role adds them to the Django Group and automatically assignes
    them the permissions.
    '''
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"))
    # category = models.CharField(_("Category"), choices=CATEGORY_CHOICES)                                  # Should probably switch back to having configurable permissions be included in the code, better for consistency and security
    category = models.ForeignKey(PermafrostCategory, verbose_name=_("Category"), on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=get_current_site)                      # This uses a callable so it will not trigger a migration with the projects it's included in
    locked = models.BooleanField(_("Locked"), default=False)                                                        # If this is locked, it can not be edited by the Client, used for System Default Roles
    deleted = models.BooleanField(_("Deleted"), default=False, help_text="Soft Delete the Role")
    group = models.ForeignKey(Group, verbose_name=_("Group"), on_delete=models.CASCADE, related_name="permafrost_role", blank=True, null=True)                  # NOTE: Need to make sure this is exported with natural key values as it can have a different PK on different servers

    objects = PermafrostRoleManager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Permafrost Role")
        verbose_name_plural = _("Permafrost Roles")
        unique_together = [['name', 'site']]

        permissions = (
            ("add_user_to_role", "Can Add Users to Role"),
            ("add_user_to_administration", "Can Add Users to the Administration Roles"),
        )

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug, self.site)

    #-------------
    # Permissions

    def available(self):
        '''
        TODO!!!
        Based on the list of permissions in the Category, compile a list of all
        that are available.
        '''
        pass

    def conform_group(self):
        '''
        TODO!!!
        Based on the list of permissions in the Category, make sure the group
        has the right set.  Make sure no permissions are outside of the
        optional and required and that all required permissions are added.
        '''
        available = self.available()

    def group_name_schema(self, site, category, slug):
        return "{0}_{1}_{2}".format( site.pk, category.slug, slug)

    def get_group_name(self):
        return self.group_name_schema(self.site, self.category, self.slug)
    
    def permissions(self):
        return self.group.permissions

    def permissions_add(self, permissions):
        '''
        Add permissions to the attached group by name "app.perm"
        '''
        for p in get_permission_models(permissions):
            self.group.permissions.add(p)

    def permissions_remove(self, permissions):
        '''
        Remove permissions from the attached group by name "app.perm"
        '''
        for p in get_permission_models(permissions):
            self.group.permissions.remove(p)

    def permissions_set(self, permissions):
        '''
        This updates the group permissions to only include what was passed in by name "app.perm"
        '''
        self.group.permissions.set( get_permission_models(permissions) )

    def permissions_clear(self):
        '''
        Remove all permissions from the group except the defaults.
        '''
        if self.category.includes:
            self.group.permissions.set( self.category.includes )
        else:
            self.group.permissions.clear()

    #-------------
    # Users

    def user_set(self):
        '''
        Wrapper around the group that returns a queryset of all the user 
        included in this role.
        '''
        return self.group.user_set.all()


    def users_add(self, users=None):
        '''
        Pass in a User object to add to the PermafrostRole
        '''
        for user in make_iterable(users):
            user.groups.add(self.group)

    def users_remove(self, users=None):
        '''
        Pass in a User object to remove from the PermafrostRole
        '''
        for user in make_iterable(users):
            user.groups.remove(self.group)

    def users_clear(self):
        '''
        Remove all users from the PermafrostRole
        '''
        self.group.clear()

    #-------------
    # Save

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        group_name = self.get_group_name()

        if not self.pk:                                                             # if this is a new role, create the matching group
            self.group, created = Group.objects.get_or_create(name=group_name)      # Add the group if one named correctly alreay exists, otherwise create a new one.
        
        result = super().save(*args, **kwargs)

        if self.group.name != group_name:                                           # if the role is renamed after successful save, update the group's name
            self.group.name = group_name
            self.group.save()

        self.conform_group()                            # Apply after a successful save

        return result
