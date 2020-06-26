from django.shortcuts import render, redirect
from .text_summarizer_v2 import generate_summary
from django.contrib import messages
# Create your views here.


def home(request):
    summarized_text = ''

    if request.method == 'POST':
        stuff = request.POST.get('stuff')
        num_of_lines = int(request.POST.get('num_of_lines'))
        try:
            summarized_text = generate_summary(stuff, num_of_lines)
        except IndexError:
            error = 'Number of sentences of summarized text cannot be greater than that of original text'
            messages.error(request, error)
            return redirect('home')
        request.session['summarized_text'] = summarized_text
        return redirect('answer')
    context = {
        'summarized_text': summarized_text,
    }
    return render(request, 'webapp/home.html', context)


def answer(request):
    summarized_text = request.session['summarized_text']
    context = {
        'summarized_text': summarized_text
    }
    return render(request, 'webapp/answer.html', context)
