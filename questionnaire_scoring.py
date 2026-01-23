"""
Questionnaire Scoring Module for IAAF/LOT 50 Questionnaire

This module provides functions to calculate total scores for the 
IAAF/LOT 50 questionnaire with 10 questions and 5 responses per question.

Data structure from CSV:
Question_No,Question,Response,Score
1,In uncertain times I usually expect the best.,0,0
1,In uncertain times I usually expect the best.,1,1
1,In uncertain times I usually expect the best.,2,2
1,In uncertain times I usually expect the best.,3,3
1,In uncertain times I usually expect the best.,4,4
... etc

Note: All questions have equal weight ratio of 1.0
"""

# from django.db.models import Sum
from user_questionaire_answers.models import UserQuestionaireAnswer
# from questionaire_answers.models import QuestionaireAnswer


def calculate_questionnaire_score(responses):
    """
    Calculate the actual total score for questionnaire responses.
    Primary function for scoring - focuses on actual score calculation.
    
    Args:
        responses (list): List of tuples (question_no, response)
            where question_no is 1-10 and response is 0-4
            
    Returns:
        float: Total score (sum of all question scores)
        
    Raises:
        ValueError: If responses are invalid
    """
    if len(responses) != 10:
        raise ValueError(f'Must answer exactly 10 questions. Provided: {len(responses)}')
    
    total_score = 0
    question_nos = set()
    
    for question_no, response in responses:
        if question_no in question_nos:
            raise ValueError(f'Duplicate response for question {question_no}')
        
        if response not in [0, 1, 2, 3, 4]:
            raise ValueError(f'Invalid response {response} for question {question_no}. Must be 0-4.')
        
        question_nos.add(question_no)
        score = calculate_question_score(question_no, response)
        total_score += score
    
    if len(question_nos) != 10:
        raise ValueError(f'Missing responses for some questions. Answered {len(question_nos)} out of 10.')
    
    return total_score


def calculate_question_score(question_no, response):
    """
    Calculate score for a specific question and response.
    Based on the CSV scoring pattern provided.
    
    Args:
        question_no (int): Question number (1-10)
        response (int): Response value (0-4)
        
    Returns:
        int: Score for this question-response combination
    """
    # Define scoring rules based on the CSV data
    # Questions 3, 7, 9 have reverse scoring (4-0)
    # Other questions have normal scoring (0-4)
    
    if question_no in [3, 7, 9]:
        # Reverse scoring: response 0 -> score 4, response 4 -> score 0
        return 4 - response
    else:
        # Normal scoring: response 0 -> score 0, response 4 -> score 4
        return response


def calculate_weighted_score(responses, weights=None):
    """
    Calculate weighted score (for formality, though all weights are 1.0).
    
    Args:
        responses (list): List of tuples (question_no, response)
        weights (dict): Optional dictionary of question weights
            If None, all weights default to 1.0
            
    Returns:
        dict: {
            'total_score': float,
            'weighted_score': float,
            'breakdown': list of dicts with details
        }
    """
    if weights is None:
        # Default all weights to 1.0 (equal weighting)
        weights = {i: 1.0 for i in range(1, 11)}
    
    total_score = 0
    weighted_score = 0
    breakdown = []
    question_nos = set()
    
    for question_no, response in responses:
        if question_no in question_nos:
            raise ValueError(f'Duplicate response for question {question_no}')
        
        if response not in [0, 1, 2, 3, 4]:
            raise ValueError(f'Invalid response {response} for question {question_no}. Must be 0-4.')
        
        question_nos.add(question_no)
        score = calculate_question_score(question_no, response)
        weight = weights.get(question_no, 1.0)
        weighted_contribution = score * weight
        
        total_score += score
        weighted_score += weighted_contribution
        
        breakdown.append({
            'question_no': question_no,
            'response': response,
            'score': score,
            'weight': weight,
            'weighted_contribution': weighted_contribution
        })
    
    if len(question_nos) != 10:
        raise ValueError(f'Missing responses for some questions. Answered {len(question_nos)} out of 10.')
    
    return {
        'total_score': total_score,
        'weighted_score': weighted_score,
        'breakdown': breakdown,
        'weights_used': weights
    }


def get_question_scoring_info(question_no):
    """
    Get scoring information for a specific question.
    
    Args:
        question_no (int): Question number (1-10)
        
    Returns:
        dict: Scoring information including weight, scoring type, etc.
    """
    scoring_type = "reverse" if question_no in [3, 7, 9] else "normal"
    
    return {
        'question_no': question_no,
        'scoring_type': scoring_type,
        'weight': 1.0,  # All questions have equal weight
        'possible_scores': {
            0: 4 - 0 if scoring_type == "reverse" else 0,
            1: 4 - 1 if scoring_type == "reverse" else 1,
            2: 4 - 2 if scoring_type == "reverse" else 2,
            3: 4 - 3 if scoring_type == "reverse" else 3,
            4: 4 - 4 if scoring_type == "reverse" else 4,
        }
    }


def calculate_total_score_from_database(user):
    """
    Calculate total score for a user from database records.
    
    Args:
        user: Django User object
        
    Returns:
        float: Total score
        
    Raises:
        ValueError: If user doesn't have exactly 10 answers
    """
    # Get all user's questionnaire answers
    user_answers = UserQuestionaireAnswer.objects.filter(user=user)
    
    # Check if user has exactly 10 answers (one per question)
    answer_count = user_answers.count()
    
    if answer_count != 10:
        raise ValueError(f'Invalid number of answers: {answer_count}. Must answer exactly 10 questions.')
    
    # Calculate total score by summing answer_score from QuestionaireAnswer
    total_score = 0
    question_ids = set()
    
    for user_answer in user_answers:
        # Get the QuestionaireAnswer object to access answer_score
        questionaire_answer = user_answer.questionaire_answer
        question = questionaire_answer.questionaire
        
        # Check for duplicate answers to same question
        if question.id in question_ids:
            raise ValueError(f'Duplicate answers for question {question.id}. Must answer each question only once.')
        
        question_ids.add(question.id)
        
        # Add the score (answer_score is FloatField)
        if questionaire_answer.answer_score is not None:
            total_score += questionaire_answer.answer_score
        else:
            # If answer_score is not set, use default scoring based on response
            response_value = extract_response_value(questionaire_answer.questionaire_answer)
            score = calculate_question_score(question.id, response_value)
            total_score += score
    
    # Verify all 10 questions were answered
    if len(question_ids) != 10:
        raise ValueError(f'Missing answers for some questions. Answered {len(question_ids)} out of 10 questions.')
    
    return total_score


def extract_response_value(answer_text):
    """
    Extract numeric response value from answer text.
    In the CSV, Response column contains 0,1,2,3,4
    
    Args:
        answer_text (str): The answer text from QuestionaireAnswer
        
    Returns:
        int: Numeric response value (0-4)
    """
    try:
        # Try to convert answer text to integer
        return int(answer_text.strip())
    except (ValueError, AttributeError):
        # If conversion fails, try to extract number from text
        import re
        numbers = re.findall(r'\d+', str(answer_text))
        if numbers:
            return int(numbers[0])
        return 0  # Default to 0 if no number found


def validate_responses(responses):
    """
    Validate questionnaire responses.
    
    Args:
        responses (list): List of tuples (question_no, response)
        
    Returns:
        dict: Validation result
    """
    if len(responses) != 10:
        return {
            'is_valid': False,
            'message': f'Must answer exactly 10 questions. Provided: {len(responses)}'
        }
    
    question_nos = set()
    for question_no, response in responses:
        if question_no in question_nos:
            return {
                'is_valid': False,
                'message': f'Duplicate response for question {question_no}'
            }
        
        if response not in [0, 1, 2, 3, 4]:
            return {
                'is_valid': False,
                'message': f'Invalid response {response} for question {question_no}. Must be 0-4.'
            }
        
        question_nos.add(question_no)
    
    if len(question_nos) != 10:
        return {
            'is_valid': False,
            'message': f'Missing responses for some questions. Answered {len(question_nos)} out of 10.'
        }
    
    return {
        'is_valid': True,
        'message': 'Responses are valid.'
    }


def get_scoring_summary(responses):
    """
    Get detailed scoring summary for responses.
    
    Args:
        responses (list): List of tuples (question_no, response)
        
    Returns:
        dict: Detailed scoring summary
    """
    try:
        total_score = calculate_questionnaire_score(responses)
        weighted_result = calculate_weighted_score(responses)
        
        # Calculate percentage (max score is 40)
        max_score = 40
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Determine risk level based on score
        if total_score >= 32:
            risk_level = "Low Risk (Optimistic)"
        elif total_score >= 24:
            risk_level = "Moderate Risk"
        elif total_score >= 16:
            risk_level = "Moderate-High Risk"
        else:
            risk_level = "High Risk (Pessimistic)"
        
        return {
            'total_score': total_score,
            'weighted_score': weighted_result['weighted_score'],
            'percentage': round(percentage, 1),
            'max_score': max_score,
            'risk_level': risk_level,
            'breakdown': weighted_result['breakdown'],
            'is_valid': True,
            'message': 'Score calculated successfully'
        }
        
    except ValueError as e:
        return {
            'total_score': 0,
            'weighted_score': 0,
            'percentage': 0,
            'max_score': 40,
            'risk_level': 'Invalid',
            'breakdown': [],
            'is_valid': False,
            'message': str(e)
        }


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Questionnaire Scoring Module - Example Usage")
    print("=" * 60)
    
    # Example 1: Valid responses
    print("\n1. Calculating score for valid responses:")
    example_responses = [
        (1, 3),  # Question 1, Response 3 -> Score 3
        (2, 2),  # Question 2, Response 2 -> Score 2
        (3, 1),  # Question 3, Response 1 -> Score 3 (reverse scoring)
        (4, 4),  # Question 4, Response 4 -> Score 4
        (5, 0),  # Question 5, Response 0 -> Score 0
        (6, 3),  # Question 6, Response 3 -> Score 3
        (7, 2),  # Question 7, Response 2 -> Score 2 (reverse scoring)
        (8, 1),  # Question 8, Response 1 -> Score 1
        (9, 0),  # Question 9, Response 0 -> Score 4 (reverse scoring)
        (10, 4), # Question 10, Response 4 -> Score 4
    ]
    
    try:
        score = calculate_questionnaire_score(example_responses)
        print(f"   Total Score: {score}")
        
        summary = get_scoring_summary(example_responses)
        print(f"   Percentage: {summary['percentage']}%")
        print(f"   Risk Level: {summary['risk_level']}")
        
        # Show weighted score (should be same as total since weights are 1.0)
        weighted_result = calculate_weighted_score(example_responses)
        print(f"   Weighted Score: {weighted_result['weighted_score']}")
        print("   Note: Weighted score equals total score since all weights are 1.0")
        
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Example 2: Invalid responses (too few)
    print("\n2. Testing invalid responses (too few):")
    invalid_responses = [(1, 3), (2, 2), (3, 1)]
    try:
        score = calculate_questionnaire_score(invalid_responses)
        print(f"   Total Score: {score}")
    except ValueError as e:
        print(f"   Error (expected): {e}")
    
    # Example 3: Show question scoring info
    print("\n3. Question scoring information:")
    for q in [1, 3, 5, 7, 10]:
        info = get_question_scoring_info(q)
        print(f"   Q{q}: {info['scoring_type']} scoring, Weight: {info['weight']}")
    
    # Example 4: Maximum and minimum scores
    print("\n4. Score ranges:")
    max_responses = [(q, 4) for q in range(1, 11)]
    min_responses = [(q, 0) for q in range(1, 11)]
    
    try:
        max_score = calculate_questionnaire_score(max_responses)
        min_score = calculate_questionnaire_score(min_responses)
        print(f"   Maximum possible score: {max_score}")
        print(f"   Minimum possible score: {min_score}")
        print(f"   Score range: {min_score} to {max_score}")
    except ValueError as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Module ready for use in Django views")
    print("=" * 60)
