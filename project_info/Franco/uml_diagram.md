# Financial Investment System UML Diagram (With Visitors and Administrators)

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Visitor and User Management
    Visitor ||--o{ User : "registers as"
    Administrator ||--o{ User : "manages"
    Administrator ||--o{ Company : "manages"
    
    %% Core User Entities
    User ||--o{ Profile : "has one"
    User ||--o{ UserQuestionaireAnswer : "answers"
    User ||--o{ UserInvestment : "invests in"
    User ||--o{ UserDecision : "makes decisions"
    
    %% Questionnaire System
    Questionaire ||--o{ QuestionaireAnswer : "has answers"
    QuestionaireAnswer ||--o{ UserQuestionaireAnswer : "selected by users"
    
    %% Investment System
    InvestmentType ||--o{ InvestmentChoice : "categorizes"
    InvestmentChoice ||--o{ InvestmentData : "has historical data"
    InvestmentChoice ||--o{ UserInvestment : "chosen by users"
    InvestmentChoice ||--o{ Portfolio : "belongs to portfolio"
    
    %% Enhanced Business Entities
    Portfolio ||--o{ InvestmentChoice : "contains"
    Company ||--o{ Portfolio : "offers"
    UserDecision ||--o{ UserInvestment : "leads to"
    UserInvestment ||--o{ DailyReport : "generates"
    
    %% Entity Definitions
    Visitor {
        string session_id PK
        string ip_address
        datetime first_visit
        datetime last_visit
        int page_views
        string referral_source
    }
    
    Administrator {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
        boolean is_active
    }
    
    User {
        int id PK
        string username
        string email
        string password_hash
        datetime date_joined
        boolean is_active
        string user_type
        int visitor_session_id FK
    }
    
    Profile {
        int id PK
        int user_id FK
        int age
        text address
        string telephone
        string gender
        string occupation
        decimal monthly_income
        decimal investment_percentage
    }
    
    Questionaire {
        int id PK
        string questionaire_statement
        string questionaire_type
        int sort_order
        string category
        int created_by FK
    }
    
    QuestionaireAnswer {
        int id PK
        int questionaire_id FK
        string questionaire_answer
        float answer_score
        float answer_weight
        int sort_order
    }
    
    UserQuestionaireAnswer {
        int id PK
        int user_id FK
        int questionaire_answer_id FK
        datetime answered_at
    }
    
    InvestmentType {
        int id PK
        string investment_type
        int created_by FK
    }
    
    InvestmentChoice {
        int id PK
        string investment_name
        int investment_type_id FK
        string investment_description
        string risk_level
        decimal expected_return
        int portfolio_id FK
        int created_by FK
    }
    
    InvestmentData {
        int id PK
        int investment_choice_id FK
        datetime investment_date
        float investment_price
        int uploaded_by FK
    }
    
    UserInvestment {
        int id PK
        int user_id FK
        int investment_choice_id FK
        datetime begin_date
        datetime end_date
        float investment_amount
        string status
        int decision_id FK
    }
    
    Company {
        int id PK
        string name
        text background
        text company_view
        string license_number
        datetime established_date
        int admin_id FK
    }
    
    Portfolio {
        int id PK
        string name
        string description
        string risk_level
        int company_id FK
        decimal min_investment
        decimal max_investment
        int created_by FK
    }
    
    UserDecision {
        int id PK
        int user_id FK
        string decision_type
        datetime decision_date
        boolean completed_questionnaire
        string chosen_path
        text notes
    }
    
    DailyReport {
        int id PK
        int user_investment_id FK
        datetime report_date
        decimal current_value
        decimal daily_return
        decimal total_return
        text performance_notes
        int generated_by FK
    }
```

## Class Diagram with Relationships

```mermaid
classDiagram
    %% Visitor and Administrator Entities
    class Visitor {
        +string session_id
        +string ip_address
        +datetime first_visit
        +datetime last_visit
        +int page_views
        +string referral_source
        +browseSite()
        +viewBackground()
        +startRegistration()
        +trackActivity()
    }
    
    class Administrator {
        +int id
        +string username
        +string email
        +string password_hash
        +string role
        +datetime created_at
        +boolean is_active
        +manageUsers()
        +manageContent()
        +viewReports()
        +configureSystem()
        +uploadInvestmentData()
    }
    
    %% User and Profile
    class User {
        +int id
        +string username
        +string email
        +string password_hash
        +datetime date_joined
        +boolean is_active
        +string user_type
        +Visitor visitor
        +login()
        +register()
        +viewBackground()
        +makeDecision()
        +convertFromVisitor()
    }
    
    class Profile {
        +int id
        +User user
        +int age
        +text address
        +string telephone
        +string gender
        +string occupation
        +decimal monthly_income
        +decimal investment_percentage
        +updateProfile()
        +calculateAffordability()
    }
    
    %% Questionnaire System
    class Questionaire {
        +int id
        +string questionaire_statement
        +string questionaire_type
        +int sort_order
        +string category
        +Administrator created_by
        +getQuestions()
        +getRiskQuestions()
        +getDemographicQuestions()
    }
    
    class QuestionaireAnswer {
        +int id
        +Questionaire questionaire
        +string questionaire_answer
        +float answer_score
        +float answer_weight
        +int sort_order
        +calculateScore()
    }
    
    class UserQuestionaireAnswer {
        +int id
        +User user
        +QuestionaireAnswer questionaire_answer
        +datetime answered_at
        +saveAnswer()
    }
    
    %% Investment System
    class InvestmentType {
        +int id
        +string investment_type
        +Administrator created_by
        +getTypeDetails()
    }
    
    class InvestmentChoice {
        +int id
        +string investment_name
        +InvestmentType investment_type
        +string investment_description
        +string risk_level
        +decimal expected_return
        +Portfolio portfolio
        +Administrator created_by
        +getRiskLevel()
        +getExpectedReturn()
        +getPerformance()
    }
    
    class InvestmentData {
        +int id
        +InvestmentChoice investment_choice
        +datetime investment_date
        +float investment_price
        +Administrator uploaded_by
        +getHistoricalData()
        +calculatePerformance()
        +generateChart()
    }
    
    class UserInvestment {
        +int id
        +User user
        +InvestmentChoice investment_choice
        +datetime begin_date
        +datetime end_date
        +float investment_amount
        +string status
        +UserDecision decision
        +startInvestment()
        +quitInvestment()
        +calculateReturn()
        +generateReport()
        +changeInvestment()
    }
    
    %% Enhanced Business Entities
    class Company {
        +int id
        +string name
        +text background
        +text company_view
        +string license_number
        +datetime established_date
        +Administrator admin
        +displayBackground()
        +getPortfolios()
        +updateCompanyInfo()
    }
    
    class Portfolio {
        +int id
        +string name
        +string description
        +string risk_level
        +Company company
        +decimal min_investment
        +decimal max_investment
        +Administrator created_by
        +getInvestmentChoices()
        +calculatePerformance()
        +getRiskLevel()
    }
    
    class UserDecision {
        +int id
        +User user
        +string decision_type
        +datetime decision_date
        +boolean completed_questionnaire
        +string chosen_path
        +text notes
        +recordDecision()
        +getDecisionSummary()
    }
    
    class DailyReport {
        +int id
        +UserInvestment user_investment
        +datetime report_date
        +decimal current_value
        +decimal daily_return
        +decimal total_return
        +text performance_notes
        +Administrator generated_by
        +generateReport()
        +sendNotification()
        +getPerformanceTrend()
    }
    
    %% Relationships
    Visitor "1" -- "*" User : registers as
    Administrator "1" -- "*" User : manages
    Administrator "1" -- "*" Company : manages
    Administrator "1" -- "*" Questionaire : creates
    Administrator "1" -- "*" InvestmentType : creates
    Administrator "1" -- "*" InvestmentChoice : creates
    Administrator "1" -- "*" Portfolio : creates
    Administrator "1" -- "*" InvestmentData : uploads
    Administrator "1" -- "*" DailyReport : generates
    
    User "1" -- "1" Profile : has
    User "1" -- "*" UserQuestionaireAnswer : answers
    User "1" -- "*" UserInvestment : invests
    User "1" -- "*" UserDecision : makes
    
    Questionaire "1" -- "*" QuestionaireAnswer : contains
    QuestionaireAnswer "1" -- "*" UserQuestionaireAnswer : selected by
    
    InvestmentType "1" -- "*" InvestmentChoice : categorizes
    InvestmentChoice "1" -- "*" InvestmentData : has data for
    InvestmentChoice "1" -- "*" UserInvestment : chosen in
    InvestmentChoice "*" -- "1" Portfolio : belongs to
    
    Portfolio "1" -- "*" InvestmentChoice : contains
    Company "1" -- "*" Portfolio : offers
    UserDecision "1" -- "*" UserInvestment : leads to
    UserInvestment "1" -- "*" DailyReport : generates
```

## Relationship Summary Table

| Relationship | Type | Description |
|--------------|------|-------------|
| User → Profile | One-to-One | Each user has one profile with personal details |
| User → UserQuestionaireAnswer | One-to-Many | User can answer multiple questionnaire questions |
| User → UserInvestment | One-to-Many | User can have multiple investments |
| Questionaire → QuestionaireAnswer | One-to-Many | Each question has multiple possible answers |
| QuestionaireAnswer → UserQuestionaireAnswer | One-to-Many | Each answer can be selected by multiple users |
| InvestmentType → InvestmentChoice | One-to-Many | Each investment type has multiple choices |
| InvestmentChoice → InvestmentData | One-to-Many | Each investment choice has multiple historical data points |
| InvestmentChoice → UserInvestment | One-to-Many | Each investment choice can be selected by multiple users |

## Enhanced Business Logic Entities (Based on Requirements)

The following entities would need to be added to fully implement your described system:

1. **Company** - Background information, licensing
2. **Decision** - User's choice to proceed with/without questionnaire
3. **Portfolio** - Collection of investments (High/Medium/Low risk levels)
4. **Product** - Specific insurance/fund products
5. **DailyReport** - Performance tracking reports
6. **RiskAssessment** - Calculated risk scores from questionnaires
7. **AffordabilityScore** - Income percentage calculations

## Key Business Rules Captured

1. **Customer Journey**: User → Questionnaire → Risk Assessment → Investment Suggestion → Portfolio Selection
2. **Investment Options**: Direct purchase (without questionnaire) vs. Questionnaire-based recommendation
3. **Risk Levels**: High/Medium/Low return portfolios based on risk tolerance
4. **Performance Tracking**: Daily reports on portfolio performance
5. **Flexibility**: Users can quit investments or change portfolios

## Next Steps for Implementation

To fully implement your described system, consider adding these models:

1. Add `risk_score`, `affordability_score`, `income_percentage` fields to UserQuestionaireAnswer or a new RiskAssessment model
2. Create Portfolio model linking multiple InvestmentChoices with risk levels
3. Add Decision model to track user's choice path (direct purchase vs questionnaire)
4. Create DailyReport model for performance tracking
5. Add Company model for background information

This UML diagram provides a comprehensive view of both the existing system and the extended requirements for your financial investment platform.
