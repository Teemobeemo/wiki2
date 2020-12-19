from django.shortcuts import render, redirect
from django.contrib import messages
from . import util

from random import randint
from markdown2 import Markdown

def index(request):
    entries = util.list_entries()
    context = {
        "entries": entries
    }

    return render(request, "encyclopedia/index.html", context)

def entry(request, title):

    entry = util.get_entry(title)

    markdowner = Markdown()

    entry = markdowner.convert(entry)


    if entry:
        context = {
            "title": title,
            "entry": entry
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html")
    

def search(request): 

    entries = util.list_entries()
    query = request.GET['q']

    # filtered entries overwriting old variable
    filtered_entries = search_filter(entries, query)

    # if len(entries) == 1:
    #     entry = entries[0]
    #     return redirect("entry", entry)


    # If filtered entries exists
    if filtered_entries:

        if len(filtered_entries) == 1:

            # if query.upper() == entries[0].upper():
            if query.upper() == filtered_entries[0].upper():
                entry = filtered_entries[0]
                return redirect("entry", entry)
            else:
                context = {
                    "entries": filtered_entries
                }
                return render(request, "encyclopedia/search.html", context)
        else:
            # TODO
            # return list of filtered entries
            context = {
                "entries": filtered_entries
            }
            return render(request, "encyclopedia/search.html", context)
            
    else:
        # TODO
        # return full list of entries in search template
        pass

        

    
    return render(request, "encyclopedia/index.html")




def create(request):


    if request.method == 'POST':

        title = request.POST['title']
        content = request.POST['content']

        all_entries = util.list_entries()

        if title in all_entries:
            # TODO 
            # Write error message to user
            messages.error(request, 'An entry with this title already exists!')
            return redirect("create")

        else:
            util.save_entry(title, content)
            return redirect("entry", title)

    return render(request, "encyclopedia/create.html")




def edit(request, title):

    if request.method == "POST":

        content = request.POST['content']

        util.save_entry(title, content)

        return redirect("entry", title)
    else:
        entry = util.get_entry(title)

        context = {
            "title": title,
            "entry": entry,
        }

        return render(request, "encyclopedia/edit.html", context)




def random(request):

    # Get all entries
    all_entries = util.list_entries()

    #   0       1        2        3      4       5      6
    ['CSS', 'Cofee', 'Django', 'Git', 'JS', 'Python', 'HTML' ]



    min_number = 0
    max_number = len(all_entries) - 1

    random_number = randint(min_number, max_number)

    # css = all_entries[0]

    # print('ALL ENTRIES')
    # print(all_entries)
    # print('index 0 = ',css)
    print('Random index')
    print(random_number)

    random_entry = all_entries[random_number]


    # print('Random entry')
    # print(random_entry)

    return redirect("entry", random_entry)



































def search_filter(list, q):
    # Make new list to return with filtered entries
    result = []

    # Loop through the list and test if the query is in the current string item
    for i in range(len(list)):
        # print(list[i])
        # print(q)

        # Convert item and query to uppercase to see if the item contains the query
        if q.upper() in list[i].upper():
            # print(True)

            if q.upper() == list[i].upper():
                return [list[i]]

            # If the item contains the query then it will be appended to the new list
            result.append(list[i])
        # else: 
        #     print(False)

    return result