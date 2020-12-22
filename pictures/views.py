from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When
from hashids import Hashids
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from taggit.models import Tag
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from pictures.models import Profile, Images, SearchLog, Bookmark
from pictures.forms import ImagesForm, EditProfileForm
from fast_pagination.helpers import FastPaginator # not working?

hashedId_user = Hashids(salt='WIORUNVWinosf0940vwiev w09rhw09 wb bvwerEFUBV',min_length=12)
hashedId_image = Hashids(salt='rervehr0 erOUBO80h BP89pbh smdUB3498 IUBubdevwerv',min_length=12)

def home(request):
    """
    Get the top images from cached results. If the cached results do not exist
    manually create the results. To avoid any loss of data Celerey tasks are scheduled for half the duration of the the 
    cached object time to live. Celerey task will ideally always have live updated results.
    """
    top_tags = cache.get('images_top_tags')
    top_images = cache.get('images_top_images')
    if top_tags == None:
        top_tags = Images.objects.get_top_tags()
        cache.set('images_top_tags', top_tags, 3600)
    if top_images == None:
        top_images = Images.objects.get_top()
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(top_images)])
        top_images = Images.objects.all().filter(parent_image=None).order_by(-preserved)
        cache.set('images_top_images', top_images, 3600)
    page = request.GET.get('page', 1)
    paginator = Paginator(top_images, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context = {
        'tags':top_tags,
        'images':images,
        'top_active':'bg-nav-active'
    }
    return render(request, 'pictures/home.html', context)

def top_viewed(request):
    
    top_viewed_images = cache.get('images_top_viewed_images')
    if top_viewed_images == None:
        top_viewed_images = Images.objects.get_most_viewed()
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(top_viewed_images)])
        top_viewed_images = Images.objects.all().filter(parent_image=None).order_by(-preserved)
        cache.set('images_top_viewed_images', top_viewed_images, 7200)
    page = request.GET.get('page', 1)
    paginator = Paginator(top_viewed_images, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)     
    context = {
        'images':images,
        'viewed_active':'bg-nav-active'
    }
    return render(request, 'pictures/home.html', context)


def latest(request):
    
    latest_images = cache.get('images_all_latest_images')
    if latest_images == None:
        latest_images = Images.objects.all().filter(parent_image=None).order_by('-last_edited')
        cache.set('images_all_latest_images', latest_images, 600) # latest images are also cached every 10 minutes 
    page = request.GET.get('page', 1)
    paginator = Paginator(latest_images, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)     
    context = {
        'images':images,
        'latest_active':'bg-nav-active'
    }
    return render(request, 'pictures/home.html', context)

def image_tags(request, tag):
    
    """
    Currently images per each tag are not scheduled to be cached via Celerey due to server limitations on number of active workers (Heroku workers).
    Ideally images would be cached everytime a new instance is added to a tag - due to demo purposes images were not initially set to a cache
    """
    tag = get_object_or_404(Tag, slug=tag)
    tag_images = cache.get(f'images_{tag.slug}_tagged_images')
    
    if tag_images == None:
        tag_images = Images.objects.get_tag_images(tag=tag)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(tag_images)])
        tag_images = Images.objects.all().filter(parent_image=None).order_by(-preserved)
        cache.set(f'images_{tag.slug}_tagged_images', tag_images, 1000)
        
    # get the related tags based on the posts sharing the tag
    # exclude the tag itself when  gettings the most common tags
    related_tags = Images.tags.most_common(extra_filters={'images__in': tag_images }).exclude(name=tag.name)[:10]
    
    page = request.GET.get('page', 1)
    paginator = Paginator(tag_images, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context = {

        'images':images,
        'tag_name':tag.name,
        'related_tags':related_tags
    }
    return render(request, 'pictures/home.html', context)

@login_required
def like_image(request, hashed_id):
    """
    hashed_id refers to an id not saved in the database and created by a random salt based on an objects id, e.g 
    Image object. This provides an extra layer of security as instance id's will not be displayed to the any request
    """
    data = dict()
    id = hashedId_image.decode(hashed_id)[0]
    image = get_object_or_404(Images, id=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.user in image.likes.all():
                image.likes.remove(request.user)
                is_liked = False
            else:
                image.likes.add(request.user)
                is_liked = True
            context = {
                'image':image, 
                'is_liked':is_liked,
                'like_count':image.likes.count()
            }
            data['like'] = render_to_string('pictures/likes.html', context, request=request)
            return JsonResponse(data)

def view_profile_images(request, username):

    user = get_object_or_404(Profile, username=username)
    if request.user.is_authenticated:
        is_request_user = True if request.user == user else False # check to see if the request.user is same as the requested profile user
    else:
        is_request_user = False
        
    image_list = user.images.all().filter(parent_image=None, is_collection=False).order_by('-last_edited')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(image_list, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
        
    context = {
        'is_request_user':is_request_user,
        'images':images,
        'user':user,
        'image_count_text':user.get_image_count_text(),
        'img_count':user.images.filter(parent_image=None, is_collection=False).count(),
        'collection_count':user.images.filter(is_collection=True, parent_image=None).count(),
    }
    
    return render(request, 'pictures/profile.html', context)

def view_profile_collections(request, username):

    user = get_object_or_404(Profile, username=username)
    if request.user.is_authenticated:
        is_request_user = True if request.user == user else False # check to see if the request.user is same as the requested profile user
    else:
        is_request_user = False
        
    image_list = user.images.all().filter(is_collection=True, parent_image=None).order_by('-last_edited')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(image_list, 20)
    try:
        collections = paginator.page(page)
    except PageNotAnInteger:
        collections = paginator.page(1)
    except EmptyPage:
        collections = paginator.page(paginator.num_pages)
        
    context = {
        'is_request_user':is_request_user,
        'images':collections,
        'user':user,
        'collection_count':user.images.filter(is_collection=True, parent_image=None).count(),
        'image_count_text':user.get_image_count_text(),
        'img_count':user.images.filter(parent_image=None, is_collection=False).count(),
        'is_collection_page':True
    }
    
    return render(request, 'pictures/profile.html', context)

def view_image(request, hashed_id):
    
    data = dict()
    id = hashedId_image.decode(hashed_id)[0]
    image = get_object_or_404(Images, id=id)
    if request.user.is_authenticated:
        if request.user not in image.views.all():
            image.views.add(request.user)
    like_count = image.likes.count()
    is_liked = request.user in image.likes.all()
    views_count = image.views.count()
    context = {
        'like_count':like_count,
        'is_liked':is_liked,
        'image':image,
        'views':views_count
    }
    data['image'] = render_to_string('pictures/image_obj.html', context, request=request)
    return JsonResponse(data)

@login_required
def bookmark_image(request, hashed_id):
    data = dict()
    id = hashedId_image.decode(hashed_id)[0]
    image = get_object_or_404(Images, id=id)
    if request.method == "GET":
        if request.user.is_authenticated:
            if Bookmark.objects.filter(profile=request.user,image=image).exists():
                data['is_bookmarked'] = True
            else:
                data['is_bookmarked'] = False
    if request.method == "POST":
        if request.user.is_authenticated:
            if Bookmark.objects.filter(profile=request.user,image=image).exists():
                Bookmark.objects.filter(profile=request.user,image=image).delete()
                data['is_bookmarked'] = False
            else:
                Bookmark.objects.create(profile=request.user,image=image)
                data['is_bookmarked'] = True
    return JsonResponse(data)

@login_required
def bookmarks(request):
    
    bookmark_list = request.user.bookmarks.all().filter(image__parent_image=None, image__is_collection=False).values_list('image_id', flat=True)
    
    image_list = Images.objects.filter(id__in=bookmark_list).order_by('-last_edited')
        
    page = request.GET.get('page', 1)
    paginator = Paginator(image_list, 20)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    
    context = {
        'images':images,
        'is_bookmark':True
    }
     
    return render(request, 'pictures/home.html', context)

@login_required
def create_image(request):     
    data=dict()
    form = ImagesForm()
    if request.method == "POST":
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(False)
            image.author = request.user
            image.save()
            form.save_m2m()
            data['saved_successfully'] = True
            data['image_object'] =  render_to_string('pictures/new_image.html', {'image':image}, request=request)
            data['img_count'] = image.author.images.filter(parent_image=None, is_collection=False).count()
            data['img_text'] = image.author.get_image_count_text()
        else:
            data['saved_successfully'] = False
        return JsonResponse(data)
    context = {
        'form':form
    }
    data['html_form'] = render_to_string('pictures/image_create.html', context, request=request)
    return JsonResponse(data)

@login_required
def create_image_collection(request):
 
    data = dict()
    if request.method == "POST":
        collection_title = request.POST.get('collection-title')
        cover_index = int(request.POST.get('collection-cover-index'))
        if request.FILES is not None:
            images = [request.FILES.get('images[%d]' % i) for i in range(0, len(request.FILES))]
            parent_image = Images.objects.create(image_photo=images[cover_index], author=request.user, is_collection=True, description=collection_title)
            parent_image.save()
            images.pop(cover_index)
            for i in images:
                image_instance = Images.objects.create(image_photo=i, parent_image=parent_image, author=request.user)
                image_instance.save()
        data['collection_created'] = True
        data['collection_object'] =  render_to_string('pictures/new_image.html', {'image':parent_image}, request=request)
        data['collection_count'] = parent_image.author.images.filter(is_collection=True, parent_image=None).count()
    else:
        data['html_form'] = render_to_string('pictures/collection_create.html', {}, request=request)
    return JsonResponse(data)       
            
@login_required
def delete_image(request, hashed_id):
    data = dict()
    id = hashedId_image.decode(hashed_id)[0]
    image = get_object_or_404(Images, id=id)
    if request.method == "POST" and request.user.is_authenticated and request.user == image.author:
        user = image.author
        image.delete()
        data['image_deleted_successfully'] = True
        data['img_count'] = user.images.filter(parent_image=None, is_collection=False).count()
        data['img_text'] = user.get_image_count_text()
        data['collection_count'] = user.images.filter(is_collection=True, parent_image=None).count()
    else:
        context = {
            'image':image
        }
        data['html_form'] = render_to_string('pictures/image_delete.html', context, request=request)
    return JsonResponse(data)

@login_required
def edit_image(request, hashed_id):
    
    data=dict()
    id = hashedId_image.decode(hashed_id)[0]
    image = get_object_or_404(Images, id=id)
    if request.method == "POST" and request.user.is_authenticated and request.user == image.author: 
        form = ImagesForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            data['edited_successfully'] = True
            data['new_description'] = image.description
            data['tags'] = list(image.tags.all().values('name','slug'))
        else:
            data['edited_successfully'] = False
        return JsonResponse(data)
    else:
        form = ImagesForm(instance=image)
        form.instance.author = request.user
        context = {
            'form':form,
            'image':image,
            'is_update':True
        }
        data['html_form'] = render_to_string('pictures/image_create.html', context, request=request)
    return JsonResponse(data)

"""
Search results are divided into two categories of getting results on 
user type and results on a GET request. Search method only returns the top 
results based on a query as the user types and does not diplay additional 
data to the end user for each instance. Result method will return all relevant results. 
Users can also search for tags as a completed  search however, 
tags will not be updated live when user type in a query
"""
def search(request):
    
    data = dict()
    query = request.GET.get('q')
    show_result = request.GET.get('results')
    if query != None:
        data['profiles'] = list(Profile.objects.search(search_text=query).values('username','first_name','last_name')[:10])
        data['terms'] = list(SearchLog.objects.related_terms(term=query).values('text'))
        return JsonResponse(data)
    return {}

def results(request):
    query = request.GET.get('q')
    obj = request.GET.get('obj','images')
    users = images = None
    if obj == 'user':
        user_list = Profile.objects.search(search_text=query)  
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 20)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)  
    elif obj == 'images':
        image_list = Images.objects.search(search_text=query)   
        image_list.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(image_list, 20)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)  
    context = {
        'images':images,
        'users':users,
        'q':query
    }
    if request.user.is_authenticated: # check if user is authenticated to save search results
        if request.user.save_searches: # check is authenticated user allows search results to be saved under their name
            SearchLog.objects.create(text=query, profile=request.user)
    else:
        SearchLog.objects.create(text=query) # if above requirements weren't met save the search text only
    return render(request, 'pictures/search_result.html', context)

@login_required
def settings(request):
    if request.user.is_authenticated:
        return render(request, 'pictures/profile_settings/settings.html')
    
@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST,request.FILES, instance=request.user)
            storage = messages.get_messages(request)
            for _ in storage:
                pass
            for _ in list(storage._loaded_messages):
                del storage._loaded_messages[0]
            if form.is_valid():
                form.save()    
                messages.success(request,"All changes saved successfully")
            else:
                messages.error(request,"There was an error processing your request")
            return redirect('settings-personal')
        else:
            form = EditProfileForm(instance=request.user)        
        context = {
            'form':form,
            }
        return render(request, 'pictures/profile_settings/information.html', context)
        

@login_required
def privacy(request):
    if request.user.is_authenticated:
        searches = request.user.searches.all().order_by('-timestamp')
        if request.method=="POST":
            request.user.searches.clear()
            return redirect('settings-privacy')
        context = {
            'searches':searches
        }
        return render(request, 'pictures/profile_settings/privacy.html', context)