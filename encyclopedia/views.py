from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from markdown import markdown
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        post = request.POST.get('post')
        # Validate
        if not title or not post:
            return render(request, 'encyclopedia/create.html', {'message': 'Please fill the required details', 'post': post})

        if title in util.list_entries():
            return render(request, 'encyclopedia/create.html', {'message': 'Title Already Exists', 'post': post})
        
        # Save post
        util.save_entry(title, post)

        return HttpResponseRedirect(reverse("display", args=[title]))
    
    return render(request, "encyclopedia/create.html", {'message': ''})


def displayPage(request, title): 
    return render(request, "encyclopedia/display.html", {
        "title": title.capitalize(),
        "content": markdown(util.get_entry(title)),
    })


def edit(request, title):
    post = util.get_entry(title)
    if request.method == 'POST':
        edited_post = request.POST.get('post')
        # Validate
        if not edited_post:
            return render(request, 'encyclopedia/edit.html', {'message': 'Please fill the required details', 'post': edited_post, 'title': title})
        
        # Save post
        util.save_entry(title, edited_post)

        return HttpResponseRedirect(reverse("display", args=[title]))
    
    return render(request, "encyclopedia/edit.html", {'message': '', 'post': post, 'title': title})


def random(request):
    all_titles = util.list_entries()
    n = randint(0, (len(all_titles) - 1))
    return HttpResponseRedirect(reverse("display", args=[all_titles[n]]))


def redirect(request):
     return HttpResponseRedirect(reverse("index"))


def search(request):
    if request.method == "POST":
        q = request.POST.get("q")
        q = q.lower()
        if not q:
            return HttpResponseRedirect(reverse("index"))
        
        all_titles = util.list_entries()
        matches = []
        
        for title in all_titles:
            title_lower = title.lower()
            # If exact match, display the page
            if q == title_lower:
                return HttpResponseRedirect(reverse("display", args=[title]))
            # If substring then display all the match cases
            substring = title_lower.find(q)

            if substring != -1:
                matches.append(title)

        return render(request, "encyclopedia/index.html", {
            "entries": matches,
        })
    
    return HttpResponseRedirect(reverse("index"))

