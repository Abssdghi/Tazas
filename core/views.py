from django.shortcuts import render
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Tag, Post
from user.models import Profile
import json
from django.contrib.auth.models import User
from .modules import chooser

all_tags = ['movie','music','digikala']

@csrf_exempt
def login_or_signup(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed!!'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
            
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'logged in'})
        else:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Invalid password'}, status=401)
            else:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                    return JsonResponse({'status': 'signed up and logged in'})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid or empty JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'logged out'})

def check_login(request):
    return JsonResponse({'logged_in': request.user.is_authenticated})

@login_required
def follow_tag(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
        
    if not user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to follow a tag.'}, status=401)
    
    try:
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        tag = Tag.objects.get(id=tag_id)
        profile.followed_tags.add(tag)
        return JsonResponse({'status': 'followed'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def unfollow_tag(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if not user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to unfollow a tag.'}, status=401)

    try:
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        tag = Tag.objects.get(id=tag_id)
        profile.followed_tags.remove(tag)
        return JsonResponse({'status': 'unfollowed'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_profile(request):
    profile = request.user.profile
    followed = list(profile.followed_tags.values('id', 'name'))
    return JsonResponse({
        'username': request.user.username,
        'avatar': profile.avatar.url if profile.avatar else None,
        'followed_tags': followed
    })

def get_tags(request):
    tags = list(Tag.objects.values('id', 'name'))
    return JsonResponse({'tags': tags})

def update_tags(tags):
    for tag_name in tags:
        tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
        
        Post.objects.filter(tag=tag_obj).delete()
        
        posts_data = chooser.choose(tag_name)
        
        for post_data in posts_data:
            Post.objects.create(
                title=post_data['title'],
                image_url=post_data['image_url'],
                desc=post_data['desc'],
                url=post_data['url'],
                tag=tag_obj
            )
  
def random_feed(request):
    update_tags(all_tags)
    posts = Post.objects.all()
    sample = random.sample(list(posts), min(20, len(posts)))
    result = [{'title': p.title, 'image':p.image_url, 'desc': p.desc, 'url': p.url, 'tag': p.tag.name} for p in sample]
    return JsonResponse({'feed': result})

@login_required
def custom_feed(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    tags = profile.followed_tags.all()
    result = []
    for tag in tags:
        posts = tag.posts.order_by('-id')[:10]
        result += [{'title': p.title, 'image':p.image_url, 'desc': p.desc, 'url': p.url, 'tag': tag.name} for p in posts]
    return JsonResponse({'feed': result})



def home_page(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')

def profile_page(request):
    return render(request, 'profile.html')