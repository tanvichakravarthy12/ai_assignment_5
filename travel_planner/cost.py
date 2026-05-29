from places_db import Attraction, PlacesDatabase

class CostEstimator:
    # Standard rates
    ACCOMMODATION_RATES = {
        "budget": 60.0,
        "moderate": 150.0,
        "luxury": 400.0
    }
    
    TRANSIT_RATES = {
        "budget": 15.0,
        "moderate": 35.0,
        "luxury": 95.0
    }

    def __init__(self, db):
        self.db = db

    def calculate_cost(self, itinerary, budget_style="moderate"):
        budget_style = budget_style.lower().strip()
        if budget_style not in self.ACCOMMODATION_RATES:
            budget_style = "moderate"
            
        duration = itinerary["duration"]
        sightseeing_cost = 0.0
        dining_cost = 0.0
        
        # Calculate daily costs
        for day in itinerary["days"]:
            sightseeing_cost += day["morning_activity"].cost
            sightseeing_cost += day["afternoon_activity"].cost
            dining_cost += day["lunch"]["cost"]
            dining_cost += day["dinner"]["cost"]

        accommodation_cost = self.ACCOMMODATION_RATES[budget_style] * duration
        transit_cost = self.TRANSIT_RATES[budget_style] * duration
        total_cost = sightseeing_cost + dining_cost + accommodation_cost + transit_cost
        
        return {
            "budget_style": budget_style,
            "sightseeing": sightseeing_cost,
            "dining": dining_cost,
            "accommodation": accommodation_cost,
            "transportation": transit_cost,
            "total_cost": total_cost
        }

    def optimize_itinerary(self, itinerary, cost_sheet, max_budget):
        if cost_sheet["total_cost"] <= max_budget:
            return itinerary, []

        destination = itinerary["destination"]
        available_alternatives = self.db.get_attractions_by_destination(destination)
        
        current_active_names = set()
        for day in itinerary["days"]:
            current_active_names.add(day["morning_activity"].name)
            current_active_names.add(day["afternoon_activity"].name)

        swap_log = []
        optimized_itinerary = dict(itinerary)
        
        # Filter available alternatives
        alternatives = [a for a in available_alternatives if a.name not in current_active_names]
        alternatives.sort(key=lambda x: x.cost)
        current_total = cost_sheet["total_cost"]

        # Swap loop
        while current_total > max_budget:
            highest_cost = -1.0
            highest_day_idx = -1
            highest_slot = None
            
            # Find target activity to swap
            for idx, day in enumerate(optimized_itinerary["days"]):
                m_act = day["morning_activity"]
                if m_act.cost > highest_cost and m_act.cost > 0:
                    has_cheaper = any(alt.cost < m_act.cost for alt in alternatives)
                    if has_cheaper:
                        highest_cost = m_act.cost
                        highest_day_idx = idx
                        highest_slot = "morning"

                a_act = day["afternoon_activity"]
                if a_act.cost > highest_cost and a_act.cost > 0:
                    has_cheaper = any(alt.cost < a_act.cost for alt in alternatives)
                    if has_cheaper:
                        highest_cost = a_act.cost
                        highest_day_idx = idx
                        highest_slot = "afternoon"

            if highest_day_idx == -1 or not alternatives:
                break

            target_day = optimized_itinerary["days"][highest_day_idx]
            if highest_slot == "morning":
                original_activity = target_day["morning_activity"]
            else:
                original_activity = target_day["afternoon_activity"]
            
            # Select cheapest alternative
            best_alt = None
            for alt in alternatives:
                if alt.cost < original_activity.cost:
                    best_alt = alt
                    break

            if not best_alt:
                break

            # Execute swap
            if highest_slot == "morning":
                target_day["morning_activity"] = best_alt
            else:
                target_day["afternoon_activity"] = best_alt

            alternatives.remove(best_alt)
            alternatives.append(original_activity)
            alternatives.sort(key=lambda x: x.cost)
            
            savings = original_activity.cost - best_alt.cost
            current_total -= savings
            
            swap_log.append({
                "day": highest_day_idx + 1,
                "slot": highest_slot.capitalize(),
                "removed": original_activity.name,
                "removed_cost": original_activity.cost,
                "added": best_alt.name,
                "added_cost": best_alt.cost,
                "savings": savings
            })
            
        return optimized_itinerary, swap_log
