from django.db import models

class Project(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    technology = models.CharField(max_length=255, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_url = models.URLField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    preview = models.ImageField(upload_to='previews', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def create_slug(self):
        self.slug = "%s-%s-%s" % (self.date.year, self.date.month, self.name.replace(" ", "-").lower()[:15])
        self.save()

    def filtered_set(self):
        projs = Project.objects.exclude(pk=self.pk)
        categories = Category.objects.filter(project=self)
        return projs.filter(category__in=categories)


    class Meta:
        ordering = ['-date']

    @property
    def category_class(self):
        class_string = ""
        for category in self.category_set.all():
            class_string = class_string + category.slug + " "
        print class_string
        return class_string
    

class Category(models.Model):
    """
    Description: Model Description
    """
    
    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ManyToManyField('Project')
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def create_slug(self):
        self.slug = "%s" % self.name.lower().replace(' ', '-')
        self.save()

    def __unicode__(self):
        return self.name


class VideoCall(models.Model):
    p1_key = models.TextField(null=True, blank=True)
    p2_key = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Video Call created on  %s." % self.created

        