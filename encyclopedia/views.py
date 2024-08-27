from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown2
from django.urls import reverse
from . import util
from django.shortcuts import redirect
from django import forms
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#def wiki(request):
 #   return HttpResponse("nothing on this page")

def title(request,title):
    content=util.get_entry(title)
    if content==None:
        return render(request,"encyclopedia/pagenotfound.html",{
            "content" :["Page Not Found !!"]
        })
    else:
        content_html=markdown2.markdown(content)
        return render(request,"encyclopedia/info.html",{
            "title" :title,
            "content" :content_html
        })
#class SearchForm(forms.Form):
 #   query=forms.CharField()

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    if query:
        if query in entries:
            """content = util.get_entry(query)
            content_html = markdown2.markdown(content)
            return render(request, "encyclopedia/info.html", {
                "title": query,
                "content": content_html
            })"""
            return HttpResponseRedirect(reverse("encyclo:title",args=[query]))
        else:
            listy = [entry for entry in entries if query.lower() in entry.lower()]
            if listy:
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "entries": listy
                })
            else:
                return render(request,"encyclopedia/pagenotfound.html",{
                    "content" :["No page named" , query,"!!"]
                })
                
    else:
        current_page = request.META.get('HTTP_REFERER')
        return redirect(current_page)
class newentries(forms.Form):
    new_entry=forms.CharField() 
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class':'custom_textarea'
    }))
def createnewpg(request):
    return render(request,"encyclopedia/createnewpage.html",{
        "title" :"create_new_page",
        "form" :newentries()

    })
def check(request):
    entries=util.list_entries()
    if request.method=="POST":
        form=newentries(request.POST)
        if form.is_valid():
            pagename=form.cleaned_data['new_entry']
            for entry in entries:
                if pagename.lower() == entry.lower():
                    form.add_error("new_entry","This page already exists")
                    return render(request,"encyclopedia/createnewpage.html",{
                        "title" :"Create_new_page",
                        "form" :form
                    })


            content= form.cleaned_data['content']
            util.save_entry(pagename ,content)
            return redirect(reverse("encyclo:title",args=[pagename]))
        else:
            return render(request,"encyclopedia/createnewpage.html",{
                "title" :"Create_new_page",
                "form" :newentries()
            })
    else:
        
        return render(request,"encyclopedia/createnewpage.html",{
            "title" :"Create_new_page",
            "form" :newentries()
        })
class editing(forms.Form):
    do_edit=forms.CharField(widget=forms.Textarea(attrs={
        'class':'custom_textarea'
    }))

def editpage(request,title_name):
    if request.method=="POST":
        form=editing(request.POST)
        if form.is_valid():
            edit=form.cleaned_data['do_edit']
            edit_html=markdown2.markdown(edit)
            util.save_entry(title_name,edit_html)
            return HttpResponseRedirect(reverse("encyclo:title",args=[title_name]))
    else:
        data={"do_edit": util.get_entry(title_name)}
        return render(request,"encyclopedia/edit.html",{
            "title" :title_name,
            "form" :editing(initial=data)
        })


def randompage(request):
    entries=util.list_entries()
    title=random.choice(entries)

    return HttpResponseRedirect(reverse("encyclo:title",args=[title]))