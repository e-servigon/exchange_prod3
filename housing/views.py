from django.shortcuts import render
import requests, uuid
from .forms import * 
from .models import *
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Create your views here.

def home(request):
    return render(request,'home.html',{})

def translate (request):
    translateform = TranslateTextsForm()
    context = {'translateform':translateform}

    if request.method == 'POST':

        translateform = TranslateTextsForm(request.POST)
        print(request.POST)
        print(request.POST.get('language_code_destiny'))
        print(request.POST.get('text_to_translate'))

        key = "0d3b56c51da84ab3b9bde995368a1f89"
        endpoint = "https://api.cognitive.microsofttranslator.com"
        location = "eastus"

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': 'es',
            'to': request.POST.get('language_code_destiny')
        }

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-type': 'application/json',
            'Ocp-Apim-Subscription-Region': location,
            'X-ClientTraceId': str(uuid.uuid4())
        }  

        body = [{
        'text': request.POST.get('text_to_translate')
        }]

        translate = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = translate.json()
        print(response)
        context['responsetranslate'] = response
        translate_row = TranslateTexts.objects.create(language_code_origin='es', language_code_destiny= request.POST.get('language_code_destiny'), text_to_translate= request.POST.get('text_to_translate'), text_translated =response )
        translate_row.save()

    return render(request,'translate.html',context)

def sentiment (request):
    analizeform = AnalyzeTextsForm()
    context = {'analyzeform':analizeform}

    if request.method == 'POST':
        analizeform = AnalyzeTextsForm(request.POST)
        print(request.POST)
        print(request.POST.get('text_to_analyze'))

        credential = AzureKeyCredential("1d962ca0288247929e1257678e4fbe83")
        endpoint="https://2023translatores.cognitiveservices.azure.com/"

        text_analytics_client = TextAnalyticsClient(endpoint, credential)

        documents = [
            request.POST.get('text_to_analyze')
        ]

        response = text_analytics_client.analyze_sentiment(documents, language="es")
        result = [doc for doc in response if not doc.is_error]

        print (result)

        for doc in result:
            print("overall sentiment:", doc.sentiment)
            context['sentimentresult'] = doc.sentiment
            sentiment_row = SentimentTexts.objects.create(text_to_analyze=request.POST.get('text_to_analyze'), result= doc.sentiment)
            sentiment_row.save()
    return render(request,'sentiment.html',context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)