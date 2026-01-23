# Financial Investment System UML Diagram

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Core Entities
    Customer ||--o{ UserAccount : "creates"
    Customer ||--o{ Decision : "makes"
    Customer ||--o{ QuestionnaireAnswer : "provides"
    Customer ||--o{ Investment : "makes"
    Customer ||--o{ Portfolio : "owns"
    
    %% Questionnaire System
    Questionnaire ||--o{ Question : "contains"
    Question ||--o{ QuestionnaireAnswer : "answered by"
    QuestionnaireAnswer ||--o{ RiskAssessment : "generates"
    QuestionnaireAnswer ||--o{ AffordabilityScore : "calculates"
    
    %% Investment System
    Product ||--o{ Investment : "purchased as"
    Product ||--o{ Portfolio : "included in"
    Portfolio ||--o{ DailyReport : "generates"
    
    %% Decision Making
    Decision ||--o{ Investment : "leads to"
    Decision ||--o{ QuestionnaireAnswer : "may include"
    
    %% Entity Definitions
    Customer {
        int customer_id PK
        string name
        string email
        string telephone
        string address
        datetime registration_date
        string status
    }
    
    UserAccount {
        int account_id PK
        int customer_id FK
        string username
        string password_hash
        datetime created_at
        boolean is_active
    }
    
    Decision {
        int decision_id PK
        int customer_id FK
        string decision_type
        datetime decision_date
        boolean completed_questionnaire
        string chosen_path
        text notes
    }
    
    Questionnaire {
        int questionnaire_id PK
        string questionnaire_type
        string description
        int total_questions
        datetime created_at
    }
    
    Question {
        int question_id PK
        int questionnaire_id FK
        string question_text
        string question_type
        int sort_order
        decimal weight
    }
    
    QuestionnaireAnswer {
        int answer_id PK
        int customer_id FK
        int question_id FK
        string answer_value
        decimal score
        datetime answered_at
    }
    
    RiskAssessment {
        int assessment_id PK
        int customer_id FK
        int answer_id FK
        string risk_level
        decimal risk_score
        string recommendation
        datetime assessed_at
    }
    
    AffordabilityScore {
        int score_id PK
        int customer_id FK
        int answer_id FK
        decimal income_percentage
        decimal affordable_amount
        string affordability_level
        datetime calculated_at
    }
    
    Product {
        int product_id PK
        string product_name
        string product_type
        string risk_level
        decimal expected_return
        decimal min_investment
        decimal max_investment
        string description
    }
    
    Investment {
        int investment_id PK
        int customer_id FK
        int product_id FK
        int decision_id FK
        decimal investment_amount
        datetime start_date
        datetime end_date
        string status
        decimal current_value
    }
    
    Portfolio {
        int portfolio_id PK
        int customer_id FK
        string portfolio_name
        string risk_level
        decimal total_value
        datetime created_at
        string status
    }
    
    DailyReport {
        int report_id PK
        int portfolio_id FK
        int investment_id FK
        datetime report_date
        decimal daily_return
        decimal total_return
        text performance_notes
        text recommendations
    }
```

## Class Diagram with Relationships

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
    Customer "1" -- "*" UserAccount : has
    Customer "1" -- "*" Decision : makes
    Customer "1" -- "*" QuestionnaireAnswer : provides
    Customer "1" -- "*" Investment : makes
    Customer "1" -- "*" Portfolio : owns
    
    Questionnaire "1" -- "*" Question : contains
    Question "1" -- "*" QuestionnaireAnswer : answered by
    QuestionnaireAnswer "1" -- "1" RiskAssessment : generates
    QuestionnaireAnswer "1" -- "1" AffordabilityScore : calculates
    
    Product "1" -- "*" Investment : purchased as
    Product "*" -- "*" Portfolio : included in
    Portfolio "1" -- "*" DailyReport : generates
    
    Decision "1" -- "*" Investment : leads to
    Decision "1" -- "0..1" QuestionnaireAnswer : may include
```

## Relationship Summary Table

| Relationship | Type | Description | Cardinality |
|--------------|------|-------------|-------------|
| Customer → UserAccount | One-to-Many | Customer can have multiple accounts | 1:N |
| Customer → Decision | One-to-Many | Customer makes multiple decisions | 1:N |
| Customer → QuestionnaireAnswer | One-to-Many | Customer provides multiple answers | 1:N |
| Customer → Investment | One-to-Many | Customer makes multiple investments | 1:N |
| Customer → Portfolio | One-to-Many | Customer owns multiple portfolios | 1:N |
| Questionnaire → Question | One-to-Many | Questionnaire contains multiple questions | 1:N |
| Question → QuestionnaireAnswer | One-to-Many | Question can have multiple answers from different customers | 1:N |
| QuestionnaireAnswer → RiskAssessment | One-to-One | Each answer generates one risk assessment | 1:1 |
| QuestionnaireAnswer → AffordabilityScore | One-to-One | Each answer calculates one affordability score | 1:1 |
| Product → Investment | One-to-Many | Product can be purchased as multiple investments | 1:N |
| Product → Portfolio | Many-to-Many | Products can be included in multiple portfolios | M:N |
| Portfolio → DailyReport | One-to-Many | Portfolio generates multiple daily reports | 1:N |
| Decision → Investment | One-to-Many | Decision leads to multiple investments | 1:N |
| Decision → QuestionnaireAnswer | Zero-or-One-to-One | Decision may include questionnaire answers | 0..1:1 |

## Business Logic Implementation

### Customer Journey Flow
1. **Visitor Phase**: View company background → Register account → Fill basic information
2. **Decision Point**: Choose between:
   - Path A: Direct purchase without questionnaire
   - Path B: Complete questionnaire for assessment
3. **Assessment Phase** (Path B only):
   - Risk level assessment
   - Affordability calculation
   - Income percentage analysis
4. **Product Selection**:
   - High/Medium/Low return options
   - Based on preference or system recommendation
5. **Investment Management**:
   - Portfolio creation
   - Daily performance reporting
   - Option to change/quit investments

### Key Business Rules
1. **Questionnaire Scoring**:
   - Psychological questions determine risk tolerance
   - Demographic questions determine affordability
   - Weighted ratio calculation for investment capacity
   
2. **Product Eligibility**:
   - Risk level must match customer's risk assessment
   - Investment amount must be within affordable range
   - Minimum investment requirements per product
   
3. **Portfolio Management**:
   - Customers can have multiple portfolios
   - Portfolios can contain multiple products
   - Daily performance tracking and reporting
   
4. **Decision Tracking**:
   - Record all customer decisions
   - Track questionnaire completion status
   - Monitor investment paths chosen

### System Features
1. **Background Information**: Company history, credentials, philosophy
2. **Questionnaire System**: Risk assessment + affordability calculation
3. **Decision Support**: Recommendations based on questionnaire results
4. **Product Catalog**: High/Medium/Low return investment options
5. **Portfolio Management**: Investment tracking and reporting
6. **Customer Management**: Account management and profile updates

This UML diagram captures the complete system architecture based on your detailed requirements, including all entities, relationships, and business logic for the financial investment platform.
