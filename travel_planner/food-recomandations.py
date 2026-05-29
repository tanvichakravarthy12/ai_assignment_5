from wine import SemanticOntology

class CulinaryDish:
    def __init__(self, name, destination, category, description,
                 is_vegetarian, is_vegan, is_gluten_free, cost_est):
        self.name = name
        self.destination = destination
        self.category = category
        self.description = description
        self.is_vegetarian = is_vegetarian
        self.is_vegan = is_vegan
        self.is_gluten_free = is_gluten_free
        self.cost_est = cost_est


class FoodRecommender:
    def __init__(self, ontology):
        self.ontology = ontology
        self.dishes = []
        self._populate_dishes()

    def add_dish(self, dish):
        self.dishes.append(dish)

    def _populate_dishes(self):
        raw_dishes = [
            # Kyoto
            CulinaryDish(
                name="Premium Sushi & Sashimi Platter",
                destination="Kyoto",
                category="Sushi",
                description="Freshly caught bluefin tuna, red snapper, and sweet shrimp served over vinegared rice.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=True,
                cost_est=60.0
            ),
            CulinaryDish(
                name="Buddhist Shojin Ryori (Kaiseki)",
                destination="Kyoto",
                category="Vegetarian",
                description="A delicate multi-course vegan meal showcasing seasonal vegetables, tofu, and mountain herbs.",
                is_vegetarian=True, is_vegan=True, is_gluten_free=True,
                cost_est=110.0
            ),
            CulinaryDish(
                name="Artisanal Tofu Tempura",
                destination="Kyoto",
                category="Vegetarian",
                description="Crispy, light-fried local silken tofu served with grated daikon and vegetarian broth.",
                is_vegetarian=True, is_vegan=True, is_gluten_free=False,
                cost_est=25.0
            ),
            CulinaryDish(
                name="Kyoto Matcha Parfait",
                destination="Kyoto",
                category="Dessert",
                description="Layers of rich Uji Matcha ice cream, sweet red bean paste, mochi balls, and matcha jelly.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=False,
                cost_est=12.0
            ),

            # Napa Valley
            CulinaryDish(
                name="Grilled Oakwood Prime Ribeye Steak",
                destination="Napa Valley",
                category="Red Meat",
                description="A thick, juicy prime ribeye steak grilled over aromatic oak wood, served with truffle butter.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=True,
                cost_est=65.0
            ),
            CulinaryDish(
                name="Pan-Seared Pacific Salmon",
                destination="Napa Valley",
                category="Seafood",
                description="Crispy skin salmon served over wild rice, asparagus, and a creamy citrus dill sauce.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=True,
                cost_est=38.0
            ),
            CulinaryDish(
                name="Wild Mushroom & Goat Cheese Flatbread",
                destination="Napa Valley",
                category="Vegetarian",
                description="Artisanal stone-baked flatbread topped with local goat cheese, roasted chanterelle mushrooms, and arugula.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=False,
                cost_est=28.0
            ),
            CulinaryDish(
                name="California Artisanal Cheese Board",
                destination="Napa Valley",
                category="Cheese",
                description="Selection of award-winning Northern California cheeses, served with organic honeycomb and grapes.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=True,
                cost_est=32.0
            ),

            # Tuscany
            CulinaryDish(
                name="Bistecca alla Fiorentina (Florentine Steak)",
                destination="Tuscany",
                category="Red Meat",
                description="A massive, dry-aged thick-cut T-bone steak grilled rare over olive wood embers, finished with sea salt.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=True,
                cost_est=80.0
            ),
            CulinaryDish(
                name="Tuscan Ribollita Vegetable Stew",
                destination="Tuscany",
                category="Vegetarian",
                description="A hearty, traditional Tuscan bread and vegetable soup slow-simmered with white cannellini beans, kale, and local olive oil.",
                is_vegetarian=True, is_vegan=True, is_gluten_free=True,
                cost_est=18.0
            ),
            CulinaryDish(
                name="Truffle Tagliatelle Pasta",
                destination="Tuscany",
                category="Pasta",
                description="Fresh, handmade egg tagliatelle tossed in a rich, buttery sauce containing shaved black truffles from San Miniato.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=False,
                cost_est=30.0
            ),
            CulinaryDish(
                name="Authentic Tuscan Tiramisu",
                destination="Tuscany",
                category="Dessert",
                description="Espresso-soaked ladyfingers layered with fresh sweetened mascarpone cheese and dusted with rich cocoa powder.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=False,
                cost_est=10.0
            ),

            # Paris
            CulinaryDish(
                name="Traditional French Beef Bourguignon",
                destination="Paris",
                category="Red Meat",
                description="Beef chuck slow-braised in rich Burgundy red wine, garlic, onions, carrots, fresh bouquet garni, and mushrooms.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=False,
                cost_est=45.0
            ),
            CulinaryDish(
                name="Provencal Ratatouille",
                destination="Paris",
                category="Vegetarian",
                description="A classic French vegetable stew slow-cooked with bell peppers, zucchini, eggplant, tomatoes, garlic, and fresh herbs.",
                is_vegetarian=True, is_vegan=True, is_gluten_free=True,
                cost_est=26.0
            ),
            CulinaryDish(
                name="Classic Marseille Bouillabaisse",
                destination="Paris",
                category="Seafood",
                description="A traditional rich saffron fish and seafood stew served with croutons and spicy garlic rouille sauce.",
                is_vegetarian=False, is_vegan=False, is_gluten_free=True,
                cost_est=55.0
            ),
            CulinaryDish(
                name="Grand Chocolate Soufflé",
                destination="Paris",
                category="Dessert",
                description="A fluffy, light-baked dark chocolate soufflé served warm with a scoop of Madagascar vanilla bean ice cream.",
                is_vegetarian=True, is_vegan=False, is_gluten_free=False,
                cost_est=14.0
            )
        ]

        for item in raw_dishes:
            self.add_dish(item)

    def get_recommendations(self, destination, diet="none", alcohol=True):
        diet = diet.lower().strip()
        matched_dishes = []

        # Filter matched dishes
        for d in self.dishes:
            if d.destination.lower() != destination.lower():
                continue
            if diet == "vegetarian" and not d.is_vegetarian:
                continue
            if diet == "vegan" and not d.is_vegan:
                continue
            if diet == "gluten-free" and not d.is_gluten_free:
                continue
            matched_dishes.append(d)

        recommendations = []
        for dish in matched_dishes:
            # Query drink pairings
            pairings = self.ontology.get_pairings_for_food(dish.category, alcohol=alcohol)
            if not pairings:
                pairings = self.ontology.get_regional_specialties(dish.destination, alcohol=alcohol)
                
            recommendations.append({
                "dish_name": dish.name,
                "category": dish.category,
                "description": dish.description,
                "cost": dish.cost_est,
                "diet_tags": {
                    "vegetarian": dish.is_vegetarian,
                    "vegan": dish.is_vegan,
                    "gluten_free": dish.is_gluten_free
                },
                "beverage_pairings": pairings
            })
        return recommendations
