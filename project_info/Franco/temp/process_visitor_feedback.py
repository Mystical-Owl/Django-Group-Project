"""
Process Visitor Feedback for 110 Questions

This script processes visitor feedback stored in a CSV file containing answers to
110 questions divided into two areas: "Financial Capacity" and "Preference".

The script uses question definitions from:
- default_data/IAAF_form_50_question.csv (50 questions, Financial Capacity)
- default_data/LOT_50.csv (50 questions, Preference)
- Additional 10 demographic questions (if any) can be added later.

Assumptions:
1. Visitor answers CSV has columns: question_id, answer_text
   where question_id matches q_sort_order in definition CSVs.
2. Answer text must match exactly the 'answer' column in definition CSVs.
3. Each question must be answered exactly once.

Outputs:
- Scores per area (Financial Capacity, Preference)
- Weighted total scores
- Overall score and recommendation
"""

import csv
# import os
from pathlib import Path

# Paths to definition CSV files
IAAF_DEF_PATH = Path("default_data/IAAF_form_50_question.csv")
LOT_DEF_PATH = Path("default_data/LOT_50.csv")
# Visitor answers CSV (to be provided later)
VISITOR_ANSWERS_PATH = Path("visitor_answers.csv")  # placeholder

def load_question_definitions(csv_path):
    """
    Load question definitions from CSV.
    
    Returns a dict mapping:
        (area, question_id, answer_text) -> {
            'score': float,
            'weight': float,
            'question_text': str
        }
    Also returns a dict of question weights (area, question_id) -> weight.
    """
    definitions = {}
    question_weights = {}  # (area, q_id) -> weight
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q_id = int(row['q_sort_order'])
            answer = row['answer']
            score = float(row['score'])
            weight = float(row['weight'])
            area = row['questionaire_type']
            question_text = row['question']
            
            definitions[(area, q_id, answer)] = {
                'score': score,
                'weight': weight,
                'question_text': question_text
            }
            # Store weight per question (same for all answers of same question)
            if (area, q_id) not in question_weights:
                question_weights[(area, q_id)] = weight
    return definitions, question_weights

def load_visitor_answers(csv_path):
    """
    Load visitor answers from CSV.
    
    Expected columns: question_id, answer_text (optional: area)
    Returns list of tuples (area, question_id, answer_text) if area column present,
    otherwise (question_id, answer_text).
    """
    answers = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        has_area = 'area' in fieldnames or 'questionaire_type' in fieldnames
        for row in reader:
            q_id = int(row['question_id'])
            answer = row['answer_text']
            if has_area:
                area = row.get('area') or row.get('questionaire_type')
                answers.append((area, q_id, answer))
            else:
                answers.append((q_id, answer))
    return answers, has_area

def calculate_scores(definitions, question_weights, answers, has_area):
    """
    Calculate scores based on visitor answers.
    
    Args:
        definitions: dict mapping (area, q_id, answer) or (q_id, answer) to info
        question_weights: dict mapping (area, q_id) or q_id to weight
        answers: list of tuples (area, q_id, answer) if has_area else (q_id, answer)
        has_area: bool indicating if area is included in answers
    
    Returns dict with:
        - scores_per_area: {area: total_score}
        - weighted_scores_per_area: {area: weighted_score}
        - overall_score: sum of weighted scores across all areas
        - breakdown: list of details per answered question
    """
    scores_per_area = {}
    weighted_scores_per_area = {}
    breakdown = []
    answered_keys = set()
    
    for answer in answers:
        if has_area:
            area, q_id, answer_text = answer
            key = (area, q_id, answer_text)
            weight_key = (area, q_id)
        else:
            q_id, answer_text = answer
            key = (q_id, answer_text)
            weight_key = q_id
        
        if key not in definitions:
            raise ValueError(f"Unknown answer '{answer_text}' for question {q_id}" + 
                             (f" in area {area}" if has_area else ""))
        
        if key in answered_keys:
            raise ValueError(f"Duplicate answer for question {q_id}" +
                             (f" in area {area}" if has_area else ""))
        answered_keys.add(key)
        
        info = definitions[key]
        score = info['score']
        weight = question_weights[weight_key]
        weighted = score * weight
        
        # Determine area
        if has_area:
            area = area
        else:
            # Extract area from definitions (assuming unique q_id)
            # Find area by looking at definitions keys that match q_id
            areas = set()
            for k in definitions.keys():
                if len(k) == 3 and k[1] == q_id:
                    areas.add(k[0])
                elif len(k) == 2 and k[0] == q_id:
                    # old format, area not stored
                    pass
            if len(areas) == 1:
                area = list(areas)[0]
            else:
                area = "Unknown"
        
        # Accumulate area scores
        scores_per_area[area] = scores_per_area.get(area, 0) + score
        weighted_scores_per_area[area] = weighted_scores_per_area.get(area, 0) + weighted
        
        breakdown.append({
            'question_id': q_id,
            'question_text': info['question_text'],
            'answer': answer_text,
            'score': score,
            'weight': weight,
            'weighted_score': weighted,
            'area': area
        })
    
    overall_score = sum(weighted_scores_per_area.values())
    
    return {
        'scores_per_area': scores_per_area,
        'weighted_scores_per_area': weighted_scores_per_area,
        'overall_score': overall_score,
        'breakdown': breakdown
    }

def generate_recommendation(scores):
    """
    Generate a recommendation based on scores.
    This is a placeholder - adjust based on business rules.
    """
    financial = scores['weighted_scores_per_area'].get('Financial Capacity', 0)
    preference = scores['weighted_scores_per_area'].get('Preference', 0)
    
    # Example rules
    if financial >= 40 and preference >= 30:
        return "High suitability for investment."
    elif financial >= 20 and preference >= 15:
        return "Moderate suitability - consider risk tolerance."
    else:
        return "Low suitability - recommend further assessment."

def main():
    # Load definitions from both CSVs
    print("Loading question definitions...")
    iaaf_defs, iaaf_weights = load_question_definitions(IAAF_DEF_PATH)
    lot_defs, lot_weights = load_question_definitions(LOT_DEF_PATH)
    
    # Merge definitions
    definitions = {**iaaf_defs, **lot_defs}
    question_weights = {**iaaf_weights, **lot_weights}
    
    print(f"Loaded {len(definitions)} answer definitions.")
    print(f"Unique questions: {len(question_weights)}")
    
    # Check if visitor answers file exists
    if not VISITOR_ANSWERS_PATH.exists():
        print(f"Visitor answers file not found at {VISITOR_ANSWERS_PATH}")
        print("Creating a sample visitor answers file for demonstration...")
        create_sample_answers(VISITOR_ANSWERS_PATH, question_weights, definitions)
        print(f"Sample file created at {VISITOR_ANSWERS_PATH}")
        print("Please replace with actual visitor data when available.")
    
    # Load visitor answers
    print("\nLoading visitor answers...")
    answers, has_area = load_visitor_answers(VISITOR_ANSWERS_PATH)
    print(f"Loaded {len(answers)} answers.")
    
    # Calculate scores
    print("\nCalculating scores...")
    try:
        scores = calculate_scores(definitions, question_weights, answers, has_area)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Display results
    print("\n" + "="*60)
    print("SCORING RESULTS")
    print("="*60)
    
    print("\nScores per area (raw):")
    for area, score in scores['scores_per_area'].items():
        print(f"  {area}: {score:.2f}")
    
    print("\nWeighted scores per area:")
    for area, wscore in scores['weighted_scores_per_area'].items():
        print(f"  {area}: {wscore:.2f}")
    
    print(f"\nOverall weighted score: {scores['overall_score']:.2f}")
    
    recommendation = generate_recommendation(scores)
    print(f"\nRecommendation: {recommendation}")
    
    # Optional: Save detailed breakdown to CSV
    output_path = Path("scoring_breakdown.csv")
    save_breakdown(scores['breakdown'], output_path)
    print(f"\nDetailed breakdown saved to {output_path}")

def create_sample_answers(output_path, question_weights, definitions):
    """
    Create a sample visitor answers CSV for testing.
    Selects the first answer option for each question.
    """
    # Group by (area, q_id)
    questions = {}
    for (area, q_id, answer), info in definitions.items():
        key = (area, q_id)
        if key not in questions:
            questions[key] = []
        questions[key].append((answer, info))
    
    # Pick first answer for each question
    sample_answers = []
    for (area, q_id) in sorted(questions.keys()):
        first_answer = questions[(area, q_id)][0][0]
        sample_answers.append([area, q_id, first_answer])
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['area', 'question_id', 'answer_text'])
        writer.writerows(sample_answers)
    
    return sample_answers

def save_breakdown(breakdown, output_path):
    """Save detailed breakdown to CSV."""
    if not breakdown:
        return
    fieldnames = ['question_id', 'question_text', 'answer', 'score', 'weight', 'weighted_score', 'area']
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(breakdown)

if __name__ == "__main__":
    main()
