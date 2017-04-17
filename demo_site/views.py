import os
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import User_Login_Form, Post_Form

from .models import Post, Profile, DevOps


def landing_page(request):

    form = User_Login_Form(request.POST or None)

    demo_url = '/demo/{0}'.format(os.environ.get("DEMO_URL"))

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect(demo_url)

    context = {
        'page_title': "Conversational UI Demo",
        'links': [('GitHub', 'https://github.com/', 'github-id')],
        'demo_url': demo_url,
        'form': form
    }

    return render(request, 'demo_site/landing.html', context)





def logout_link(request):

    logout(request)

    return redirect('/')





def demo(request):

    if not request.user.is_authenticated():
        return redirect('/')

    posts = Post.objects.filter(author=request.user)

    dev_ops = DevOps.objects.all()

    post_form = Post_Form(request.POST or None)

    context = {
        'page_title': request.user.profile.bot_name,
        'links': [
            ('Development Info', '#', 'main-id'),
            ('Resources', '#', 'resources-id'),
            ('Modules', '#', 'modules-id'),
            ('Logout', '/logout/', 'exit-id')
        ],
        'posts': posts,
        'post_form': post_form,
        'dev_ops': dev_ops
    }

    return render(request, 'demo_site/demo.html', context)






past_contexts = []
task_in_progress = []

def create_post(request):

    if request.user.is_authenticated() and request.method == 'POST':

        if request.POST.get('the_post') != "":
            post_text = request.POST.get('the_post')
            post_author = request.user

            post = Post(message=post_text, author=post_author)
            post.save()

            response_data = {}

            if post.subjects:
                post.subjects = post.subjects.split(",")

            if post.intent == "REMI":
                task_in_progress.append(post.intent)

            response_data['message'] = post.message
            response_data['intent'] = post.intent
            response_data['task'] = task_in_progress
            response_data['subjects'] = post.subjects
            response_data['past_intents'] = past_contexts
            response_data['message_reply'] = post.message_reply
            response_data['upload_date'] = post.upload_date.strftime('%B %d, %Y %I:%M %p')


            past_contexts.append(post.intent)
            if len(past_contexts) >= 5:
                past_contexts.pop(0)

        return JsonResponse(response_data)

    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


