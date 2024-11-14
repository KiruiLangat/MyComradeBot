import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionProvideFinalDirections(Action):
    def name(self) -> Text:
        return "action_provide_final_directions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        near_destination_hub = tracker.get_slot("near_destination_hub")
        destination = tracker.get_slot("destination")

        if not near_destination_hub or not destination:
            dispatcher.utter_message(text="Please provide both your current location and where you want to go.")
            return []
        
        try:
            with open('data/final_directions.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['near_destination_hub'].lower() == near_destination_hub.lower() and row['destination'].lower() == destination.lower():
                        final_directions = row['final_directions']
                        dispatcher.utter_message(text=f"The {destination} is {final_directions} the {near_destination_hub}. Was  this helpful?")
                        return []
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I couldn't find the final directions data.")
            return []
        
        #if no matching final directions is found
        dispatcher.utter_message(text="Sorry, I couldn't find the final directions from {near_destination_hub} to {destination}.")
        return []
    
