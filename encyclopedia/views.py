from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import util
import markdown2
import random
import re

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
        if util.get_entry(title):
            markdownText = util.get_entry(title)
            html = markdown2.markdown(markdownText)
            return render(request, "encyclopedia/content.html", {
                "content_html" : html,
                "title": title,
                })
        else:
            return error(request, "The entry you searched for does not exist.")

def create(request):
    if request.method == "POST":
            entry = list()
            entry = request.POST
            if util.get_entry(entry['title']):
                return error(request, f"An entry with the name {entry['title']} already exists. Please choose another title")
            else:
                util.save_entry(entry['title'], entry['content'])
                title = entry['title']
                return HttpResponseRedirect('/wiki/%s' % title)
    else:        
        return render(request, "encyclopedia/create.html")

def edit(request,title):
    content = util.get_entry(title)
    print(content)
    if request.method == "POST":
            entry = list()
            entry = request.POST
            if util.get_entry(entry['title']):
                util.save_entry(entry['title'], entry['content'])
                title = entry['title']
                return HttpResponseRedirect('/wiki/%s' % title)
            else :
                return error(request, "Something went wrong. Try again.")
    else:        
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
        })

def randompage(request):
        entries = util.list_entries()
        entry = random.choice(entries)
        return content(request, entry)

def searchpage(request):
                if request.method == "POST":
                    query = request.POST['q']
                    entries = util.list_entries()
                    result = []
                    for entry in entries:
                        if not re.search(query.lower(),entry.lower()) is None:
                            result.append(entry)
                        if query == entry:
                                markdownText = util.get_entry(entry)
                                html = markdown2.markdown(markdownText)
                                return render(request, "encyclopedia/content.html", {
                                    "title": entry,
                                    "content_html": html
                                    })
                    if len(result) == 0:
                        return error(request, "Sorry, no search results found.") 
                    else:
                        return render(request, "encyclopedia/search.html", {
                                "queries": result
                            })       

def error(request, error):
                return render(request, "encyclopedia/error.html", {
                        "error": error
                        })       