from django.shortcuts import render, redirect
from .forms import PictureForm
from .models import Picture, Album
import re
from django.contrib import messages


def album_save(request):
    if request.method == "GET":
        return redirect('/')
    if not request.user.is_authenticated():
        return redirect('/')
    name = request.POST['album-name']
    e = Album(name=name)
    e.save()
    return redirect('/edit-album/' + str(e.id))


def album_edit(request, album_id):
    pic = PictureForm()
    album_id = int(album_id)
    album = Album.objects.get(id=album_id)
    pictures = Picture.objects.filter(album=album)
    return render(request, 'edit_album.html', {'pictures': pictures, 'album': album, 'picform': pic})


def album_delete(request):
    if request.method == "GET":
        return redirect('/')
    if not request.user.is_authenticated():
        return redirect('/')
    album_id = request.POST['album-delete']
    Album.objects.get(pk=album_id).delete()
    messages.add_message(request, messages.SUCCESS, 'Álbum deletado!')
    return redirect('/config/')


def add_pictures(request):
    if request.method == "GET":
        return redirect('/')
    if not request.user.is_authenticated():
        return redirect('/')
    id = request.POST['album-id']
    for post in request.POST:
        if re.findall(r'name', post) and request.POST[post] != '':
            p = Picture(album=Album.objects.get(pk=id), url=request.POST[post])
            p.save()
    return redirect('/edit-album/' + id)


def remove_pictures(request):
    if request.method == "GET":
        return redirect('/')
    if not request.user.is_authenticated():
        return redirect('/')
    album_id = request.POST['album-id']
    picture_id = request.POST['picture-id']
    Picture.objects.get(pk=picture_id).delete()
    return redirect('/edit-album/' + album_id)
