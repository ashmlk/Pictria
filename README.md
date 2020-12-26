# Pictria

**[Pictria]** is a web application for sharing images and Collections (Multiple images at once). With the ability to Bookmark favourite images and like images as well.

> Pictria uses Heroku as a PaaS to run. The application runs on free Dyno's, which 
> go to sleep every 30 minutes of inactivity. In that case, please allow 10 seconds for the Dyno's to restart and load the website.
> The application also uses the free PostgreSQL tier on Heroku, which has a 10,000-row limit. Therefore, for demo purposes, the data is minimized as much as possible

### Datasets and API's

The inital data for this project was retrieved from [Unsplash API], which contains 25,000 images (Lite Version) including their tags, location, author and many other criteria.
The images and their relevant tags was used for populating the inital data for [Pictra]

### Motivation

Creating this project's motivation was to explore using Django with cloud technologies such AWS (S3) to create Pinterest Clone and explore the capabilities of Redis and Celery to create a lazy caching system to update regularly or in line to improve the loading time of webpages.

Technologies such as OAuth 2.0 are also used for user authentication using Google API and the application's default authentication.

This project's goal was to have an in-depth exploration of how companies like [Pinterest] handle an image CRUD system , large datasets, improve their user interactivity, reduce their general loading time per request, and use consistent UI/UX components to have a consistent UI across different pages.

## Features
  - Create an account or log in using your Google account
  - Create single image posts 
  - Create Collections, which which are posts that contain a maximum of 10 images
  - Add tags to your images 
  - Pages that contain the top, most, viewed and latest images from accross the website
  
### Tech

Pictria uses a number of frameworks:

* [Django (Python)] - For handeling the back end
* [PostgreSQL] - The database used in this application is PostgreSQL
* JavaScript - Libraries such as [jQuery] as well as technologies such as AJAX is used to build reusable front end components
* [Twitter Bootstrap] - great UI boilerplate for modern web apps


   [pictria]: <https://pictria.herokuapp.com>
   [Django (Python)]: <https://www.djangoproject.com/>
   [PostgreSQL]: <https://www.djangoproject.com/>
   [Unsplash API]: <https://unsplash.com/developers>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   
### Example screen shoots and examples

![image demo 1](https://github.com/ashmlk/Pictria/blob/master/image_demo_1.png)
![image demo 2](https://github.com/ashmlk/Pictria/blob/master/image_demo_2.png)
