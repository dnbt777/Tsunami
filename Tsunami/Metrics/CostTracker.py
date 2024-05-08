# Tracks costs across model requests

class CostTracker():
    def __init__(self):
        self.cost_data = [] # list of dicts
    

    def show_cost_data(self):
        # Initialize the total of all total costs
        total_of_totals = 0

        # Print header for clarity
        print(f"{'Index':<15} {'Input Cost':<15} {'Output Cost':<15} {'Total Cost':<15}")
        
        # Iterate through each cost item and print details
        for index, cost in enumerate(self.cost_data):
            print(f"{index:<15.4f} ${cost['input_cost']:<15.4f} ${cost['output_cost']:<15.4f} ${cost['total_cost']:<15.4f}")
            # Accumulate the total of total costs
            total_of_totals += cost['total_cost']

        # Print the total of all total costs
        print(f"\nCumulative cost: ${total_of_totals:<10.4f}")



    def add_request_metrics_to_cost_data(self, metrics_entry):
        request_cost_data = self.calculate_request_costs(
            metrics_entry["model"],
            metrics_entry["inputTokenCount"],
            metrics_entry["outputTokenCount"],
        )
        self.cost_data.append(request_cost_data)
    


    def calculate_request_costs(self, model, input_tokens, output_tokens):
        model_costs_per_1k_tokens = {
            "haiku" : {
                "input" : 0.00025,
                "output": 0.00125,
            },
            "sonnet" : {
                "input" : 0.003,
                "output": 0.015,
            },
            "opus" : {
                "input" : 0.015,
                "output": 0.075,
            },
        }
        model_costs = {
            model : {
                key: value / 1000 for key, value in costs.items()
            } for model, costs in model_costs_per_1k_tokens.items()
        }

        input_cost = model_costs[model]["input"]*input_tokens
        output_cost = model_costs[model]["output"]*output_tokens
        total_cost = input_cost + output_cost
        cost_data = {
            "input_cost" : input_cost,
            "output_cost" : output_cost,
            "total_cost" : total_cost,
            "model" : model,
        }
        return cost_data