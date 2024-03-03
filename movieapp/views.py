from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import CreateView,ListView
from django.urls import reverse
from .forms import NewUserForm
from .models import Post,Comment
from django.http import HttpResponseRedirect, JsonResponse


#  view function for home page
# def home(request):
#     # Getting object of database
#     posts = Post.objects.all()
#     return render(request, "movieapp/home.html", {"posts": posts})

class Home(ListView):
    model = Post
    template_name = "movieapp/home.html" 
    context_object_name = "posts"
    ordering = ["-created"]


# view for register page
def register_user(request):
    # Check if the method is post
    if request.method == "POST":
        form = NewUserForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            form.save()

            # authenticate & login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)

            # double check if user registered succesfully
            if user is not None:
                login(request, user)
                messages.success(request, "You have been registered successfully")
                return redirect("home")
    else:
        form = NewUserForm()
        return render(request, "movieapp/register.html", {"form": form})
    return render(request, "movieapp/register.html", {"form": form})

# view function for liking a post
def like_post(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.likes += 1
        post.save()
        return HttpResponseRedirect(reverse("individual_post",args=[str(pk)]))

    
def add_comment(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        commenter_name = request.user.username
        comment_text = request.POST.get("comment_text")
        Comment.objects.create(post=post, commenter_name=commenter_name, comment=comment_text)
        return HttpResponseRedirect(reverse("individual_post",args=[str(pk)]))

def update_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    # Check if the request method is POST and if the user is authenticated and the author of the comment
    if request.method == "POST" and  request.user.is_authenticated and comment.commenter_name == request.user.username:
        # Get the updated comment text from the form
        updated_comment_text = request.POST.get("updated_comment_text")

        # Update the comment
        comment.comment = updated_comment_text
        comment.save()

        messages.success(request, "Comment updated successfully")
        return redirect("home")
    else:
        messages.error(request, "You are not authorized to update this comment")
        
    return render(request, "movieapp/update_comment.html",{"comment":comment})

def delete_comment(request, pk):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Fetch the comment to be deleted
            comment = Comment.objects.get(id=pk)
            
            # Check if the user is the author of the comment
            if comment.commenter_name == request.user.username:
                comment.delete()
                messages.success(request, "Comment deleted successfully")
            else:
                messages.error(request, "You are not authorized to delete this comment")
        except Comment.DoesNotExist:
            messages.error(request, "The comment you are trying to delete does not exist")
    else:
        messages.error(request, "You need to login first")
    
    return redirect("home")

    

# view for login page
def login_user(request):
    # Check if the request method is post
    if request.method == "POST":
        uname = request.POST.get("username")
        pswd = request.POST.get("password")

        # authenticating user
        user = authenticate(request, username=uname, password=pswd)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully...")
            return redirect("home")
        else:
            messages.warning(request, "couldn't log in ...")
    return render(request, "movieapp/login.html")


# view for logging out
def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out...")
    return redirect("home")


# view for individual post
def individual_post(request, pk):
    # Check if the user is logged in
    if request.user.is_authenticated:
        user_post = Post.objects.get(id=pk)
        return render(request, "movieapp/post.html", {"user_post": user_post})
    else:
        messages.warning(request, "You need to log in ")
        return redirect("login")


#  view for deleting a post
def delete_post(request, pk):
    # checking is the user is a valid user
    if request.user.is_authenticated:

        # creating object for that post
        post = Post.objects.get(id=pk)

        # User can only delete the post if he posted that post
        if request.user.email == post.email and request.user.username == post.user_name:
            post.delete()
            messages.success(request, "Post deleted successfully")
            return redirect("home")
        else:
            messages.warning(request,"You are signed in as "+request.user.email+" So you can't delete this post")
            return redirect("home")

    else:
        messages.warning(request, "You need to login first")
        return redirect("login")

    return render(request, "movieapp/home.html")


# View for adding new post

# def add_post(request):

#     # Checking if the user is logged in
#     if request.user.is_authenticated:

#         # checking if the request is post
#         if request.method == "POST":

#             # getting variables from form
#             username = request.user.username
#             email = request.user.email
#             caption = request.POST.get("caption")
#             content = request.POST.get("content")

#             # Adding variables to Database
#             new_post = Post()
#             new_post.user_name = username
#             new_post.email = email
#             new_post.caption = caption
#             new_post.content = content
#             new_post.save()

#             return redirect("home")
#     else:
#         messages.warning(request,"You need to login to add a post...")
#         return redirect("login")
#     return render(request, "movieapp/add_post.html")

class Add_post(CreateView):
    model = Post
    template_name = "movieapp/add_post.html"
    fields = ("caption","content","images")



# Views for updating post

def update_post(request, pk):

    # Checking if the user is authenticated
    if request.user.is_authenticated:

        # fetching current data
        current_post = Post.objects.get(id=pk)

        if request.method == "POST" and request.user.username == current_post.user_name and request.user.email == current_post.email :
            # getting variables from form
            # username = current_post.user_name
            # email = current_post.email
            caption = request.POST.get("caption")
            content = request.POST.get("content")

            # updating variables to Database
            # current_post.user_name = username
            # current_post.email = email
            current_post.caption = caption
            current_post.content = content
            current_post.save()

            return redirect("home")
    else:
        messages.warning(request, "You need to login to add a post...")
        return redirect("login")
    return render(request, "movieapp/update_post.html",{"current_post":current_post})