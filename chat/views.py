from django.urls import reverse
import markdown2
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Conversation, Message
from openai import OpenAI
from django.conf import settings
from .prompt_templates import NEWS_SUMMARY_PROMPT

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('chat_list')
    return render(request, 'chat/landing.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing_page')

@login_required
def chat_list(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat/chat_list.html', {'conversations': conversations})

@login_required
def chat(request, conversation_id=None):
    # If conversation_id is None and it's not a new chat request, redirect to chat list
    if conversation_id is None and request.path != reverse('new_chat'):
        return redirect('chat_list')

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    else:
        # Only create new conversation if it's a new chat request
        conversation = Conversation.objects.create(
            user=request.user,
            title="New Summary"
        )

    chat_messages = Message.objects.filter(conversation=conversation).order_by('created_at')

    # Process markdown for each message
    for message in chat_messages:
        if message.is_bot:
            # Convert markdown to HTML and mark as safe
            message.content = mark_safe(markdown2.markdown(message.content))

    if request.method == 'POST':
        article_text = request.POST.get('article_text')
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            content=article_text,
            is_bot=False
        )

        try:
            # Generate summary using OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": NEWS_SUMMARY_PROMPT},
                    {"role": "user", "content": article_text}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content

            # Save bot response
            Message.objects.create(
                conversation=conversation,
                content=summary,
                is_bot=True
            )

            # Update conversation title with first line of summary
            first_line = summary.split('\n')[0][:100]  # Get first line, max 100 chars
            conversation.title = first_line
            conversation.save()

        except Exception as e:
            messages.error(request, f"Error generating summary: {str(e)}")
            print(f"Error: {str(e)}")  # For debugging

        return redirect('chat', conversation_id=conversation.id)

    return render(request, 'chat/chat.html', {
        'conversation': conversation,
        'chat_messages': chat_messages
    })

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted successfully!')
        return redirect('chat_list')
    
    # If it's not a POST request, return to chat list
    return redirect('chat_list')