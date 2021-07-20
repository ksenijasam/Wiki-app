from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound, HttpResponseRedirect
from . import util
from django.urls import reverse
from django.shortcuts import redirect
import markdown2
from random import choices
from django import forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def funct(request, name):
    try:
        return render(request, "encyclopedia/pages.html",{
            "name1":name,
            "html1": markdown2.markdown(util.get_entry(name))
        })
    except: 
        return HttpResponseNotFound("<h1>Page Not Found.</h1>Such entry does not exist.")
    
def search(request):
    if util.get_entry(request.POST["q"]) is None:
        temp=[]
        for entry in util.list_entries():
            if request.POST["q"].upper() in entry.upper():
                temp.append(entry)
        if len(temp)==0:
            return HttpResponseNotFound("<h1>Not Found.</h1>Entry with such input does not exist.")
        else:
            return render(request, "encyclopedia/entries.html",{
                "entries":temp
            })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:funct", args=(request.POST["q"],)))


def random(request):
    return HttpResponseRedirect(reverse("encyclopedia:funct", args=(choices(util.list_entries()))))
    
class NewEntrieForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    

def newpage(request):
    if request.method=="POST":
        form = NewEntrieForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            for entry in util.list_entries():
                if title.upper() in entry.upper():
                    return HttpResponse("<h2>Encyclopedia entry with the provided title already exist.</h2>") 
            util.save_entry(title,text)
            return render(request, "encyclopedia/pages.html",{
                "name1":title,
                "html1": markdown2.markdown(text)
                    })
    else: 
        return render(request, "encyclopedia/new_page.html",{
            "form": NewEntrieForm()
        })

    
def edit(request,name):
    if request.method == "GET":
        title = name
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
        "form": NewEntrieForm(initial={"text": text, "title": title})
        })
    else:
        form = NewEntrieForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title,text)
            return render(request, "encyclopedia/pages.html",{
                "name1": title,
                "html1":markdown2.markdown(text)
                })

    


    










