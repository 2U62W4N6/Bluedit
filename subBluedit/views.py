from django.shortcuts import render, redirect
from .models import Forum, Post, Comment, PostVote, CommentVote, Abo
from blueditUser.models import BlueditUser
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .forms import PostForm, CommentForm, SearchForm, UserEditForm, DeleteComment, EditCommnt
from django.urls import reverse_lazy
from django.db.models import Q

# Alle Foren ---------------------------------------------------------
def AllSubs(request):
    if request.user.is_anonymous:
        return redirect('login')
    search_query = request.GET.get("search")
    allSubs = None
    # Schaut nach ob eine Such-Anfrage mitgegeben wurd
    if search_query:
        allSubs = Forum.objects.filter(
            Q(name__icontains=search_query) |
            Q(owner__username__icontains=search_query) |
            Q(type__icontains=search_query[0])
        ).distinct()
    else:
        allSubs = Forum.objects.all()
    context = {'all_subs': allSubs}
    return render(request, 'forum-list.html', context)

# Forum erstellen ---------------------------------------------------------
def CreateSub(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        forum = Forum.objects.create(owner=request.user,name=request.POST.get("name"),description=request.POST.get("description"), type=request.POST.get("type"))
        Abo.objects.create(user=request.user, type='O', forum=forum)
        return redirect('sub-list')

    return render(request, 'forum-create.html')

# Ein Forum / Alle Posts ---------------------------------------------------------
def OneSub(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    subID = kwargs['pk']
    allPosts = Post.objects.filter(forum_id=subID)
    request_query = request.GET.get("search")
    if request_query:
        allPosts = Post.objects.filter(
            Q(title__icontains=request_query) |
            Q(text__icontains=request_query) |
            Q(creator__username__icontains=request_query)
        ).filter(forum_id=subID).distinct()

    if request.method == 'POST':
        Forum.objects.get(id=subID).delete()
        return redirect('sub-list')

    context = {
        'allPost': allPosts,
        'forum' : Forum.objects.get(id=kwargs['pk'])
    }
    return render(request, 'post-list.html', context)

# Create TextPost ---------------------------------------------------------
def CreateTextPost(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        text = request.POST.get('text')
        title = request.POST.get('title')
        user = request.user
        forum = Forum.objects.get(id=kwargs['pk'])
        Post.objects.create(creator=user, forum=forum, text=text, title=title)
        return redirect('sub', pk=kwargs['pk'])

    return render(request, 'create-text.html')

# Create MediaPost ---------------------------------------------------------
def CreateMediaPost(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        media = request.POST.get('url')
        title = request.POST.get('title')
        user = request.user
        forum = Forum.objects.get(id=kwargs['pk'])
        Post.objects.create(creator=user, forum=forum, media=media, title=title)
        return redirect('sub', pk=kwargs['pk'])

    return render(request, 'create-media.html')


# Ein Post ---------------------------------------------------------
def PostDetail(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    postID = kwargs['pk_post']
    post = Post.objects.get(id=postID)

    if 'delete-post' in request.POST:
        Post.objects.get(id=kwargs["pk_post"]).delete()
        print(kwargs['pk_sub'])
        return redirect('sub', pk=kwargs['pk_sub'])

    # Add Comment
    if 'comment' in request.POST:
        form = CommentForm(request.POST)
        form.instance.creator = request.user
        form.instance.post = post
        if form.is_valid():
            form.save()
            return redirect('post', pk_sub = kwargs['pk_sub'], pk_post=kwargs['pk_post'])
        else:
            print(form.errors)

    if 'delete' in request.POST:
        form = DeleteComment(request.POST)
        if Comment.objects.filter(id=request.POST['delete']).exists():
            Comment.objects.get(id=request.POST['delete']).delete()
        if form.is_valid():
            form.save()
            return redirect('post', pk_sub = kwargs['pk_sub'], pk_post=kwargs['pk_post'])
        else:
            print(form.errors)
     
    comments = Comment.objects.filter(post=post)
    context = {
        'that_one_post': post,
        'comment_for_that_post': comments,
        'comment_form': CommentForm,
    }

    return render(request, 'post-detail.html', context)

# Post Editieren ---------------------------------------------------------
def PostEdit(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    post = Post.objects.get(id=kwargs['pk_post'])
    print(post.text)
    if request.method == "POST":
        text = request.POST.get('text')
        print(text)
        Post.objects.filter(id=kwargs['pk_post']).update(text=text)
        return redirect('post', pk_sub=kwargs['pk_sub'], pk_post=kwargs['pk_post'])

    context = {'post' : post}
    return render(request, 'post-edit.html', context)

# Home-Seite ---------------------------------------------------------
def showHome(request):
    if request.user.is_anonymous:
        return redirect('login')    
    # User.objects.get(id=)
    user = BlueditUser.objects.get(id=request.user.id)
    BlueditUser.update_votes(user)
    # Posts von Abos
    ownSubs = Abo.objects.filter(user=user, type='O')
    modSubs = Abo.objects.filter(Q(user=user) & (Q(type='A') | Q(type='S')))
    otherSubs = Abo.objects.filter(user=user, type='N')

    allSubs = Abo.objects.filter(Q(user=user) & ~Q(type='B'))
    ids_Abos = []
    for abo in allSubs:
        ids_Abos.append(abo.forum.id)

    allForum = Forum.objects.filter(id__in=ids_Abos)
    ids_Foren = []
    for forum in allForum:
        ids_Foren.append(forum.id)

    allPosts = Post.objects.filter(forum__in=allForum)[:5]
    # Posts die erstellt wurden
    all_foren = Post.objects.filter(creator=user)
    
    ids_posts = []
    for forum in all_foren:
        ids_posts.append(forum.id)

    createdposts = Post.objects.filter(id__in=ids_posts)[:5]
    # Kommentare
    comments = Comment.objects.filter(creator=user)[:5]

    context = {
        "allAboPosts": allPosts,
        "posts": createdposts,
        "comments": comments,
        "user" : user,
        "ownSubs" : ownSubs,
        "modSubs" : modSubs,
        "otherSubs" : otherSubs
           }
    return render(request, 'home-feed.html', context)

# Suchfunktion ---------------------------------------------------------
def my_search(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        form_in_my_function_based_view = SearchForm(request.POST)
        search_string = request.POST['name']
        foren_found = Forum.objects.filter(name__contains=search_string)

        form_in_my_function_based_view = SearchForm()
        context = {'form': form_in_my_function_based_view,
                   'foren_found': foren_found,
                   'show_results': True}
        return render(request, 'my-search.html', context)

    else:
        form_in_my_function_based_view = SearchForm()
        context = {'form': form_in_my_function_based_view,
                   'show_results': False}
        return render(request, 'my-search.html', context)

# Edit Subscriber-Levels ---------------------------------------------------------
def setRole_or_Ban(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    forum = Forum.objects.get(id=kwargs['pk'])
    queryset = Abo.objects.filter(forum=forum)
    if request.method == "POST":
        if not request.POST.get('user') == None:
            user = BlueditUser.objects.get(username=request.POST.get('user'))
            Abo.objects.filter(user=user, forum=forum).update(type=request.POST.get('type'))
        return redirect('sub', forum.id)
    context = {"queryset" : queryset, "forum" : forum}

    return render(request, 'editAbo.html', context)

# Like/Dislike Post ---------------------------------------------------------
def VotePost(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    PostVote.vote(post_id=kwargs['pk'], user=request.user, vote=kwargs['up_or_down'])
    post = Post.objects.get(id=kwargs['pk'])
    Post.updateVotes(post)
    BlueditUser.update_votes(user=post.creator)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Like/Dislike Comment ---------------------------------------------------------
def VoteComment(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    CommentVote.vote(comment_id=kwargs["pk"], user_id=request.user, vote=kwargs["up_or_down"])
    Comment.updateVotes(comment_id=kwargs["pk"])
    comment = Comment.objects.get(id=kwargs["pk"])
    BlueditUser.update_votes(user=comment.creator)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Ein Kommentar ---------------------------------------------------------
def CommentDetail(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    that_one_comment = Comment.objects.get(id=kwargs['pk_comment'])
    post = Post.objects.get(id=kwargs['pk_post'])
     # Add Comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.creator = request.user
        form.instance.post = post
        form.instance.parent = that_one_comment
        if form.is_valid():
            form.save()
            return redirect('post', pk_sub=kwargs['pk_sub'], pk_post=kwargs['pk_post'])
        else:
            print(form.errors)

    context = {
        'that_one_comment': that_one_comment,
        'comment_form': CommentForm,
    }

    return render(request, 'comment-detail.html', context)

# Kommentar Editieren ---------------------------------------------------------
def CommentEdit(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    comment = Comment.objects.filter(id=kwargs['pk_comment'])
    if request.method == 'POST':
        comment.update(text=request.POST['text'])
        return redirect('post', pk_post=kwargs['pk_post'], pk_sub=kwargs['pk_sub'])    
        
    context= {"comment" : comment[0]}
    return render(request, 'comment-edit.html', context)

# Ein Sub Folgen---------------------------------------------------------
def Follow(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    forum = Forum.objects.get(id=kwargs['pk'])
    Abo.objects.create(user=request.user, forum=forum, type='N')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Ein Sub Entfolgen ---------------------------------------------------------
def UnFollow(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    forum = Forum.objects.get(id=kwargs['pk'])
    Abo.objects.filter(user=request.user, forum=forum).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))