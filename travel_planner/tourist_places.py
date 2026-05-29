class Attraction:
    def __init__(self, name, destination, category, cost, duration, time_of_day, rating, description):
        self.name = name
        self.destination = destination
        self.category = category
        self.cost = cost
        self.duration = duration
        self.time_of_day = time_of_day
        self.rating = rating
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "destination": self.destination,
            "category": self.category,
            "cost": self.cost,
            "duration": self.duration,
            "time_of_day": self.time_of_day,
            "rating": self.rating,
            "description": self.description
        }


class PlacesDatabase:
    def __init__(self):
        self.attractions = []
        self._populate_database()

    def add_attraction(self, att):
        self.attractions.append(att)

    def get_attractions_by_destination(self, destination):
        # Filter destination
        res = []
        for a in self.attractions:
            if a.destination.lower() == destination.lower():
                res.append(a)
        return res

    def get_destinations(self):
        # Get list of destinations
        dests = set()
        for a in self.attractions:
            dests.add(a.destination)
        return sorted(list(dests))

    def _populate_database(self):
        raw_data = [
            # Kyoto
            Attraction(
                name="Fushimi Inari Shrine",
                destination="Kyoto",
                category="Culture",
                cost=0.0,
                duration=3.0,
                time_of_day="Morning",
                rating=4.9,
                description="Hike through the iconic path of thousands of vibrant red Torii gates."
            ),
            Attraction(
                name="Kinkaku-ji (Golden Pavilion)",
                destination="Kyoto",
                category="Culture",
                cost=5.0,
                duration=1.5,
                time_of_day="Morning",
                rating=4.8,
                description="A breathtaking Zen temple covered in gold leaf, reflecting over a tranquil pond."
            ),
            Attraction(
                name="Arashiyama Bamboo Grove Walk",
                destination="Kyoto",
                category="Nature",
                cost=0.0,
                duration=2.0,
                time_of_day="Morning",
                rating=4.7,
                description="Stroll through towering paths of swaying green bamboo shoots."
            ),
            Attraction(
                name="Traditional Tea Ceremony in Gion",
                destination="Kyoto",
                category="Culture",
                cost=40.0,
                duration=1.5,
                time_of_day="Afternoon",
                rating=4.8,
                description="Experience the meditative art of authentic Matcha preparation in a historic tea house."
            ),
            Attraction(
                name="Kyoto Nishiki Market Food Tour",
                destination="Kyoto",
                category="Foodie",
                cost=75.0,
                duration=3.0,
                time_of_day="Evening",
                rating=4.9,
                description="Sample local street food like octopus skewers, sweet tamagoyaki, and fresh sashimi."
            ),
            Attraction(
                name="Fushimi Sake District Brewery Tour",
                destination="Kyoto",
                category="Foodie",
                cost=30.0,
                duration=2.0,
                time_of_day="Afternoon",
                rating=4.7,
                description="Visit centuries-old wooden sake breweries along willow-lined canals, with sake flight tasting."
            ),

            # Napa Valley
            Attraction(
                name="Sunrise Hot Air Balloon Flight",
                destination="Napa Valley",
                category="Adventure",
                cost=250.0,
                duration=3.0,
                time_of_day="Morning",
                rating=4.9,
                description="Soar high above the morning mist and sweeping vineyard lines of the valley."
            ),
            Attraction(
                name="Beringer Vineyards Estate Tour",
                destination="Napa Valley",
                category="Foodie",
                cost=60.0,
                duration=2.0,
                time_of_day="Morning",
                rating=4.8,
                description="Tour historical wine tunnels and taste premium Cabernet Sauvignon and Chardonnay."
            ),
            Attraction(
                name="Napa Valley Wine Train",
                destination="Napa Valley",
                category="Foodie",
                cost=180.0,
                duration=3.0,
                time_of_day="Afternoon",
                rating=4.7,
                description="A luxury vintage train journey through wine country featuring a multi-course gourmet lunch."
            ),
            Attraction(
                name="Hiking in Skyline Wilderness Park",
                destination="Napa Valley",
                category="Nature",
                cost=6.0,
                duration=3.0,
                time_of_day="Morning",
                rating=4.6,
                description="Trek through rolling hillsides with broad views of Napa Valley and Mount Diablo."
            ),
            Attraction(
                name="Calistoga Natural Mud Baths & Spa",
                destination="Napa Valley",
                category="Relaxation",
                cost=120.0,
                duration=2.5,
                time_of_day="Afternoon",
                rating=4.8,
                description="Unwind in mineral-rich volcanic ash mud baths, geothermal pools, and steam rooms."
            ),
            Attraction(
                name="Castello di Amorosa Castle Tour",
                destination="Napa Valley",
                category="Foodie",
                cost=45.0,
                duration=2.0,
                time_of_day="Afternoon",
                rating=4.8,
                description="Explore an authentic 13th-century style Italian castle with deep brick wine cellars."
            ),

            # Tuscany
            Attraction(
                name="Florence Uffizi Gallery Tour",
                destination="Tuscany",
                category="Culture",
                cost=35.0,
                duration=3.0,
                time_of_day="Morning",
                rating=4.9,
                description="Marvel at iconic Renaissance masterpieces by Botticelli, Michelangelo, and Da Vinci."
            ),
            Attraction(
                name="Tuscan Truffle Hunting Experience",
                destination="Tuscany",
                category="Foodie",
                cost=110.0,
                duration=3.0,
                time_of_day="Morning",
                rating=4.9,
                description="Hunt truffles in forests with trained dogs, followed by a luxurious truffle-paired farm lunch."
            ),
            Attraction(
                name="Leaning Tower of Pisa Climb",
                destination="Tuscany",
                category="Culture",
                cost=22.0,
                duration=2.0,
                time_of_day="Afternoon",
                rating=4.7,
                description="Ascend the famous tilted marble bell tower in the Square of Miracles."
            ),
            Attraction(
                name="Wine Tasting in Chianti Hills",
                destination="Tuscany",
                category="Foodie",
                cost=55.0,
                duration=2.5,
                time_of_day="Afternoon",
                rating=4.8,
                description="Visit a rustic Tuscan farmhouse to taste authentic Chianti Classico, olive oil, and cured meats."
            ),
            Attraction(
                name="Cycling in Val d'Orcia",
                destination="Tuscany",
                category="Nature",
                cost=25.0,
                duration=4.0,
                time_of_day="Morning",
                rating=4.8,
                description="Ride a bicycle through postcard landscapes of cypress-lined roads and wheat hills."
            ),
            Attraction(
                name="Tuscan Farmhouse Cooking Masterclass",
                destination="Tuscany",
                category="Foodie",
                cost=90.0,
                duration=4.0,
                time_of_day="Evening",
                rating=4.9,
                description="Learn the family secrets of rolling hand-made pici pasta and cooking traditional sauces from scratch."
            ),

            # Paris
            Attraction(
                name="Louvre Museum Guided Entry",
                destination="Paris",
                category="Culture",
                cost=25.0,
                duration=3.5,
                time_of_day="Morning",
                rating=4.9,
                description="View global treasures like the Mona Lisa and Winged Victory of Samothrace."
            ),
            Attraction(
                name="Eiffel Tower Summit Access",
                destination="Paris",
                category="Culture",
                cost=30.0,
                duration=2.5,
                time_of_day="Afternoon",
                rating=4.8,
                description="Take the glass lifts to the top floor summit to gaze at unmatched panoramic views of Paris."
            ),
            Attraction(
                name="Palace of Versailles Day Tour",
                destination="Paris",
                category="Culture",
                cost=45.0,
                duration=5.0,
                time_of_day="Morning",
                rating=4.8,
                description="Roam the grand Hall of Mirrors and the vast landscaped royal gardens of Louis XIV."
            ),
            Attraction(
                name="Seine River Evening Dinner Cruise",
                destination="Paris",
                category="Foodie",
                cost=95.0,
                duration=2.5,
                time_of_day="Evening",
                rating=4.8,
                description="Float past illuminated river monuments while dining on a premium 3-course French meal."
            ),
            Attraction(
                name="Parisian Bakery & Pastry Walk",
                destination="Paris",
                category="Foodie",
                cost=65.0,
                duration=2.5,
                time_of_day="Morning",
                rating=4.9,
                description="Go behind-the-scenes at a boutique boulangerie to smell fresh baguettes and taste macarons."
            ),
            Attraction(
                name="Luxembourg Gardens Stroll",
                destination="Paris",
                category="Nature",
                cost=0.0,
                duration=1.5,
                time_of_day="Afternoon",
                rating=4.7,
                description="Walk past gravel paths, fountains, and flower beds in Paris's most beautiful public park."
            )
        ]
        for item in raw_data:
            self.add_attraction(item)
