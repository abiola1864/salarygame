



import pygambit as gbt

class AllocationGameGambit:
    def __init__(self):
        """
        Define a single-player allocation game using Pygambit.
        """
        self.total_amount = 10000
        self.game = gbt.Game.new_tree(players=["Allocator"],
                                     title="Strategic Allocation Game")
        self._setup_game_structure()

    def _setup_game_structure(self):
        """
        Set up the moves and outcomes for the allocation game.
        """
        self.game.append_move(self.game.root, "Allocator", [
            "Conservative",
            "Aggressive",
            "Innovative",
            "Sustainable",
            "Balanced"
        ])
        self._add_outcomes()

    def _add_outcomes(self):
        """
        Define outcomes for each strategy.
        """
        outcomes = {
            "Conservative": [8000, 7000],
            "Aggressive": [12000, 5000],
            "Innovative": [10000, 8000],
            "Sustainable": [7000, 9000],
            "Balanced": [9000, 7500]
        }

        for idx, (strategy, outcome) in enumerate(outcomes.items()):
            game_outcome = self.game.add_outcome(outcome, label=strategy)
            self.game.set_outcome(self.game.root.children[idx], game_outcome)

    def evaluate_allocation(self, allocations):
        """
        Evaluates the player's allocation strategy.
        """
        strategy = self._determine_strategy(allocations)
        outcome = self._get_strategy_outcome(strategy)
        
        return {
            'strategy': strategy,
            'monetary_outcome': outcome[0],
            'impact_score': outcome[1],
            'analysis': self._generate_analysis(allocations, strategy),
            'total_allocated': sum(allocations.values())
        }

    def _determine_strategy(self, allocations):
        """
        Determines the allocation strategy based on distribution.
        """
        total = sum(allocations.values())
        distribution = {k: (v/total) * 100 for k, v in allocations.items()}

        high_risk_categories = ['AI Research', 'Blockchain', 'Quantum Computing']
        sustainable_categories = ['Sustainable Tech', 'Environmental Conservation']
        
        high_risk_allocation = sum(distribution.get(cat, 0) 
                                 for cat in high_risk_categories)
        sustainable_allocation = sum(distribution.get(cat, 0) 
                                  for cat in sustainable_categories)

        if high_risk_allocation > 60:
            return "Aggressive"
        elif sustainable_allocation > 50:
            return "Sustainable"
        elif max(distribution.values()) > 40:
            return "Innovative"
        elif max(distribution.values()) < 25:
            return "Conservative"
        else:
            return "Balanced"

    def _get_strategy_outcome(self, strategy):
        """
        Returns the outcome for a given strategy.
        """
        outcomes = {
            "Conservative": [8000, 7000],
            "Aggressive": [12000, 5000],
            "Innovative": [10000, 8000],
            "Sustainable": [7000, 9000],
            "Balanced": [9000, 7500]
        }
        return outcomes.get(strategy, [9000, 7500])

    def _generate_analysis(self, allocations, strategy):
        """
        Generates analysis of the allocation.
        """
        strategy_insights = {
            "Conservative": "Lower risk with stable returns. Good for uncertain markets.",
            "Aggressive": "High potential returns but increased volatility.",
            "Innovative": "Good balance of innovation and stability.",
            "Sustainable": "Strong long-term impact focus with moderate returns.",
            "Balanced": "Well-rounded approach with good risk management."
        }
        
        analysis = [strategy_insights[strategy]]
        total = sum(allocations.values())
        
        for category, amount in allocations.items():
            percentage = (amount / total) * 100
            if percentage > 30:
                analysis.append(f"Heavy investment in {category} ({percentage:.1f}%)")
            elif percentage < 10:
                analysis.append(f"Conservative position in {category} ({percentage:.1f}%)")
                
        return analysis

# import pygambit as gbt

# class TrustGameGambit:
#     def __init__(self):
#         """
#         Define the Trust Game structure using Pygambit.
#         """
#         # Create a new game tree with Buyer and Seller
#         self.game = gbt.Game.new_tree(players=["Buyer", "Seller"],
#                                       title="One-shot Trust Game")
        
#         # Add Buyer's move with Trust and Not Trust actions
#         self.game.append_move(self.game.root, "Buyer", ["Trust", "Not trust"])
        
#         # Add Seller's move if Buyer chooses Trust
#         self.game.append_move(self.game.root.children[0], "Seller", ["Honor", "Abuse"])
        
#         # Add outcomes
#         # Not Trust outcome: Buyer gets 6000, Seller gets 0
#         not_trust_outcome = self.game.add_outcome([6000, 0], label="Opt-out")
#         self.game.set_outcome(self.game.root.children[1], not_trust_outcome)
        
#         # Trust + Honor outcome: Buyer gets 7200, Seller gets 2000
#         trust_honor_outcome = self.game.add_outcome([7200, 2000], label="Trustworthy Transaction")
#         self.game.set_outcome(self.game.root.children[0].children[0], trust_honor_outcome)
        
#         # Trust + Abuse outcome: Buyer gets 3000, Seller gets 4000
#         trust_abuse_outcome = self.game.add_outcome([3000, 4000], label="Trust Betrayed")
#         self.game.set_outcome(self.game.root.children[0].children[1], trust_abuse_outcome)

#     def solve_game(self):
#         """
#         Solve the game for Nash equilibria.
#         Simplified to return empty list if no solver is available
#         """
#         try:
#             # Try to find a solver method
#             if hasattr(gbt, 'nash'):
#                 # Attempt to use a solver if available
#                 solver_methods = [
#                     'ExternalEnumMixedSolver',
#                     'ExternalEnumPureSolver',
#                     'EnumMixedSolver',
#                     'EnumPureSolver'
#                 ]
                
#                 for solver_name in solver_methods:
#                     if hasattr(gbt.nash, solver_name):
#                         solver = getattr(gbt.nash, solver_name)()
#                         equilibria = solver.solve(self.game)
#                         return [
#                             {str(self.game.players[i]): eq[i] for i in range(len(self.game.players))}
#                             for eq in equilibria
#                         ]
            
#             # Fallback to an empty list if no solver works
#             return []
        
#         except Exception as e:
#             print(f"Error solving game: {e}")
#             return []


# import pygambit as gbt

# class TrustGameGambit:
#     def __init__(self):
#         """
#         Define the Trust Game structure using Pygambit.
#         """
#         self.game = gbt.Game.new_tree(players=["Buyer", "Seller"],
#                                       title="One-shot Trust Game")
#         self._setup_game_structure()

#     def _setup_game_structure(self):
#         """
#         Set up the moves and outcomes for the game.
#         This is done during initialization to set up the tree.
#         """
#         # Add Buyer's move with Trust and Not Trust actions
#         self.game.append_move(self.game.root, "Buyer", ["Trust", "Not trust"])
        
#         # Add Seller's move if Buyer chooses Trust
#         self.game.append_move(self.game.root.children[0], "Seller", ["Honor", "Abuse"])

#         # Add outcomes for each possible scenario
#         self._add_outcomes()

#     def _add_outcomes(self):
#         """
#         Define all possible outcomes based on buyer and seller actions.
#         """
#         # Not Trust outcome: Buyer gets 6000, Seller gets 0
#         not_trust_outcome = self.game.add_outcome([6000, 0], label="Opt-out")
#         self.game.set_outcome(self.game.root.children[1], not_trust_outcome)

#         # Trust + Honor outcome: Buyer gets 7200, Seller gets 2000
#         trust_honor_outcome = self.game.add_outcome([7200, 2000], label="Trustworthy Transaction")
#         self.game.set_outcome(self.game.root.children[0].children[0], trust_honor_outcome)

#         # Trust + Abuse outcome: Buyer gets 3000, Seller gets 4000
#         trust_abuse_outcome = self.game.add_outcome([3000, 4000], label="Trust Betrayed")
#         self.game.set_outcome(self.game.root.children[0].children[1], trust_abuse_outcome)

#     def play_game(self, buyer_choice, seller_choice=None):
#         """
#         Determines the outcome based on the buyer's and seller's choices.
#         """
#         if buyer_choice == "Trust":
#             if seller_choice == "Honor":
#                 outcome = {"Buyer": 7200, "Seller": 2000}
#             elif seller_choice == "Abuse":
#                 outcome = {"Buyer": 3000, "Seller": 4000}
#             else:
#                 return {"error": "Invalid seller choice!"}
#         elif buyer_choice == "Not trust":
#             outcome = {"Buyer": 6000, "Seller": 0}
#         else:
#             return {"error": "Invalid buyer choice!"}

#         return outcome


