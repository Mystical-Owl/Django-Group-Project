# Financial Investment System UML Diagram (Formatted)

## Class Diagram

```mermaid
classDiagram
    %% Core Customer Entities
    class Customer {
        +int customer_id
        +string name
        +string email
        +string telephone
        +string address
        +datetime registration_date
        +string status
        +register()
        +updateProfile()
        +makeDecision()
        +viewBackground()
    }
    
    class UserAccount {
        +int account_id
        +Customer customer
        +string username
        +string password_hash
        +datetime created_at
        +boolean is_active
        +login()
        +logout()
        +changePassword()
        +resetPassword()
    }
    
    %% Decision Making
    class Decision {
        +int decision_id
        +Customer customer
        +string decision_type
        +datetime decision_date
        +boolean completed_questionnaire
        +string chosen_path
        +text notes
        +recordDecision()
        +getDecisionSummary()
        +calculatePath()
    }
    
    %% Questionnaire System
    class Questionnaire {
        +int questionnaire_id
        +string questionnaire_type
        +string description
        +int total_questions
        +datetime created_at
        +getQuestions()
        +calculateScore()
        +generateReport()
    }
    
    class Question {
        +int question_id
        +Questionnaire questionnaire
        +string question_text
        +string question_type
        +int sort_order
        +decimal weight
        +getAnswerOptions()
        +calculateWeight()
    }
    
    class QuestionnaireAnswer {
        +int answer_id
        +Customer customer
        +Question question
        +string answer_value
        +decimal score
        +datetime answered_at
        +saveAnswer()
        +calculateScore()
        +validateAnswer()
    }
    
    %% Assessment System
    class RiskAssessment {
        +int assessment_id
        +Customer customer
        +QuestionnaireAnswer answer
        +string risk_level
        +decimal risk_score
        +string recommendation
        +datetime assessed_at
        +calculateRisk()
        +getRecommendation()
        +updateAssessment()
    }
    
    class AffordabilityScore {
        +int score_id
        +Customer customer
        +QuestionnaireAnswer answer
        +decimal income_percentage
        +decimal affordable_amount
        +string affordability_level
        +datetime calculated_at
        +calculateAffordability()
        +getAffordableAmount()
        +updateScore()
    }
    
    %% Investment System
    class Product {
        +int product_id
        +string product_name
        +string product_type
        +string risk_level
        +decimal expected_return
        +decimal min_investment
        +decimal max_investment
        +string description
        +getProductDetails()
        +calculateReturns()
        +checkEligibility()
    }
    
    class Investment {
        +int investment_id
        +Customer customer
        +Product product
        +Decision decision
        +decimal investment_amount
        +datetime start_date
        +datetime end_date
        +string status
        +decimal current_value
        +startInvestment()
        +quitInvestment()
        +calculateReturn()
        +updateValue()
    }
    
    class Portfolio {
        +int portfolio_id
        +Customer customer
        +string portfolio_name
        +string risk_level
        +decimal total_value
        +datetime created_at
        +string status
        +addInvestment()
        +removeInvestment()
        +calculatePerformance()
        +generateReport()
    }
    
    class DailyReport {
        +int report_id
        +Portfolio portfolio
        +Investment investment
        +datetime report_date
        +decimal daily_return
        +decimal total_return
        +text performance_notes
        +text recommendations
        +generateReport()
        +sendNotification()
        +getPerformanceTrend()
    }
    
    %% Relationships
    Customer "1" --> "*" UserAccount : has
    Customer "1" --> "*" Decision : makes
    Customer "1" --> "*" QuestionnaireAnswer : provides
    Customer "1" --> "*" Investment : makes
    Customer "1" --> "*" Portfolio : owns
    
    Questionnaire "1" --> "*" Question : contains
    Question "1" --> "*" QuestionnaireAnswer : answered by
    QuestionnaireAnswer "1" --> "1" RiskAssessment : generates
    QuestionnaireAnswer "1" --> "1" AffordabilityScore : calculates
    
    Product "1" --> "*" Investment : purchased as
    Product "*" --> "*" Portfolio : included in
    Portfolio "1" --> "*" DailyReport : generates
    
    Decision "1" --> "*" Investment : leads to
    Decision "1" --> "0..1" QuestionnaireAnswer : may include
```

## Simplified Relationship Summary

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| Customer → UserAccount | 1:N | Customer can have multiple accounts |
| Customer → Decision | 1:N | Customer makes multiple decisions |
| Customer → QuestionnaireAnswer | 1:N | Customer provides multiple answers |
| Customer → Investment | 1:N | Customer makes multiple investments |
| Customer → Portfolio | 1:N | Customer owns multiple portfolios |
| Questionnaire → Question | 1:N | Questionnaire contains multiple questions |
| Question → QuestionnaireAnswer | 1:N | Question can have multiple answers |
| QuestionnaireAnswer → RiskAssessment | 1:1 | Each answer generates one risk assessment |
| QuestionnaireAnswer → AffordabilityScore | 1:1 | Each answer calculates one affordability score |
| Product → Investment | 1:N | Product can be purchased as multiple investments |
| Product → Portfolio | M:N | Products can be included in multiple portfolios |
| Portfolio → DailyReport | 1:N | Portfolio generates multiple daily reports |
| Decision → Investment | 1:N | Decision leads to multiple investments |
| Decision → QuestionnaireAnswer | 0..1:1 | Decision may include questionnaire answers |

*Note: This formatted version focuses on the class diagram with directional relationships for clarity.*