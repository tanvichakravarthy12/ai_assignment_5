# AI-Based Travel Planner

## Overview

AI-Based Travel Planner that generates personalized travel itineraries based on a user's destination, budget, interests, trip duration, and dietary preferences.

The system recommends attractions, food options, beverage pairings, and estimates trip costs to help users plan efficient and budget-friendly trips.

## Project Structure

### `travel.py`
Main program that collects user input, generates recommendations, creates the itinerary, and displays the final travel plan.

### `planner.py`
Creates day-by-day travel schedules based on destination, interests, and trip duration.

### `tourist_places.py`
Stores information about tourist attractions, including ratings, categories, entry fees, and visit details.

### `food.py`
Provides food recommendations based on destination and dietary preferences.

### `wine_ontology.py`
Suggests suitable beverage pairings for recommended meals.

### `cost.py`
Calculates estimated trip expenses and helps keep the itinerary within the user's budget.

## Features

- Personalized travel planning
- Attraction recommendations
- Food recommendations
- Beverage pairing suggestions
- Budget estimation
- Cost optimization
- Multi-day itinerary generation
- Interest-based activity selection

## How It Works

1. User enters trip details such as destination, duration, budget, interests, and diet.
2. The system recommends attractions that match the user's interests.
3. Food suggestions are generated based on dietary preferences.
4. Beverage pairings are recommended for selected meals.
5. A day-by-day itinerary is created.
6. Total trip cost is estimated.
7. Budget-friendly alternatives are suggested if needed.

## Example

### Input

```text
Destination: Kyoto
Duration: 3 Days
Budget: $600
Diet: Vegetarian
Interests: Culture, Food
```

### Output

```text
Day 1
- Morning: Fushimi Inari Shrine
- Afternoon: Nishiki Market
- Evening: Vegetarian Japanese Dinner

Recommended Beverage: Green Tea
Estimated Cost: $180
```

## Running the Project

Run the application:

```bash
python travel.py
```

## Conclusion

This project demonstrates how multiple knowledge bases can be combined to create intelligent travel recommendations. By considering user preferences, budget constraints, and destination-specific information, the system generates practical and personalized travel plans.
