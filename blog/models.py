import datetime
import re

from django.db import models
from django.utils.text import slugify

class UniqueVisitor(models.Model):
    session_id = models.CharField(null=True, blank=True, max_length=255)
    post = models.ForeignKey('Post', null=True, blank=True)
    number_of_hits = models.PositiveIntegerField(default=0)

    date_visited = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "visited post %s on %s" % (self.post, self.date_visited)


class PostManager(models.Manager):
    def published_visible_posts(self, include_intro=False):
        extra = self.get_queryset().filter(slug='intro') if include_intro else self.get_queryset().filter(pk=0)
        return (self.get_queryset().filter(
            published=True,
            posted__lte=datetime.datetime.today()
        ) | extra ).order_by('-posted') 


class Post(models.Model):
    published = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    preview_image = models.ImageField(upload_to='previews', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    posted = models.DateTimeField(null=True, blank=True)

    number_of_hits = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __unicode__(self):
        if self.slug == None:
            self.slug = slugify(self.title)
            self.save()

        return self.title


    def get_all_post_images(self):
        # just a way to get the post images in the admin
        return PostImage.objects.order_by('-pk')


    def get_top_level_comments(self):
        return self.comment_set.filter(parent_comment=None)

    def update_statistics(self, session_id):
        self.number_of_hits += 1
        self.save()

        visitor, created = UniqueVisitor.objects.get_or_create(post=self, session_id=session_id)
        visitor.number_of_hits += 1
        visitor.save()


    def get_body_html(self):
        html = self.body.lower()

        delimeter = '\r\n\r\n'
        open_header_delim = '[[ '
        close_header_delim = ' ]]'

        if delimeter not in html:
            print 'p-tagging the whole thing'
            html = "<p>%s</p>" % html
        else:
            new_html = ""
            first = ''
            second = html

            while delimeter in second:
                first, mih, second = second.partition(delimeter)
                
                first = first.strip()
                second = second.strip()

                if first != '' and first != None:
                    new_html += "<p>%s</p>" % first

            if second != '' and second != None:
                new_html += "<p>%s</p>" % second

            html = new_html

        # add bold header tags
        new_html = ""
        first = ''
        second = html

        while open_header_delim in second:
            first, mih, second = second.partition(open_header_delim)
            
            # everything before the [[ 
            new_html += first

            # middle is what's IN [[ ]] 
            # second is what's after the ]] 
            middle, mih, second = second.partition(close_header_delim)

            header_tag = "<h2 class='bold-header'>%s</h2>" % middle
            new_html += header_tag

        if second != '' and second != None:
            new_html += second

        html = new_html

        # add image tags
        matches = re.findall(r'({{\ img.(\d+) }})', html)

        if matches:
            for match_tuple in matches:
                image = PostImage.objects.get(pk=match_tuple[1])
                img_tag = "<img class='post-image' src='%s'>" % image.image_file.url
                html = html.replace(match_tuple[0], img_tag, 1)
        

        # matches = re.findall(r'(\[\[(.+)\]\])', html)

        # if matches:
        #     for match_tuple in matches:
        #         html = html.replace(match_tuple[0], header_tag, 1)

        html = html.replace('<p><h2', '<h2')
        html = html.replace('</h2></p>', '</h2>')

        return html


class PostImage(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image_file = models.ImageField(upload_to='image_file', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField("comment body", null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    post = models.ForeignKey('Post', null=True, blank=True)
    parent_comment = models.ForeignKey('Comment', null=True, blank=True, related_name='children')
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __unicode__(self):
            return self.author + ": " + self.body[:15]
