from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import HashForm
from .models import Hash

from .utils import get_hash


def home(request):
    form = HashForm(initial={'algo': 'sha256'})
    text_hash = ''
    if request.method == 'POST':
        filledForm = HashForm(request.POST)
        if filledForm.is_valid():
            text = filledForm.cleaned_data['text']
            algo = filledForm.cleaned_data['algo']
            
            text_hash = get_hash(algo, text)

            try:
                Hash.objects.get(hash=text_hash, algo=algo)
            except Hash.DoesNotExist:
                hash = Hash()
                hash.algo = algo
                hash.hash = text_hash
                hash.text = text
                hash.save()

            return redirect('hash', hash=text_hash)
        
    return render(request, 'hashing/home.html', {'form': form, 'hash': text_hash})

def hash(request, hash):
    hash = Hash.objects.get(hash=hash)
    return render(request, 'hashing/hash.html', {'hash': hash})

def quickhash(request):
    text = request.GET['text']
    data = {'hash': get_hash('sha256', text)}
    return JsonResponse(data)
