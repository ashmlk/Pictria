"""
This is an additional file not related to the main purpose of this project.
This file is to create dummy data for demonstration purposes. The data created in this file are 
created using the Faker library. 

One production phase data is transferred to live Postgres database, and running the methods on this file is not necessary. 

Methods in this file SHOULD NOT BE RAN ON PRODUCTION DATA. methods create dummy data from users.
This method generate over 120,000 row of data however, due to server limitations the project database will be scaled down to only contain 10,000 row of data form all field
"""

from faker import Faker
from pictures.models import Profile, Images
from taggit.models import Tag
import pandas as pd
import glob, random
from pictures.models import UnsplashCollections, UnsplashPhotos, UnsplashKeywords

faker = Faker()
    
# Method to create UnsplashPhoto object
def unsplash_photos(photo_id,photo_url,photo_image_url,photo_submitted_at,photo_featured,
                    photo_description,photographer_username,
                    photographer_first_name,photographer_last_name,photo_location_name,photo_location_country,
                    photo_location_city,ai_description,ai_primary_landmark_name):
    
    UnsplashPhotos.objects.create(photo_id=photo_id,photo_url=photo_url,photo_image_url=photo_image_url,photo_submitted_at=photo_submitted_at,photo_featured=photo_featured,
                    photo_description=photo_description,photographer_username=photographer_username,
                    photographer_first_name=photographer_first_name,photographer_last_name=photographer_last_name,photo_location_name=photo_location_name,photo_location_country=photo_location_country,
                    photo_location_city=photo_location_city,ai_description=ai_description,ai_primary_landmark_name=ai_primary_landmark_name)

# method to create unsplash collection object
def unsplash_collections(photo_id,title,collected_at):
    
    p = UnsplashPhotos.objects.get(photo_id=photo_id)
    UnsplashCollections.objects.create(photo=p, collection_title=title, photo_collected_at=collected_at)
    
# This is for demoing purposes only, construct Unsplash Photo objects to assign to Image object later
def create_unsplash_photos():
    path = 'static/unsplash-research-dataset-lite-latest/'
    doc = 'photos'
    datasets = {}
    files = glob.glob(path + doc + ".tsv*") 
    subsets = []
    for filename in files:
        df = pd.read_csv(filename, sep='\t', header=0)
    for row in  zip(df['photo_id'], df['photo_url'], df['photo_image_url'], 
                    df['photo_submitted_at'], df['photo_featured'], df['photo_description'], df['photographer_username'], 
                    df['photographer_first_name'], df['photographer_last_name'], df['photo_location_name'], df['photo_location_country'], 
                    df['photo_location_city'], df['ai_description'], df['ai_primary_landmark_name']):
        unsplash_photos(photo_id=row[0],photo_url=row[1],photo_image_url=row[2],photo_submitted_at=row[3],photo_featured=row[4],
                        photo_description=row[5],photographer_username=row[6],
                        photographer_first_name=row[7],photographer_last_name=row[8],photo_location_name=row[9],photo_location_country=row[10],
                        photo_location_city=row[11],ai_description=row[12],ai_primary_landmark_name=row[13])
        
        
def create_unsplash_collections():
    
    path = 'static/unsplash-research-dataset-lite-latest/'
    doc = 'collections'
    datasets = {}
    files = glob.glob(path + doc + ".tsv*") 
    subsets = []
    for filename in files:
        df = pd.read_csv(filename, sep='\t', header=0)
    for row in  zip(df['photo_id'],df['collection_title'], df['photo_collected_at']):
        unsplash_collections(photo_id=row[0],title=row[1],collected_at=row[2])

# this method is used to create fake username - usernames maybe irrelevant to the user based on this method
def generate_username():
    return faker.profile(fields=['username'])['username']

# this method creates dummy data for users (10000 users)
def create_users():
    
    counter = 0 
    while counter <= 10000:
        try:
            Profile.objects.create(first_name=faker.first_name(), last_name=faker.last_name(), email=faker.ascii_free_email(), username=generate_username())
            counter += 1
        except:
            pass
    return 'success'

# the UnsplashPhotos model is just for demonstration puposes and will not be used by real-time users. this method
# create ImageObjects which users interact with using data collected from UnsplashAPI 
# data is displayed for demo 
def create_random_images():
    
    ids = [u.id for u in Profile.objects.all()]
    unsplash_ids = [p.photo_id for p in UnsplashPhotos.objects.all()]
    chosen_unsplash = []
    for _ in range(10000):
        random_id = random.choice(ids)
        random_photo = random.choice(unsplash_ids)
        Images.objects.create(author=Profile.objects.get(id=random_id),unsplash_photo=UnsplashPhotos.objects.get(photo_id=random_photo))
    return 'success'

# Image objects are not associated with collection objects 
# Images have tags - this method created tags for images retrieved from UnsplashAPI
def assign_collections():
    for i in Images.objects.all():
        if i.unsplash_photo!=None:
            cs = i.get_unsplash_collection_title()
            if cs != None:
                for c in cs:
                    i.tags.add(c)
            i.save()
    return 'success'

# generate random likes for images (DO NOT RUN ON PRODUCTION)
def rand_likes():
    ids = [u.id for u in Profile.objects.all()]
    for i in Images.objects.all():
        random_profile_count = random.randint(50, 10000) 
        rand_profiles = random.sample(ids, random_profile_count)
        for p in Profile.objects.filter(id__in=rand_profiles):
            i.likes.add(p)

# generate random views (DO NO RUN ON PRODUCTION)
def rand_views():
    ids = [u.id for u in Profile.objects.all()]
    for i in Images.objects.all():
        random_profile_count = random.randint(50, 4000) 
        rand_profiles = random.sample(ids, random_profile_count)
        for p in Profile.objects.filter(id__in=rand_profiles):
            i.views.add(p)   

# fix dummy username to be related to user
def fix_usernames():
    for p in Profile.objects.all():
        p.username = p.first_name.strip().lower() + p.last_name.strip().lower() + str(random.randint(100,10000))
        p.save()
    return 'success'

                
            