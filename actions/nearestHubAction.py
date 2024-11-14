import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionFindNearestHub(Action):

    def name(self) -> Text:
        return "action_find_nearest_hub"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's location
        location = tracker.get_slot("location") 

        if not location:
            dispatcher.utter_message(text="Kindly provide your location.")
            return []   
        
        try:
            with open('data/locations_to_hubs.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['location_name'].lower() == location.lower():
                        nearest_hub = row['nearest_hub']
                        #set the nearest_hub slot
                        # dispatcher.utter_message(template="utter_confirm_nearest_hub", nearest_hub=nearest_hub)
                        return [SlotSet("nearest_hub", nearest_hub)]
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I couldn't find the locations data.")
            return []
        
        #if no matching location is found
        dispatcher.utter_message(text="Sorry, I couldn't find the nearest hub to your location.")
        return []
    

