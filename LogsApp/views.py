from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404

def index(request):
    """ The home page for LogsApp """
    return render(request, 'LogsApp/index.html')

def topics(request):
    """ Show all topics. """
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'LogsApp/topics.html', context)

def topic(request, topic_id):
    """ Show a single topic and all its entries """
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'LogsApp/topic.html', context)

def new_topic(request):
    """ Add a new topic. """
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('LogsApp:topics')

    context = {'form': form}
    return render(request, 'LogsApp/new_topic.html', context)

def new_entry(request, topic_id):
    """ Add new entry for a particular topic """
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('LogsApp:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'LogsApp/new_entry.html', context)

def edit_entry(request, entry_id):
    """ Edit an existing entry """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('LogsApp:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'LogsApp/edit_entry.html', context)
