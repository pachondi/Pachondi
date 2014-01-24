from django import template
register = template.Library()
import pdb;

@register.filter 
def pdb(element):
    import pdb; pdb.set_trace()
    return element

@register.simple_tag 
def render_likes(likedList, loggedUser):
    """
    This tag is used to render likes in a readable format
    For example: 
    You like this message
    You and X like this message
    You, X and Y like this message
    X likes this message
    X and Y like this message
    X, Y and Z like this message
    
    """
    total_likes = likedList.count()
    liked_by = ''
    like = "like"
    #check if current user likes this message
    if loggedUser in [ likeobj.user for likeobj in likedList]:
        liked_by = 'You'
    elif total_likes == 1:
            like = "likes"
        #remove current user from the list
        #@todo: after establishing only one like per user
        #use del. It's more efficient
        #likedList = [ a for a in likedList if a.user !=loggedUser ]
        
        #@todo: ok filter lambda is not working
    
    if total_likes > 1:    
        for i in range(len(likedList)):
            #if likedList[i].user != loggedUser:
            if i == len(likedList)-1: 
                liked_by += ' and '+str(likedList[i].user)
            else:
                liked_by += ', '+str(likedList[i].user)
    
    if total_likes > 0:
        liked_by += " "+like+" this message."
               
    return "( Total "+ str(total_likes) +" Likes ) "+liked_by;

