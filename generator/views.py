import os
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from openai import OpenAI

# Initialize the OpenAI client from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
You are an expert content strategist for short and long form video platforms.
Given a user-provided video title and description, return a JSON object with three fields:
- optimized_title: a single SEO-friendly catchy title (<= 70 chars)
- optimized_description: a 2-3 sentence SEO-rich description including 1–3 short CTAs
- hashtags: a list of 8–10 relevant hashtags (no duplicates, include 1–2 local tags if region provided)

Input:
Title: {title}
Description: {description}
Platform: {platform}
Region: {region}

Respond ONLY with valid JSON.
Example:
{{"optimized_title": "...", "optimized_description": "...", "hashtags": ["#a","#b",...]}}
"""

def parse_model_response(text):
    """Safely parse the JSON-like model response."""
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except Exception:
        return None


@csrf_exempt
def ai_toolkit_view(request):
    """Main view for the CREFAS Creator Dashboard."""
    result, error = None, None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        platform = request.POST.get('platform', 'YouTube').strip()
        region = request.POST.get('region', '').strip()

        # Validate user input
        if not title or not description:
            messages.error(request, "Please provide both a title and description.")
            return render(request, 'generator/dashboard.html', {'result': None})

        # Prepare the structured prompt
        prompt = PROMPT_TEMPLATE.format(
            title=title,
            description=description,
            platform=platform,
            region=region or "Global"
        )

        # Query OpenAI model
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=500,
            )

            text = response.choices[0].message.content
            parsed = parse_model_response(text)

            if parsed:
                result = {
                    'optimized_title': parsed.get('optimized_title', '').strip(),
                    'optimized_description': parsed.get('optimized_description', '').strip(),
                    'hashtags': parsed.get('hashtags', []),
                }
            else:
                result = {'raw': text}
        except Exception as e:
            error = f"Error: {str(e)}"

    # Render result to dashboard.html
    return render(request, 'generator/dashboard.html', {
        'result': result,
        'error': error,
    })
