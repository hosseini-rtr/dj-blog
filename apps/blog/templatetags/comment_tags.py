from django import template

register = template.Library()


@register.inclusion_tag('base/components/comment_list.html')
def comments_for(obj, show_unapproved=False):
    comments = obj.comments.all()
    if not show_unapproved:
        comments = comments.filter(is_approved=True)
    return {'comments': comments}
