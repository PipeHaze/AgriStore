from django.shortcuts import render, get_object_or_404, redirect
from tiendita.models import Producto
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def new_conversation(request, slug):
    producto = get_object_or_404(Producto, slug=slug, en_stock=True,)

    if producto.creado_por == request.user:
        return redirect('tiendita:listado')
    
    conversations = Conversation.objects.filter(producto=producto).filter(members__in=[request.user.id])

    if conversations:
        pass #redirect to conversation

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(producto=producto)
            conversation.members.add(request.user)
            conversation.members.add(producto.creado_por)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('tiendita:producto_detalle', slug=slug)
    else:
        form = ConversationMessageForm()
        
    return render(request, 'conversacion/new.html', {
        'form': form
    })

@login_required

def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversacion/inbox.html', {
        'conversations': conversations
    })

def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversacion:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversacion/detail.html', {
        'conversation': conversation,
        'form': form
    })
    