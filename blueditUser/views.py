from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import EditBio,  CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.db.models import Q

from subBluedit.models import Forum, Abo, Post, Comment, PostVote, CommentVote
from .models import BlueditUser
from django.views.generic import ListView
#from django.contrib.auth.forms import UserCreationForm

# View zum erstellen eines User ---------------------------------------------------------
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user = BlueditUser.objects.create_user(username=data['username'], password=data['password1'])

        return redirect(self.success_url)

# Zeige alle User an ---------------------------------------------------------
def showAllUser(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    context = {'users': BlueditUser.objects.all()}
    return render(request, 'user-list.html', context)

# Home-Seite des Users ---------------------------------------------------------
def show_profile(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    id = kwargs['pk']
    user = BlueditUser.objects.get(id=id)
    BlueditUser.update_votes(user)
    # Posts von Abos
    ownSubs = Abo.objects.filter(user=user, type='O')
    modSubs = Abo.objects.filter(Q(user=user) & (Q(type='A') | Q(type='S')))
    otherSubs = Abo.objects.filter(Q(user=user) & Q(type='N'))

    allSubs = Abo.objects.filter(user=user)
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
        "user" : user,
        "allAboPosts": allPosts,
        "posts": createdposts,
        "comments": comments,
        "ownSubs" : ownSubs,
        "modSubs" : modSubs,
        "otherSubs" : otherSubs
           }
    return render(request, 'user-profile.html', context)

# Editieren des Pofiles ---------------------------------------------------------
def bio_edit(request, **kwargs):
    if request.user.is_anonymous:
        return redirect('login')
    form = EditBio
    context = {'form' : form}
    user = BlueditUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = EditBio(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('home-feed')
    
    return render(request, 'editProfile.html', context)

