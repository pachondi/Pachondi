from django.core.urlresolvers import reverse
from django import template


register = template.Library()

@register.filter 
def pdb(element):
    import pdb; pdb.set_trace()
    return element

@register.simple_tag 
def render_likes(likedList, loggedUser, obj):
    """
    This tag is used to render likes in a readable format
    For example: 
    You like this message
    You and X like this message
    You, X and Y like this message
    X likes this message
    X and Y like this message
    X, Y and Z like this message
    Like link should prevent auto clicks.
    What if javascript is disabled 
    """
    total_likes = likedList.count()
    liked_by = '<span style="border:1px solid black;width:auto;" >'
    
    #To change when 2nd person singular happens 
    like = "like"
    like_link = '';
    #check if current user likes this message
    if loggedUser in [ likeobj.user for likeobj in likedList]:
        liked_by += 'You'
    else:
        #set the link url
        like_link = '<span><a href="'+reverse('group-discussion-message-like',args=(obj.id,))+'">Like<a/>. </span>'
        liked_by += like_link
        #Only one person liked and its not me, so change to likes
        if total_likes == 1:
            like = "likes"
    
    #remove current user from the list since You is established
    #@todo: after establishing only one like per user
    #use del. It's more efficient
    #@todo: ok filter lambda is not working
    likedList = [ a for a in likedList if a.user !=loggedUser ]
        
    if total_likes > 1:    
        for i in range(len(likedList)):
            if i == len(likedList)-1: 
                liked_by += ' and '+str(likedList[i].user)
            else:
                liked_by += ', '+str(likedList[i].user)

    if total_likes > 0:
        liked_by += " "+like+" this message."
    liked_by += like.title()+" ("+ str(total_likes) +")"
    
    liked_by += '</span>'
    #<a href="{% url 'group-discussion-message-like' messageobj.id %}">Like<a/> ({{likes|length}} Likes)
        
    return liked_by;

