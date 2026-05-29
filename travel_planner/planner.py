from places_db import Attraction, PlacesDatabase
from food import FoodRecommender

class TourPlannerEngine:
    def __init__(self, db, recommender):
        self.db = db
        self.recommender = recommender

    def generate_itinerary(self, destination, duration, interests, diet="none", alcohol=True):
        interests_lower = [i.lower().strip() for i in interests]
        
        # Rank attractions by heuristic score
        all_attractions = self.db.get_attractions_by_destination(destination)
        ranked_attractions = []
        for a in all_attractions:
            match_bonus = 25.0 if a.category.lower() in interests_lower else 0.0
            score = (a.rating * 10.0) + match_bonus
            ranked_attractions.append((score, a))
            
        ranked_attractions.sort(key=lambda x: x[0], reverse=True)
        available_attractions = [item[1] for item in ranked_attractions]

        # Select food options
        food_options = self.recommender.get_recommendations(destination, diet, alcohol)
        if not food_options:
            food_options = [{
                "dish_name": "Local Gastronomic Choice",
                "category": "Local",
                "description": "Sample local traditional cuisine at a trusted neighborhood tavern.",
                "cost": 25.0,
                "beverage_pairings": ["Local Beverage"]
            }]

        itinerary = []
        used_attractions = set()
        food_index = 0

        # Formulate itinerary
        for day in range(1, duration + 1):
            day_plan = {
                "day_number": day,
                "morning_activity": None,
                "lunch": None,
                "afternoon_activity": None,
                "dinner": None
            }
            
            # Morning activity
            morning_candidate = None
            for a in available_attractions:
                if a.name not in used_attractions and a.time_of_day == "Morning":
                    morning_candidate = a
                    break
            if not morning_candidate:
                for a in available_attractions:
                    if a.name not in used_attractions:
                        morning_candidate = a
                        break
            if morning_candidate:
                day_plan["morning_activity"] = morning_candidate
                used_attractions.add(morning_candidate.name)
            else:
                day_plan["morning_activity"] = Attraction(
                    name=f"Explore the Streets of {destination}",
                    destination=destination, category="Culture", cost=0.0, duration=2.0,
                    time_of_day="Morning", rating=4.5,
                    description="Spend the morning strolling through local streets, visiting small shops and cafes."
                )

            # Lunch
            day_plan["lunch"] = food_options[food_index % len(food_options)]
            food_index += 1

            # Afternoon activity
            afternoon_candidate = None
            for a in available_attractions:
                if a.name not in used_attractions and a.time_of_day == "Afternoon":
                    afternoon_candidate = a
                    break
            if not afternoon_candidate:
                for a in available_attractions:
                    if a.name not in used_attractions:
                        afternoon_candidate = a
                        break
            if afternoon_candidate:
                day_plan["afternoon_activity"] = afternoon_candidate
                used_attractions.add(afternoon_candidate.name)
            else:
                day_plan["afternoon_activity"] = Attraction(
                    name=f"Scenic Walking Tour in {destination}",
                    destination=destination, category="Nature", cost=0.0, duration=3.0,
                    time_of_day="Afternoon", rating=4.5,
                    description="Take a leisurely walking tour along picturesque neighborhood scenic spots."
                )

            # Dinner
            day_plan["dinner"] = food_options[food_index % len(food_options)]
            food_index += 1

            itinerary.append(day_plan)

        return {
            "destination": destination,
            "duration": duration,
            "interests": interests,
            "diet": diet,
            "alcohol": alcohol,
            "days": itinerary
        }
