#establshing connection with firbase database
import pyrebase
import matplotlib.pyplot as plt
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
from flask import Flask, render_template, request
from pyfcm import FCMNotification
config = {
    'apiKey': "AIzaSyBkh2OQfxMwvStAS027GaOvLPB_3WTMObQ",
    'authDomain': "powercutfinalyearproject.firebaseapp.com",
    'databaseURL': "https://powercutfinalyearproject.firebaseio.com",
    'projectId': "powercutfinalyearproject",
    'storageBucket': "powercutfinalyearproject.appspot.com",
    'messagingSenderId': "278489685905"
  }
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def notify_reason():
    users = db.child("powercutfinalyearproject").get()
    users_notification = db.child("notification").get()
    todisplay_powercut_reason = []
    for element in users.val():
        entry_data = users.val()[element]
        if entry_data['reasonforpowercut'] == " ":
            if entry_data['sublocation'] and entry_data['sublocation'] not in todisplay_powercut_reason:
                todisplay_powercut_reason.append(entry_data['sublocation'])
            
    return render_template("result.html",result = todisplay_powercut_reason)
        

@app.route('/result', methods = ['GET', 'POST'])
def notify_user():
    users = db.child("powercutfinalyearproject").get()
    users_notification = db.child("notification").get()
    token_key = set()
    if request.method == 'POST':
        result = request.form
        result_name = result['SBLC']
        result_timeofpowerrestore = result['TPRS']
        result_dateofpowerrestore = result['DPRC']
        result_reasonforpowercut = result['RPC']
        result_ans = " " + result_name + " " + result_timeofpowerrestore + " " + result_dateofpowerrestore + " " + result_reasonforpowercut
        for element in users.val():
            entry_data = users.val()[element]
            if entry_data['reasonforpowercut'] == " " and entry_data['sublocation'] == result_name:
                db.child('powercutfinalyearproject').child(element).update({'dateofpowerrestore' : result_dateofpowerrestore})
                db.child('powercutfinalyearproject').child(element).update({'timeofpowerrestore' : result_timeofpowerrestore})
                db.child('powercutfinalyearproject').child(element).update({'reasonforpowercut' : result_reasonforpowercut})
        push_service = FCMNotification(api_key="AAAAQNdHX5E:APA91bHZUhNaowqjs_HajURjzS2HfuMofyiZTOojawhdjOvpK2IFI817sDeVZyXLZRBQJDv4bqjRnP_N6ElG-O1HlLwGBsoxG7ZZP3AQ-fOF8v7347kiACr7R2AHGClRKUubh20dcn5w")
        message_title = "Power cut notification"
        message_body = " Hi powercut reason is :-" + result_reasonforpowercut + " powercut restore time is " + result_timeofpowerrestore + "your region " + result_name + " Thank you "
        for elements_notification in users_notification.val():
            sublocality = ""
            if len(users_notification.val()[elements_notification].split(" ")) > 3:
                sublocality = users_notification.val()[elements_notification].split(" ")[1] + " " + users_notification.val()[elements_notification].split(" ")[2]
            else:
                sublocality = users_notification.val()[elements_notification].split(" ")[1]
            print(sublocality)
            if sublocality == result_name:
                token_key.add(users_notification.val()[elements_notification].split(" ")[0])
        for token in token_key:  
            result = push_service.notify_single_device(registration_id=token, message_title=message_title, message_body=message_body)
            
        return result_ans

@app.route('/analyze1', methods = ['GET', 'POST'])
def fetch_graph_for_city():
    users = db.child("powercutfinalyearproject").get()
    dict_for_graph = {} 
    for user in users.val():
        dataset = users.val()[user]
        if dataset['reasonforpowercut'] != " ":
            hours = 0
            hours += int(dataset['timeofpowerrestore'].split(':')[0])-int(dataset['timeofpowercut'].split(':')[0])
            hours = int(hours) * 60
            hours += int(dataset['timeofpowerrestore'].split(':')[1])-int(dataset['timeofpowercut'].split(':')[1])
            if dataset['city'] in dict_for_graph.keys():
                dict_for_graph[ dataset['city']] += hours
            else:
                dict_for_graph[dataset['city']] = hours
    names = list(dict_for_graph.keys())
    values = list(dict_for_graph.values())

    plt.xlabel("City")
    plt.ylabel("TimeInMinutes")
    plt.bar(range(len(names)),values,tick_label=names)
    
    plt.savefig('static/sity.png')
            
@app.route('/analyze2', methods = ['GET', 'POST'])
def fetch_graph_for_state():
    users = db.child("powercutfinalyearproject").get()
    dict_for_graph_state = {} 
    for user in users.val():
        dataset = users.val()[user]
        if dataset['reasonforpowercut'] != " ":
            hours = 0
            hours += int(dataset['timeofpowerrestore'].split(':')[0])-int(dataset['timeofpowercut'].split(':')[0])
            hours = int(hours) * 60
            hours += int(dataset['timeofpowerrestore'].split(':')[1])-int(dataset['timeofpowercut'].split(':')[1])
            if dataset['state'] in dict_for_graph_state.keys():
                dict_for_graph_state[ dataset['state']] += hours
            else:
                dict_for_graph_state[dataset['state']] = hours
    names = list(dict_for_graph_state.keys())
    values = list(dict_for_graph_state.values())
    plt.bar(range(len(names)),values,tick_label=names)
    plt.xlabel("State")
    plt.ylabel("TimeInMinutes")
    plt.savefig('static/state.png')
            
    
@app.route('/displayallgraph', methods = ['GET','POST'])
def display():
    analysis1()
    analysis2()
    return render_template("display_result.html")

if __name__ == "__main__":
    app.run(debug=True)
    
