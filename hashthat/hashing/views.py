import hashlib

from django.shortcuts import render

from .forms import HashForm
from .models import Hash

def home(request):
    form = HashForm(initial={'algo': 'sha256'})
    text_hash = ''
    if request.method == 'POST':
        filledForm = HashForm(request.POST)
        if filledForm.is_valid():
            text = filledForm.cleaned_data['text']
            algo = filledForm.cleaned_data['algo']
            hashFunc = hashlib.new(algo)
            hashFunc.update(text.encode('utf-8'))
            text_hash = hashFunc.hexdigest()
            try:
                Hash.objects.get(hash=text_hash, algo=algo)
            except Hash.DoesNotExist:
                hash = Hash()
                hash.algo = algo
                hash.hash = text_hash
                hash.text = text
                hash.save()
        
    return render(request, 'hashing/home.html', {'form': form, 'hash': text_hash})

