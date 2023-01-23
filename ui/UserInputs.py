class UserInputs:

    def __init__(
            self,
            population_amount,
            epochs_amount,
            cross_probability,
            mutation_probability,
            selection_method,
            cross_method,
            mutation_method,
            maximum,
            elite_strategy,

    ):
        self.population_amount = population_amount
        self.epochs_amount = epochs_amount
        self.cross_probability = cross_probability
        self.mutation_probability = mutation_probability
        self.selection_method = selection_method
        self.cross_method = cross_method
        self.mutation_method = mutation_method
        self.maximum = maximum
        self.elite_strategy = elite_strategy
