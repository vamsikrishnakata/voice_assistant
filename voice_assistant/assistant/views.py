from django.shortcuts import render
from datetime import datetime
import pyjokes, requests, wikipedia, psutil
import json
from django.http import JsonResponse

# Chat history stored in session
def index(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    chat_history = request.session["chat_history"]
    response = ""

    if request.method == "POST":
        query = request.POST.get("query", "").lower().strip()

        response = process_query(query)

        # Save to chat history
        chat_history.append({"query": query, "response": response})
        request.session["chat_history"] = chat_history

    return render(request, "index.html", {"chat_history": chat_history})


# API endpoint for AJAX requests
def assistant_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query", "").lower().strip()
        response_text = process_query(query)
        return JsonResponse({"response": response_text})

    return JsonResponse({"response": "Invalid request"}, status=400)


# Helper function to process queries
def process_query(query):
    # Greetings
    if any(word in query for word in ["hello", "hi", "hey"]):
        return "Hello! How can I assist you today?"

    # Time & Date
    if "time" in query:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    if "date" in query:
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}"

    # Joke
    if "joke" in query:
        return pyjokes.get_joke()

    # Google & YouTube links
    if "google" in query:
        return '<a href="https://www.google.com" target="_blank">Open Google</a>'
    if "youtube" in query:
        return '<a href="https://www.youtube.com" target="_blank">Open YouTube</a>'
    # Instagram link
    if "instagram" in query:
        return '<a href="https://www.instagram.com" target="_blank">Open Instagram</a>'
    if "facebook" in query:
        return '<a href="https://www.facebook.com" target="_blank">Open Facebook</a>'
     



    # Battery status
    if "battery" in query:
        battery = psutil.sensors_battery()
        if battery:
            return f"Battery is at {battery.percent}%"
        return "Battery information not available."

    # Weather
    if "weather" in query:
        city = query.replace("weather in", "").replace("weather", "").strip() or "Hyderabad"
        api_key = "0b5ad24d8da1f2a202a13b75948fa17a"  # Your OpenWeather API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            data = requests.get(url).json()
            if data.get("cod") == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"The weather in {city} is {temp}°C with {desc}."
            return "Sorry, I couldn't fetch the weather."
        except:
            return "Weather service is unavailable."

    # Wikipedia
    if "wikipedia" in query:
        try:
            topic = query.replace("wikipedia", "").strip()
            return wikipedia.summary(topic, sentences=2)
        except:
            return "Sorry, I couldn't find anything on Wikipedia."

    # News
    if "news" in query:
        api_key = "YOUR_NEWS_API_KEY"  # Replace with your NewsAPI key
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
        try:
            data = requests.get(url).json()
            if "articles" in data:
                top_articles = [a["title"] for a in data["articles"][:3]]
                return "Top news: " + " | ".join(top_articles)
            return "Couldn't fetch news."
        except:
            return "News service unavailable."

    # Dictionary
    if "meaning of" in query or "define" in query:
        word = query.replace("meaning of", "").replace("define", "").strip()
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            data = requests.get(url).json()
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return f"The meaning of {word} is: {meaning}"
        except:
            return f"Sorry, I couldn't find the meaning of {word}."

    return "Sorry, I don't know that yet."
