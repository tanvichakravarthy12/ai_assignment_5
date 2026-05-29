import time
import os
import sys
from wine import SemanticOntology
from places_db import PlacesDatabase
from food import FoodRecommender
from planner import TourPlannerEngine
from cost import CostEstimator

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(f"\n=== {title} ===")

def get_input_choice(prompt, options, default=1):
    while True:
        try:
            choice = input(f"{prompt} (Default: {default}): ").strip()
            if not choice:
                return default
            for idx, opt in enumerate(options):
                if str(opt).lower() == choice.lower() or choice.lower() in str(opt).lower():
                    return idx + 1
            val = int(choice)
            if 1 <= val <= len(options):
                return val
            print(f"Invalid option. Choose 1 to {len(options)}.")
        except ValueError:
            print("Invalid input. Enter a number or name.")

def run_non_interactive(destination, duration, budget_style, max_budget, diet, alcohol, interests):
    ontology = SemanticOntology()
    db = PlacesDatabase()
    recommender = FoodRecommender(ontology)
    engine = TourPlannerEngine(db, recommender)
    cost_estimator = CostEstimator(db)
    
    supported = ["Kyoto", "Napa Valley", "Tuscany", "Paris"]
    is_supported = any(s.lower() == destination.lower() for s in supported)
            
    # Generate itinerary
    itinerary = engine.generate_itinerary(destination, duration, interests, diet, alcohol)
    
    # Calculate costs
    costs = cost_estimator.calculate_cost(itinerary, budget_style)
    
    # Optimize budget
    was_optimized = False
    original_total = costs["total_cost"]
    swap_log = []
    if original_total > max_budget:
        itinerary, swap_log = cost_estimator.optimize_itinerary(itinerary, costs, max_budget)
        costs = cost_estimator.calculate_cost(itinerary, budget_style)
        was_optimized = len(swap_log) > 0

    # Print plan
    print_header(f"TRIP PLAN: {destination.upper()}")
    if not is_supported:
        print(f"Note: '{destination}' is not preloaded. Using fallback plan.")
        
    print("\nSummary:")
    print(f"- Destination: {destination}")
    print(f"- Duration: {duration} Days")
    print(f"- Style: {budget_style}")
    print(f"- Diet: {diet}")
    print(f"- Drinks: {alcohol}")
    print(f"- Interests: {', '.join(interests)}")
    print(f"- Max Budget: ${max_budget}")

    # Daily itinerary
    for day in itinerary["days"]:
        print(f"\nDay {day['day_number']}:")
        m_act = day["morning_activity"]
        print(f"  Morning: {m_act.name} (${m_act.cost})")
        print(f"    Desc: {m_act.description}")
        
        lunch = day["lunch"]
        print(f"  Lunch: {lunch['dish_name']} (${lunch['cost']})")
        print(f"    Desc: {lunch['description']}")
        print(f"    Drinks: {', '.join(lunch['beverage_pairings'])}")
        
        a_act = day["afternoon_activity"]
        print(f"  Afternoon: {a_act.name} (${a_act.cost})")
        print(f"    Desc: {a_act.description}")
        
        dinner = day["dinner"]
        print(f"  Dinner: {dinner['dish_name']} (${dinner['cost']})")
        print(f"    Desc: {dinner['description']}")
        print(f"    Drinks: {', '.join(dinner['beverage_pairings'])}")

    # Expense sheet
    print("\nExpenses:")
    print(f"- Accommodation: ${costs['accommodation']}")
    print(f"- Transportation: ${costs['transportation']}")
    print(f"- Sightseeing: ${costs['sightseeing']}")
    print(f"- Dining: ${costs['dining']}")
    print(f"- Total Cost: ${costs['total_cost']}")
    
    status = "SUCCESS" if costs["total_cost"] <= max_budget else "WARNING (Exceeds budget)"
    print(f"- Status: {status}")
    
    if was_optimized:
        print(f"- Original Total: ${original_total}")
        print(f"- Savings: ${original_total - costs['total_cost']}")
        print("\nOptimizations:")
        for swap in swap_log:
            print(f"  Day {swap['day']}: Swapped '{swap['removed']}' for '{swap['added']}' (Saved ${swap['savings']})")

def run_planner_wizard():
    clear_screen()
    print_header("AI TRAVEL PLANNER WIZARD")
    
    ontology = SemanticOntology()
    db = PlacesDatabase()
    recommender = FoodRecommender(ontology)
    engine = TourPlannerEngine(db, recommender)
    cost_estimator = CostEstimator(db)
    
    # Destination
    destinations = db.get_destinations()
    print("Destinations:")
    for idx, d in enumerate(destinations):
        print(f"  [{idx + 1}] {d}")
    dest_idx = get_input_choice("Select destination", destinations, 1)
    destination = destinations[dest_idx - 1]

    # Duration
    while True:
        try:
            dur_in = input("Duration in days (1-14) (Default: 3): ").strip()
            if not dur_in:
                duration = 3
                break
            duration = int(dur_in)
            if 1 <= duration <= 14:
                break
            print("Must be between 1 and 14 days.")
        except ValueError:
            print("Enter a valid integer.")

    # Style
    styles = ["Budget", "Moderate", "Luxury"]
    print("\nStyles:")
    for idx, s in enumerate(styles):
        print(f"  [{idx + 1}] {s}")
    style_choice = get_input_choice("Select travel style", styles, 2)
    budget_style = ["budget", "moderate", "luxury"][style_choice - 1]

    # Budget limit
    default_budgets = {"budget": 120.0 * duration, "moderate": 300.0 * duration, "luxury": 800.0 * duration}
    default_max = default_budgets[budget_style]
    while True:
        try:
            budget_input = input(f"Max budget ($) (Default: {default_max}): ").strip()
            if not budget_input:
                max_budget = default_max
                break
            max_budget = float(budget_input)
            if max_budget > 0:
                break
            print("Must be positive.")
        except ValueError:
            print("Enter a valid number.")

    # Diet
    diets = ["None", "Vegetarian", "Vegan", "Gluten-Free"]
    print("\nDiets:")
    for idx, d in enumerate(diets):
        print(f"  [{idx + 1}] {d}")
    diet_choice = get_input_choice("Select diet", diets, 1)
    diet = ["none", "vegetarian", "vegan", "gluten-free"][diet_choice - 1]

    # Alcohol
    print("\nDrink options:")
    print("  [1] Yes (Alcohol)")
    print("  [2] No (Non-Alcoholic)")
    bev_choice = get_input_choice("Select drink type", [1, 2], 1)
    alcohol = (bev_choice == 1)

    # Interests
    categories = ["Culture", "Nature", "Adventure", "Relaxation", "Foodie"]
    print("\nInterests:")
    for idx, c in enumerate(categories):
        print(f"  [{idx + 1}] {c}")
    while True:
        try:
            int_in = input("Enter choices separated by commas (Default: 1, 5): ").strip()
            if not int_in:
                selected_idx = [1, 5]
                break
            parts = int_in.split(",")
            selected_idx = []
            for p in parts:
                p_clean = p.strip()
                matched_idx = None
                for idx, c in enumerate(categories):
                    if p_clean.lower() == c.lower():
                        matched_idx = idx + 1
                        break
                if matched_idx is not None:
                    selected_idx.append(matched_idx)
                else:
                    selected_idx.append(int(p_clean))
            if all(1 <= val <= len(categories) for val in selected_idx):
                break
            print("Invalid index choice.")
        except ValueError:
            print("Enter numbers or names separated by commas.")
            
    interests = [categories[idx - 1] for idx in selected_idx]

    # Compile
    print("\nCompiling plan...")
    time.sleep(0.5)
    
    itinerary = engine.generate_itinerary(destination, duration, interests, diet, alcohol)
    costs = cost_estimator.calculate_cost(itinerary, budget_style)
    
    was_optimized = False
    original_total = costs["total_cost"]
    swap_log = []
    if original_total > max_budget:
        print("Budget exceeded. Optimizing plan...")
        time.sleep(0.5)
        itinerary, swap_log = cost_estimator.optimize_itinerary(itinerary, costs, max_budget)
        costs = cost_estimator.calculate_cost(itinerary, budget_style)
        was_optimized = len(swap_log) > 0

    # Print results
    clear_screen()
    print_header(f"TRIP PLAN: {destination.upper()}")
    
    print("Summary:")
    print(f"- Destination: {destination}")
    print(f"- Duration: {duration} Days")
    print(f"- Style: {budget_style}")
    print(f"- Diet: {diet}")
    print(f"- Drinks: {alcohol}")
    print(f"- Interests: {', '.join(interests)}")
    print(f"- Max Budget: ${max_budget}")

    for day in itinerary["days"]:
        print(f"\nDay {day['day_number']}:")
        m_act = day["morning_activity"]
        print(f"  Morning: {m_act.name} (${m_act.cost})")
        print(f"    Desc: {m_act.description}")
        
        lunch = day["lunch"]
        print(f"  Lunch: {lunch['dish_name']} (${lunch['cost']})")
        print(f"    Desc: {lunch['description']}")
        print(f"    Drinks: {', '.join(lunch['beverage_pairings'])}")
        
        a_act = day["afternoon_activity"]
        print(f"  Afternoon: {a_act.name} (${a_act.cost})")
        print(f"    Desc: {a_act.description}")
        
        dinner = day["dinner"]
        print(f"  Dinner: {dinner['dish_name']} (${dinner['cost']})")
        print(f"    Desc: {dinner['description']}")
        print(f"    Drinks: {', '.join(dinner['beverage_pairings'])}")

    print("\nExpenses:")
    print(f"- Accommodation: ${costs['accommodation']}")
    print(f"- Transportation: ${costs['transportation']}")
    print(f"- Sightseeing: ${costs['sightseeing']}")
    print(f"- Dining: ${costs['dining']}")
    print(f"- Total Cost: ${costs['total_cost']}")
    
    status = "SUCCESS" if costs["total_cost"] <= max_budget else "WARNING (Exceeds budget)"
    print(f"- Status: {status}")
    
    if was_optimized:
        print(f"- Original Total: ${original_total}")
        print(f"- Savings: ${original_total - costs['total_cost']}")
        print("\nOptimizations:")
        for swap in swap_log:
            print(f"  Day {swap['day']}: Swapped '{swap['removed']}' for '{swap['added']}' (Saved ${swap['savings']})")
            
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["-h", "--help", "help"]:
            print("Usage: python travel_planner.py [Destination] [Duration] [Style] [MaxBudget] [Diet] [Alcohol] [Interests]")
            sys.exit(0)
            
        try:
            destination = sys.argv[1]
            duration = 3
            budget_style = "moderate"
            max_budget = 500.0
            diet = "none"
            alcohol = True
            interests = ["Culture", "Foodie"]
            
            if len(sys.argv) > 2:
                try:
                    duration = int(sys.argv[2])
                    if duration < 1: duration = 1
                except ValueError: pass
            
            if len(sys.argv) > 3:
                style_arg = sys.argv[3].lower()
                if style_arg in ["budget", "moderate", "luxury"]:
                    budget_style = style_arg
            
            if len(sys.argv) > 4:
                try: max_budget = float(sys.argv[4])
                except ValueError: pass
            else:
                default_budgets = {"budget": 120.0 * duration, "moderate": 300.0 * duration, "luxury": 800.0 * duration}
                max_budget = default_budgets.get(budget_style, 300.0 * duration)
            
            if len(sys.argv) > 5:
                diet_arg = sys.argv[5].lower()
                if diet_arg in ["none", "vegetarian", "vegan", "gluten-free"]:
                    diet = diet_arg
            
            if len(sys.argv) > 6:
                alcohol = sys.argv[6].lower() in ["yes", "true", "1", "y"]
            
            if len(sys.argv) > 7:
                interests = [i.strip() for i in sys.argv[7].split(",")]
            
            dest_clean = destination.lower()
            supported_dests = ["Kyoto", "Napa Valley", "Tuscany", "Paris"]
            for d in supported_dests:
                if d.lower() == dest_clean:
                    destination = d
                    break
            
            run_non_interactive(destination, duration, budget_style, max_budget, diet, alcohol, interests)
        except Exception as e:
            print(f"Error parsing CLI args ({e}). Running wizard instead...")
            time.sleep(1)
            while True:
                try: run_planner_wizard()
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    sys.exit(0)
    else:
        while True:
            try: run_planner_wizard()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                sys.exit(0)
