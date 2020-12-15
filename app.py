#handle complaints
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

def avoid_redundant_complaints():
    users = db.child("powercutfinalyearproject").get()
    users_notification = db.child("notification").get()
    todisplay_powercut_reason = []
    toupdate_powercut_region =[]  #will keep uniique id 
    already_filled_powercut_region = []
    for element in users.val():
        print(element)
        entry_data = users.val()[element]
        if entry_data['reasonforpowercut'] == " ":
            if entry_data['sublocation'] and entry_data['sublocation'] not in todisplay_powercut_reason:
                todisplay_powercut_reason.append(entry_data['sublocation'])
                toupdate_powercut_region.append(element)
        else:
            already_filled_powercut_region.append(element)
    print(todisplay_powercut_reason)
    cnt = -1
    for element_powercut in todisplay_powercut_reason:
        cnt = cnt + 1
        for elements in already_filled_powercut_region:
            element = users.val()[elements]
#            print("I am element",element)
            if element_powercut == element['sublocation']:
                print("I am element",element)
                if( len(element['timeofpowerrestore']) > 1 and len(element['dateofpowerrestore']) > 1):
                    print(element['timeofpowerrestore'].split(" ")[0])         
                    print(int(element['timeofpowerrestore'].split(":")[0]))
                    print(element['dateofpowerrestore'].split("-")[2])            
                    print(int(element['dateofpowerrestore'].split("-")[2]))
                    print(element['sublocation'])
                if element['reasonforpowercut'] != " " and element['timeofpowerrestore']!=" " and int(element['timeofpowerrestore'].split(":")[0]) >=  pd.datetime.now().hour and  element['sublocation'] == element_powercut and int(element['dateofpowerrestore'].split("-")[2]) >= (pd.datetime.now().day) and int(element['dateofpowerrestore'].split("-")[1]) >= (pd.datetime.now().month):
                    print("Gonna Update database")
                    print(element)
                    db.child('powercutfinalyearproject').child(toupdate_powercut_region[cnt]).update({'dateofpowerrestore' : element['dateofpowerrestore']})
                    db.child('powercutfinalyearproject').child(toupdate_powercut_region[cnt]).update({'timeofpowerrestore' : element['timeofpowerrestore']})
                    db.child('powercutfinalyearproject').child(toupdate_powercut_region[cnt]).update({'reasonforpowercut' : element['reasonforpowercut']})
                    print("db updated")
                    push_service = FCMNotification(api_key="AAAAQNdHX5E:APA91bHZUhNaowqjs_HajURjzS2HfuMofyiZTOojawhdjOvpK2IFI817sDeVZyXLZRBQJDv4bqjRnP_N6ElG-O1HlLwGBsoxG7ZZP3AQ-fOF8v7347kiACr7R2AHGClRKUubh20dcn5w")
                    message_title = "Power cut notification"
                    token_key = set()
                    message_body = " Hi powercut reason is " +  entry_data['reasonforpowercut'] + " powercut restore time is " + entry_data['timeofpowerrestore'] + "your region " +  entry_data['sublocation'] + " Thank you "
                    for elements_notification in users_notification.val():
                        if users_notification.val()[elements_notification].split(" ")[1] == entry_data['sublocation']:
                            token_key.add(users_notification.val()[elements_notification].split(" ")[0])
                    for token in token_key:  
                        result = push_service.notify_single_device(registration_id=token, message_title=message_title, message_body=message_body)
    return "Refreshed"



if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(to_avoid_future_complain_whose_response_available, 'interval', seconds=10)            
    scheduler.start()
