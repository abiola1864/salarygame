import pygambit as gbt
from random import randint

class PaymentStructureGame:
    def __init__(self):
        """
        Initialize the payment structure game with experimental stages and conditions.
        """
        self.base_salary = 6000
        self.game = gbt.Game.new_tree(players=["Participant"], 
                                     title="Payment Structure Experiment")
        
        self.stages = {
            'baseline': {
                'frame': 'Base Salary',
                'description': 'Your monthly base salary is 6,000 NGN.',
                'base_salary': 6000,
                'additional_payment': 0,
                'shock_range': (0, 0),
                'categories': ['discretionary', 'savings', 'essential', 'transportation', 'social', 'work']
            },
            'condition_a': {
                'frame': 'Monthly Payment Schedule',
                'description': 'Your monthly income consists of a base salary of 6,000 NGN plus a temporal payment of 4,000 NGN.',
                'base_salary': 6000,
                'additional_payment': 4000,
                'shock_range': (1000, 2000),
                'categories': ['discretionary', 'savings', 'essential', 'transportation', 'social', 'work']
            },
            'condition_b': {
                'frame': 'Performance Bonus',
                'description': 'Congratulations! You have received a performance bonus of 10,000 NGN for your excellent work.',
                'base_salary': 0,
                'bonus_payment': 10000,
                'shock_range': (2000, 3000),
                'categories': ['discretionary', 'savings', 'essential', 'transportation', 'social', 'work']
            },
            'condition_c': {
                'frame': 'One-Time Payment',
                'description': 'You have received a one-time lump sum payment of 10,000 NGN.',
                'base_salary': 0,
                'lump_sum': 10000,
                'shock_range': (2000, 3000),
                'categories': ['discretionary', 'savings', 'essential', 'transportation', 'social', 'work']
            },
            'condition_d': {
                'frame': 'Salary Adjustment',
                'description': 'Your base salary has been permanently increased to 5,000 NGN monthly.',
                'base_salary': 5000,
                'additional_payment': 0,
                'shock_range': (2000, 3000),
                'categories': ['discretionary', 'savings', 'essential', 'transportation', 'social', 'work']
            }
        }
        
        self._setup_game_structure()

    def _setup_game_structure(self):
        """Set up the game tree structure using pygambit."""
        # Add stages as moves in the game tree
        root_move = self.game.append_move(self.game.root, "Participant", 
                                        list(self.stages.keys()))
        
        # Add outcomes for each stage
        for idx, stage in enumerate(self.stages.keys()):
            config = self.stages[stage]
            total_available = (
                config.get('base_salary', 0) +
                config.get('additional_payment', 0) +
                config.get('bonus_payment', 0) +
                config.get('lump_sum', 0)
            )
            outcome = self.game.add_outcome([total_available], label=stage)
            self.game.set_outcome(root_move.children[idx], outcome)

    def evaluate_allocation(self, allocations, stage, shock_amount=None):
        """
        Evaluate participant's allocation strategy for current stage.
        """
        if stage not in self.stages:
            raise ValueError(f"Invalid stage: {stage}")
            
        stage_config = self.stages[stage]
        
        # Calculate total available amount
        total_available = (
            stage_config.get('base_salary', 0) +
            stage_config.get('additional_payment', 0) +
            stage_config.get('bonus_payment', 0) +
            stage_config.get('lump_sum', 0)
        )
        
        # Apply shock if not specified
        if shock_amount is None:
            shock_min, shock_max = stage_config['shock_range']
            shock_amount = randint(shock_min, shock_max)
            
        # Calculate net amount after shock
        net_amount = total_available - shock_amount
        
        # Validate allocations
        total_allocated = sum(allocations.values())
        if total_allocated > net_amount:
            return {
                'valid': False,
                'message': f'Total allocation ({total_allocated}) exceeds available amount ({net_amount})',
                'net_amount': net_amount,
                'shock_amount': shock_amount
            }
            
        # Calculate allocation percentages
        percentages = {
            category: (amount / net_amount * 100)
            for category, amount in allocations.items()
        }
        
        # Analyze behavior
        analysis = self._analyze_allocation(percentages, stage)
        
        return {
            'valid': True,
            'stage': stage,
            'frame': stage_config['frame'],
            'total_available': total_available,
            'net_amount': net_amount,
            'shock_amount': shock_amount,
            'total_allocated': total_allocated,
            'unallocated': net_amount - total_allocated,
            'percentages': percentages,
            'analysis': analysis
        }
        
    def _analyze_allocation(self, percentages, stage):
        """
        Analyze allocation behavior based on stage and percentages.
        """
        analysis = []
        
        # Primary categories analysis
        savings_ratio = percentages.get('savings', 0)
        discretionary_ratio = percentages.get('discretionary', 0)
        
        # Secondary categories analysis
        essential_ratio = percentages.get('essential', 0)
        transportation_ratio = percentages.get('transportation', 0)
        social_ratio = percentages.get('social', 0)
        work_ratio = percentages.get('work', 0)
        
        # Stage-specific analysis
        if stage == 'baseline':
            analysis.append("Baseline allocation pattern")
        elif stage == 'condition_a':
            analysis.append("Response to temporal payment structure")
        elif stage == 'condition_b':
            analysis.append("Bonus payment allocation strategy")
        elif stage == 'condition_c':
            analysis.append("Lump-sum payment behavior")
        elif stage == 'condition_d':
            analysis.append("Permanent income change adaptation")
            
        return analysis

    def get_next_stage(self, current_stage):
        """
        Determine the next stage in the experiment.
        """
        stages = list(self.stages.keys())
        try:
            current_index = stages.index(current_stage)
            if current_index < len(stages) - 1:
                return stages[current_index + 1]
            return None
        except ValueError:
            return stages[0]