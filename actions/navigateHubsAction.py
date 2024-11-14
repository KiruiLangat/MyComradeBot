import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionNavigateHubs(Action):
    def name(self) -> Text:
        return "action_navigate_hubs"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        #Extract the nearest hub and destination from the slots
        nearest_hub = tracker.get_slot("nearest_hub")
        destination = tracker.get_slot("destination")

        if not nearest_hub or not destination:
            dispatcher.utter_message(text="Please provide both your current location and where you want to go.")
            return []
        
        try:
            with open('data/hub_connections.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['current_hub'].lower() == nearest_hub.lower() and row['destination'].lower() == destination.lower():
                        near_destination_hub = row['near_destination_hub']
                        directions = row['directions']
                        #set the near_destination_hub slot
                        dispatcher.utter_message(text=f"Great! I'll guide you from the {nearest_hub} to the {near_destination_hub}, which is close to the {destination}. To navigate: {directions}.\n\n Let me know if you need any more help.")
                        return [SlotSet("near_destination_hub", near_destination_hub)]
                    
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I couldn't find the hubs connection data.")
            return []
        
        #if no matching hub connection is found
        dispatcher.utter_message(text="Sorry, I couldn't find the connection to the destination hub.")
        return []
    
