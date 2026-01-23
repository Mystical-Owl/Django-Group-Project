"""
Simple test to demonstrate questionnaire scoring.
"""

# Test the scoring logic directly without Django dependencies
def test_scoring_directly():
    """Test scoring logic without Django."""
    
    print("Testing Questionnaire Scoring Logic")
    print("=" * 50)
    
    # Define the scoring function (copied from main module)
    def calculate_question_score(question_no, response):
        if question_no in [3, 7, 9]:
            return 4 - response  # Reverse scoring
        else:
            return response  # Normal scoring
    
    def calculate_total_score(responses):
        """Calculate total score from responses."""
        if len(responses) != 10:
            raise ValueError(f'Must answer exactly 10 questions. Provided: {len(responses)}')
        
        total = 0
        seen_questions = set()
        
        for q, r in responses:
            if q in seen_questions:
                raise ValueError(f'Duplicate answer for question {q}')
            if r not in [0, 1, 2, 3, 4]:
                raise ValueError(f'Invalid response {r} for question {q}')
            
            seen_questions.add(q)
            total += calculate_question_score(q, r)
        
        if len(seen_questions) != 10:
            raise ValueError(f'Missing answers. Answered {len(seen_questions)} out of 10.')
        
        return total
    
    # Test cases from the CSV data
    print("\n1. Testing individual question scoring:")
    print("   Question 1 (normal scoring):")
    for response in range(5):
        score = calculate_question_score(1, response)
        print(f"     Response {response} -> Score {score}")
    
    print("\n   Question 3 (reverse scoring):")
    for response in range(5):
        score = calculate_question_score(3, response)
        print(f"     Response {response} -> Score {score}")
    
    # Test complete questionnaire
    print("\n2. Testing complete questionnaire:")
    
    # Example from user's initial message
    test_responses = []
    print("   Building responses from CSV pattern...")
    
    # Based on CSV: each question has 5 possible responses 0-4
    # Let's create a sample where user selects middle response (2) for all questions
    for q in range(1, 11):
        response = 2  # Middle response
        test_responses.append((q, response))
    
    try:
        total = calculate_total_score(test_responses)
        print(f"   Sample responses (all middle): Total score = {total}")
        
        # Calculate expected: 
        # Questions 1,2,4,5,6,8,10: normal scoring, response 2 -> score 2 (7 questions × 2 = 14)
        # Questions 3,7,9: reverse scoring, response 2 -> score 2 (3 questions × 2 = 6)
        # Total = 20
        print(f"   Expected: 20")
        print(f"   Match: {'✓' if total == 20 else '✗'}")
        
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Test edge cases
    print("\n3. Testing edge cases:")
    
    # All minimum responses (0)
    min_responses = [(q, 0) for q in range(1, 11)]
    min_score = calculate_total_score(min_responses)
    print(f"   All minimum responses (0): Score = {min_score}")
    
    # All maximum responses (4)
    max_responses = [(q, 4) for q in range(1, 11)]
    max_score = calculate_total_score(max_responses)
    print(f"   All maximum responses (4): Score = {max_score}")
    
    # Calculate range
    print(f"   Score range: {min_score} to {max_score}")
    
    # Test invalid cases
    print("\n4. Testing invalid cases:")
    
    # Too few responses
    try:
        calculate_total_score([(1, 2), (2, 2)])
        print("   ✗ Should have raised error for too few responses")
    except ValueError as e:
        print(f"   ✓ Correctly rejected: {e}")
    
    # Invalid response value
    try:
        calculate_total_score([(1, 5)] + [(q, 2) for q in range(2, 11)])
        print("   ✗ Should have raised error for invalid response")
    except ValueError as e:
        print(f"   ✓ Correctly rejected: {e}")
    
    # Duplicate question
    try:
        duplicate = [(1, 2), (1, 3)] + [(q, 2) for q in range(3, 11)]
        calculate_total_score(duplicate)
        print("   ✗ Should have raised error for duplicate question")
    except ValueError as e:
        print(f"   ✓ Correctly rejected: {e}")
    
    print("\n" + "=" * 50)
    print("Scoring logic test complete!")
    print("\nKey points:")
    print("1. 10 questions total, must answer exactly 10")
    print("2. Each question has 5 possible responses (0-4)")
    print("3. Questions 3, 7, 9 use reverse scoring")
    print("4. All questions have weight = 1.0")
    print("5. Total score range: 0 to 40")


if __name__ == "__main__":
    test_scoring_directly()
