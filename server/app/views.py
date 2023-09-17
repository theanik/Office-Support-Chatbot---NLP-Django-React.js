from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
import datetime
import pandas as pd
from django.http.response import JsonResponse
from http import HTTPStatus
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
import json



def pong(request):
    return JsonResponse({"message" : 'Pong'})

def chat(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/index.html", {"room_name": room_name})

@csrf_exempt
def store_feedback(request):
    if request.method == "POST": # and request.headers['Signature'] == "1:1-bot"
        json_data = json.loads(request.body)
        feedback_data = json_data['feedbackData']
        file_name = os.path.join(settings.BASE_DIR, 'data/raw/notsatisfied/' + get_current_date_string() + '.csv')
        if "label" in feedback_data and "qcontext" in feedback_data and feedback_data["label"] and len(feedback_data["qcontext"]):
            if not os.path.exists(file_name):
                create_csv_file(file_name)
            append_row_to_csv(file_name, feedback_data["qcontext"], feedback_data["label"])
        print(feedback_data)
        return JsonResponse({'status':'true','message':'Feedback acknowledged!'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status':'false','message':'Method not allowed!'}, status=405)


def create_csv_file(filename):
    df = pd.DataFrame(columns=['question', 'predicted_label'])
    df.to_csv(filename, index=False)

def append_row_to_csv(filename, question, label):
    df = pd.read_csv(open(filename))
    if str(question) in df['question'].values:
        return
    df.loc[len(df)] = [question, label]
    df.to_csv(filename, index=False)

def get_current_date_string():
    x = datetime.datetime.now()
    return x.strftime("%d-%m-%y")