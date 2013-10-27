from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from app.users.posts.models import UserPost, PostComment
from django.utils.datetime_safe import datetime
from app.users.models import SiteUser

@login_required
def add_post(request, user_id, **kwargs):
    if request.method == "POST":   
        #current_user = get_object_or_404(SiteUser, id=request.user.id)
        user = get_object_or_404(SiteUser, id=user_id)
        post = UserPost()
        post.user=request.user
        post.message=request.POST["message"]
        post.post_by=user
        post.post_dt=datetime.now();
        post.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def delete_post(request, post_id, **kwargs):    
    post = UserPost.objects.get(pk=post_id)
    post.delete()
    
    return redirect('/users/home', **kwargs)

@login_required
def post_comment(request, post_id, **kwargs):
    if request.method == "POST":   
        user = get_object_or_404(SiteUser, id=request.user.id)
        post = UserPost.objects.get(pk=post_id)
        comment=PostComment()
        comment.post=post
        comment.comment_by=user
        comment.message=request.POST["comment"]
        comment.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def delete_comment(request, comment_id, **kwargs):    
    comment = PostComment.objects.get(pk=comment_id)        
    if comment:
        comment.delete()
    
    return redirect('/users/home', **kwargs)
