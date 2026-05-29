class SemanticOntology:
    def __init__(self):
        # Triple store
        self.triples = []
        self._load_triples()

    def add_triple(self, subject, predicate, obj):
        self.triples.append((subject.strip(), predicate.strip(), obj.strip()))

    def _load_triples(self):
        # Beverages
        beverages = [
            ("Cabernet Sauvignon", "is_a", "Red Wine"),
            ("Chianti", "is_a", "Red Wine"),
            ("Bordeaux", "is_a", "Red Wine"),
            ("Chardonnay", "is_a", "White Wine"),
            ("Sauvignon Blanc", "is_a", "White Wine"),
            ("Champagne", "is_a", "Sparkling Wine"),
            ("Sake", "is_a", "Rice Wine"),
            ("Matcha Green Tea", "is_a", "Non-Alcoholic"),
            ("Sencha Green Tea", "is_a", "Non-Alcoholic"),
            ("Pomegranate Ginger Mocktail", "is_a", "Non-Alcoholic"),
            ("Lemon Mint Infusion", "is_a", "Non-Alcoholic"),
            ("Apple Cider Vinegar Spritzer", "is_a", "Non-Alcoholic"),
            ("Sparkling Apple Pomme", "is_a", "Non-Alcoholic"),
            ("Rosemary Berry Infusion", "is_a", "Non-Alcoholic"),
            ("Sparkling White Grape Mocktail", "is_a", "Non-Alcoholic"),
            ("Espresso Macchiato Mocktail", "is_a", "Non-Alcoholic"),
            ("Blackberry Thyme Shrub", "is_a", "Non-Alcoholic"),
            ("Cucumber Lavender Spritz", "is_a", "Non-Alcoholic"),
            ("Citrus Herb Tonic", "is_a", "Non-Alcoholic"),
            ("Raspberry Chocolate Infusion", "is_a", "Non-Alcoholic")
        ]
        for s, p, o in beverages:
            self.add_triple(s, p, o)

        # Region origins
        regions = [
            ("Sake", "produced_in", "Kyoto"),
            ("Matcha Green Tea", "produced_in", "Kyoto"),
            ("Sencha Green Tea", "produced_in", "Kyoto"),
            ("Cabernet Sauvignon", "produced_in", "Napa Valley"),
            ("Chardonnay", "produced_in", "Napa Valley"),
            ("Chianti", "produced_in", "Tuscany"),
            ("Bordeaux", "produced_in", "Paris"),
            ("Champagne", "produced_in", "Paris")
        ]
        for s, p, o in regions:
            self.add_triple(s, p, o)

        # Pairings
        pairings = [
            ("Red Meat", "pairs_with", "Red Wine"),
            ("Seafood", "pairs_with", "White Wine"),
            ("Sushi", "pairs_with", "Rice Wine"),
            ("Sushi", "pairs_with", "White Wine"),
            ("Vegetarian", "pairs_with", "White Wine"),
            ("Pasta", "pairs_with", "Red Wine"),
            ("Cheese", "pairs_with", "Red Wine"),
            ("Cheese", "pairs_with", "Sparkling Wine"),
            ("Dessert", "pairs_with", "Sparkling Wine"),
            ("Red Meat", "pairs_with_non_alc", "Pomegranate Ginger Mocktail"),
            ("Seafood", "pairs_with_non_alc", "Lemon Mint Infusion"),
            ("Sushi", "pairs_with_non_alc", "Sencha Green Tea"),
            ("Vegetarian", "pairs_with_non_alc", "Cucumber Lavender Spritz"),
            ("Pasta", "pairs_with_non_alc", "Sparkling White Grape Mocktail"),
            ("Cheese", "pairs_with_non_alc", "Sparkling Apple Pomme"),
            ("Dessert", "pairs_with_non_alc", "Raspberry Chocolate Infusion")
        ]
        for s, p, o in pairings:
            self.add_triple(s, p, o)

    def query(self, s=None, p=None, o=None):
        # Query triples
        results = []
        for subject, predicate, obj in self.triples:
            if s is not None and subject.lower() != s.lower():
                continue
            if p is not None and predicate.lower() != p.lower():
                continue
            if o is not None and obj.lower() != o.lower():
                continue
            results.append((subject, predicate, obj))
        return results

    def get_regional_specialties(self, destination, alcohol=True):
        # Get specialties
        specialties = []
        results = self.query(p="produced_in", o=destination)
        for drink, _, _ in results:
            drink_class = self.query(s=drink, p="is_a")[0][2]
            is_na = drink_class == "Non-Alcoholic"
            if alcohol and not is_na:
                specialties.append(drink)
            elif not alcohol and is_na:
                specialties.append(drink)
        return specialties

    def get_pairings_for_food(self, food_category, alcohol=True):
        # Get pairings
        pairings = []
        if alcohol:
            results = self.query(s=food_category, p="pairs_with")
            for _, _, target_class in results:
                drinks = self.query(p="is_a", o=target_class)
                for d, _, _ in drinks:
                    pairings.append(d)
        else:
            results = self.query(s=food_category, p="pairs_with_non_alc")
            for _, _, drink in results:
                pairings.append(drink)
        return pairings
