import csv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionProvideNavigation(Action):
    def name(self):
        return "action_provide_navigation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Get the 'location' slot value
        location = tracker.get_slot('location')

        # Get the latest intent to check for 'affirm' or 'deny'
        last_intent = tracker.get_intent_of_latest_message()

        # Check if we're waiting for affirmation
        confirmation_required = tracker.get_slot('confirmation_required')

        # Handle affirm/deny response
        if confirmation_required and last_intent in ["affirm", "deny"]:
            if last_intent == "affirm":
                dispatcher.utter_message(text="Great! Let's proceed with the directions.")
                # You could provide specific directions here.
                return []
            elif last_intent == "deny":
                dispatcher.utter_message(text="Alright, could you please specify which building or landmark you're close to?")
                return []

        # Proceed with normal flow if no confirmation needed
        if not location:
            dispatcher.utter_message(text="Could you please tell me where you're heading?")
            return []

        try:
            # Open the CSV file
            with open('actions/locations.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Match the location in the CSV with the user's requested location
                    if row['location_name'].lower() == location.lower():
                        landmarks = [row['landmark_1'], row['landmark_2'], row['landmark_3']]
                        # Filter out empty landmark fields
                        landmarks = [landmark for landmark in landmarks if landmark]
                        
                        if landmarks:
                            # Format the response with the available landmarks
                            response = f"The {location} is next to the {', the '.join(landmarks[:-1])}, and {landmarks[-1]}. Are you near any of these landmarks or buildings?"
                            # Set confirmation_required slot to True
                            return [SlotSet("confirmation_required", True)]
                        else:
                            response = f"The {location} doesn't have well-known landmarks around."

                        dispatcher.utter_message(text=response)
                        return []
                
                # If location not found in the CSV
                dispatcher.utter_message(text=f"Sorry, I don't have directions for {location}. Can you specify any nearby landmarks or buildings?")
                return []
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I'm having trouble accessing the location data. Please try again later.")
            return []

# Reset confirmation_required slot after getting affirm/deny
class ActionResetConfirmation(Action):
    def name(self):
        return "action_reset_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Reset the confirmation slot
        return [SlotSet("confirmation_required", None)]
