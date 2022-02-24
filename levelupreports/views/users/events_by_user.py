"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all event along with the organizer first name, last name, and id
            # For the organizer
            db_cursor.execute("""
                select e.id, g.id as gamer_id, e.date, e.time, u.first_name, u.last_name
                from levelupapi_event e
                join levelupapi_gamer g on e.organizer_id = g.id
                join auth_user u on g.user_id = u.id
            """)
            
            # For Attendees
            # db_cursor.execute("""
            #     select e.id, g.id as gamer_id, e.date, e.time, u.first_name, u.last_name
            #     from levelupapi_event e
            #     join levelupapi_eventgamer eg on e.id = eg.event_id 
            #     join levelupapi_gamer g on eg.gamer_id = g.id
            #     join auth_user u on g.user_id = u.id
            # """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

           

            events_by_user = []

            for row in dataset:
                # TODO: write an event dictionary
                event = {
                    'id': row['id'],
                    'date': row['date'],
                    'time': row['time']
                }
                
                # This is using a generator comprehension to find the user_dict in the events_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in events_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                
                user_dict = next(
                    (
                        user_event for user_event in events_by_user
                        if user_event['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the event to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    # `${}`
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": f"{row['first_name']} {row['last_name']} ",
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
