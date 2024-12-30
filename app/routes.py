


from flask import Blueprint, render_template, request, jsonify, session
from .payment_structure_game import PaymentStructureGame

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Initialize the experiment and render first stage."""
    if 'stage' not in session:
        session['stage'] = 'baseline'
    return render_template('index.html')

@main.route('/stage')
def get_stage():
    """Get current stage configuration."""
    game = PaymentStructureGame()
    current_stage = session.get('stage', 'baseline')
    stage_config = game.stages[current_stage]
    
    return jsonify({
        'stage': current_stage,
        'config': stage_config
    })

@main.route('/play', methods=['POST'])
def play_game():
    """Handle allocation submission for current stage."""
    data = request.get_json()
    current_stage = session.get('stage', 'baseline')
    
    if not data:
        return jsonify({
            'error': 'No data received'
        }), 400
    
    # Extract allocations
    allocations = {
        category: int(amount)
        for category, amount in data.items()
        if category.startswith('allocation_')
    }
    
    # Initialize game and evaluate
    game = PaymentStructureGame()
    result = game.evaluate_allocation(allocations, current_stage)
    
    if result['valid']:
        # Get next stage
        next_stage = game.get_next_stage(current_stage)
        if next_stage:
            session['stage'] = next_stage
            result['next_stage'] = next_stage
        else:
            result['experiment_complete'] = True
    
    return jsonify({'game_analysis': result})

@main.route('/progress')
def get_progress():
    """Get experiment progress."""
    game = PaymentStructureGame()
    current_stage = session.get('stage', 'baseline')
    total_stages = len(game.stages)
    current_index = list(game.stages.keys()).index(current_stage)
    
    return jsonify({
        'current_stage': current_stage,
        'progress': ((current_index + 1) / total_stages) * 100,
        'total_stages': total_stages
    })

@main.route('/analysis/<session_id>')
def get_analysis(session_id):
    """Admin only: Get detailed analysis of participant's allocations."""
    # Add authentication check here
    game = PaymentStructureGame()
    # Implement analysis retrieval logic
    return jsonify({'message': 'Analysis endpoint'})






# from flask import Blueprint, render_template, request, jsonify
# from .trust_game_gambit import AllocationGameGambit  # Assuming AllocationGameGambit is the correct import

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

# @main.route('/play', methods=['POST'])
# def play_game():
#     """
#     Handle the allocation game submission.
#     """
#     data = request.get_json()
    
#     if not data:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': 'No data received',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400
    
#     # Extract allocations from form data
#     allocations = {}
#     for key, value in data.items():
#         if key.startswith('allocation_'):
#             category = key[11:].replace('_', ' ').title()
#             try:
#                 amount = int(value)
#                 allocations[category] = amount
#             except (ValueError, TypeError):
#                 return jsonify({
#                     'game_analysis': {
#                         'valid': False,
#                         'message': f'Invalid amount for {category}',
#                         'total_allocated': 0,
#                         'expected_total': 10000
#                     }
#                 }), 400
    
#     # Initialize and run game analysis
#     game = AllocationGameGambit()
#     result = game.evaluate_allocation(allocations)
#     total_allocated = result['total_allocated']
    
#     # Prepare response
#     response = {
#         'game_analysis': {
#             'valid': total_allocated == 10000,
#             'message': f'Strategy identified: {result["strategy"]}',
#             'total_allocated': total_allocated,
#             'expected_total': 10000,
#             'strategy': result['strategy'],
#             'monetary_outcome': result['monetary_outcome'],
#             'impact_score': result['impact_score'],
#             'analysis': result['analysis'],
#             'percentages': {k: (v / total_allocated * 100) for k, v in allocations.items()}
#         }
#     }
    
#     return jsonify(response)



# from flask import Blueprint, render_template, request, jsonify
# from .trust_game_gambit import AllocationGameGambit  # Assuming AllocationGameGambit is the correct import

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

# @main.route('/play', methods=['POST'])
# def play_game():
#     """
#     Handle the allocation game submission.
#     """
#     data = request.get_json()
    
#     if not data:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': 'No data received',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400
    
#     # Extract allocations from form data
#     allocations = {}
#     for key, value in data.items():
#         if key.startswith('allocation_'):
#             category = key[11:].replace('_', ' ').title()
#             try:
#                 amount = int(value)
#                 allocations[category] = amount
#             except (ValueError, TypeError):
#                 return jsonify({
#                     'game_analysis': {
#                         'valid': False,
#                         'message': f'Invalid amount for {category}',
#                         'total_allocated': 0,
#                         'expected_total': 10000
#                     }
#                 }), 400
    
#     # Initialize and run game analysis
#     game = AllocationGameGambit()
#     result = game.evaluate_allocation(allocations)
#     total_allocated = result['total_allocated']
    
#     # Prepare response
#     response = {
#         'game_analysis': {
#             'valid': total_allocated == 10000,
#             'message': f'Strategy identified: {result["strategy"]}',
#             'total_allocated': total_allocated,
#             'expected_total': 10000,
#             'strategy': result['strategy'],
#             'monetary_outcome': result['monetary_outcome'],
#             'impact_score': result['impact_score'],
#             'analysis': result['analysis'],
#             'percentages': {k: (v / total_allocated * 100) for k, v in allocations.items()}
#         }
#     }
    
#     return jsonify(response)

# @main.route('/tree')
# def view_tree():
#     """
#     Visualizes the game tree.
#     """
#     game = AllocationGameGambit()  # Create a new game instance
#     tree_representation = str(game)  # Get the string representation of the game tree
#     return render_template('tree.html', tree=tree_representation)  # Pass 'tree' to template

# @main.route('/strategies')
# def view_strategies():
#     """
#     View all possible strategies and their outcomes.
#     """
#     game = AllocationGameGambit()  # Create a new game instance
#     strategies = game.get_all_strategies()  # This method should return a list of strategies
#     return render_template('strategies.html', strategies=strategies)

# @main.route('/export')
# def export_game():
#     """
#     Export the game data to a file (for reporting or analysis).
#     """
#     game = AllocationGameGambit()  # Create a new game instance
#     file_path = game.export_to_file()  # Assuming 'export_to_file()' method exists
#     return jsonify({'file_path': file_path})

# @main.route('/score')
# def view_score():
#     """
#     View the score of a player using session ID.
#     """
#     session_id = request.args.get('session_id')  # Get session ID from query params
#     game = AllocationGameGambit()  # Create a new game instance
#     score = game.get_score(session_id)  # Assuming 'get_score()' method exists to fetch score
#     return jsonify({'session_id': session_id, 'score': score})














# from flask import Blueprint, render_template, request, jsonify
# from .trust_game_gambit import TrustGameGambit

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

# @main.route('/play', methods=['POST'])
# def play_game():
#     """
#     Play the Trust Game using Gambit.
#     """
#     data = request.get_json()
#     buyer_choice = data.get('buyer_choice')
#     seller_choice = data.get('seller_choice', None)

#     # Initialize and model the game using Gambit
#     trust_game = TrustGameGambit()
#     equilibria = trust_game.solve_game()

#     # Determine outcome based on user input
#     if buyer_choice == "Not trust":
#         result = {
#             'label': 'Opt-out',
#             'payoff': 6000,
#             'message': 'Buyer chose not to trust.',
#             'equilibria': equilibria
#         }
#     elif buyer_choice == "Trust" and seller_choice == "Honor":
#         result = {
#             'label': 'Trustworthy Transaction',
#             'payoff': 7200,
#             'message': 'Trust leads to mutual benefit!',
#             'equilibria': equilibria
#         }
#     elif buyer_choice == "Trust" and seller_choice == "Abuse":
#         result = {
#             'label': 'Trust Betrayed',
#             'payoff': 3000,
#             'message': 'Trust was betrayed.',
#             'equilibria': equilibria
#         }
#     else:
#         result = {
#             'label': 'Incomplete',
#             'payoff': None,
#             'message': 'Game is incomplete.',
#             'equilibria': equilibria
#         }

#     return jsonify(result)







# from flask import Blueprint, render_template, request, jsonify
# from .trust_game_gambit import TrustGameGambit


# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

# @main.route('/play', methods=['POST'])
# def play_game():
#     """
#     Handle the allocation game submission.
#     """
#     data = request.get_json()
    
#     if not data:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': 'No data received',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400

#     # Extract buyer and seller choices
#     buyer_choice = data.get('buyer_choice')
#     seller_choice = data.get('seller_choice')

#     # Validate buyer's choice
#     if buyer_choice not in ['Trust', 'Not trust']:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': f'Invalid buyer choice: {buyer_choice}',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400

#     # If the buyer chooses "Trust", seller's choice should also be provided
#     if buyer_choice == "Trust" and seller_choice not in ['Honor', 'Abuse']:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': f'Invalid seller choice for "Trust": {seller_choice}',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400

#     # Initialize the game logic
#     game = TrustGameGambit()  # Create an instance of the Trust Game

#     # Get the outcome of the game based on the buyer's and seller's choices
#     outcome = game.play_game(buyer_choice, seller_choice)

#     if "error" in outcome:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': outcome['error'],
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400

#     # Calculate percentages if needed (similar to your allocation game logic)
#     total_allocated = sum(outcome.values())
#     percentages = {key: (value / total_allocated * 100) for key, value in outcome.items()}

#     return jsonify({
#         'game_analysis': {
#             'valid': True,
#             'total_allocated': total_allocated,
#             'percentages': percentages,
#             'allocations': outcome
#         }
#     })






# from flask import Blueprint, render_template, request, jsonify

# main = Blueprint('main', __name__)

# class AllocationGame:
#     def __init__(self):
#         self.total_amount = 10000

#     def validate_allocation(self, allocations):
#         """
#         Validates if the allocations sum up to the total amount and are valid.
#         """
#         total_allocated = sum(allocations.values())
        
#         if total_allocated != self.total_amount:
#             return {
#                 'valid': False,
#                 'message': f'Total allocation must equal ${self.total_amount}',
#                 'total_allocated': total_allocated,
#                 'expected_total': self.total_amount
#             }
        
#         # Check for negative values
#         if any(amount < 0 for amount in allocations.values()):
#             return {
#                 'valid': False,
#                 'message': 'Allocations cannot be negative',
#                 'total_allocated': total_allocated,
#                 'expected_total': self.total_amount
#             }
        
#         return {
#             'valid': True,
#             'total_allocated': total_allocated,
#             'percentages': {
#                 category: (amount / self.total_amount * 100)
#                 for category, amount in allocations.items()
#             },
#             'allocations': allocations
#         }

# @main.route('/')
# def home():
#     """
#     Render the homepage.
#     """
#     return render_template('index.html')

# @main.route('/play', methods=['POST'])
# def play_game():
#     """
#     Handle the allocation game submission.
#     """
#     data = request.get_json()
    
#     if not data:
#         return jsonify({
#             'game_analysis': {
#                 'valid': False,
#                 'message': 'No data received',
#                 'total_allocated': 0,
#                 'expected_total': 10000
#             }
#         }), 400
    
#     # Initialize the game
#     game = AllocationGame()
    
#     # Extract allocations from the form data
#     allocations = {}
#     for key, value in data.items():
#         if key.startswith('allocation_'):
#             # Convert from allocation_category_name to Category Name
#             category = key[11:].replace('_', ' ').title()
#             try:
#                 amount = int(value)
#                 allocations[category] = amount
#             except (ValueError, TypeError):
#                 return jsonify({
#                     'game_analysis': {
#                         'valid': False,
#                         'message': f'Invalid amount for {category}',
#                         'total_allocated': 0,
#                         'expected_total': 10000
#                     }
#                 }), 400
    
#     # Validate and process the allocations
#     result = game.validate_allocation(allocations)
    
#     return jsonify({
#         'game_analysis': result
#     })
