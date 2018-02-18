from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable #connecting to airtable database
import os #for storing api keys
# Create your views here.

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))
#we now connect to our airtable database

def home_page(request):
    #print(str(request.GET.get('query', ''))) we take what user writes
    user_query = str(request.GET.get('query', ''))
    #we will use a formula inside airtable that searches in a particular way
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    #we only search on lower case, no matter how the user is typing --> no case sensitivity
    stuff_for_frontend = {'search_result': search_result}
    #sending for frontend
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)
#to run html file which we create under movies folder
#when someone starts the app, it should open function=homepage which renders the html code

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.gladessheriff.org/media/images/most%20wanted/No%20image%20available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
        #notify on create
            messages.success(request, 'Movie successfully added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error while trying to add a new movie.')
    return redirect("/")

#we now create the function for updating movie's info
def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url':request.POST.get('url') or 'http://www.gladessheriff.org/media/images/most%20wanted/No%20image%20available.jpg'}],
            'Rating':int(request.POST.get('rating')),
            'Notes':request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id, data)
        #notify on update
            messages.success(request, 'Movie successfully edited: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error while trying to edit the movie: {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        deleted_movie = AT.get(movie_id)['fields']['Name']
        AT.delete(movie_id)
    #notify on delete
        messages.warning(request, 'Movie successfully deleted: {}'.format(deleted_movie))
    except Exception as e:
            messages.warning(request, 'Got an error while trying to delete the following movie: {}'.format(e))
    return redirect('/')

