# Financial Investment System UML Diagram with Workflow

## Overview
This document combines the static UML class diagram with dynamic workflow diagrams based on the UI/UX workflow description. It provides a comprehensive view of both structure and behavior.

## Static Structure: Class Diagram

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

## Dynamic Behavior: Workflow Diagrams

### 1. Visitor Registration Journey
*Based on UI/UX workflow: Visitor → Registered User Journey*

```mermaid
sequenceDiagram
    participant V as Visitor
    participant S as System
    participant DB as Database
    
    V->>S: Browse landing page
    S->>V: Show company background
    V->>S: Click "Register"
    S->>V: Display registration form
    V->>S: Submit registration details
    S->>DB: Create Customer record
    S->>DB: Create UserAccount record
    DB-->>S: Success
    S->>V: Show profile setup form
    V->>S: Submit profile details
    S->>DB: Update Profile
    DB-->>S: Success
    S->>V: Show investment approach choice
    V->>S: Choose path (Questionnaire/Direct)
    S->>DB: Create Decision record
    DB-->>S: Success
    S->>V: Redirect to dashboard
```

### 2. Investment Decision Journey - Questionnaire Path
*Based on UI/UX workflow: Questionnaire Path*

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant Q as Questionnaire
    participant RA as RiskAssessment
    participant AS as AffordabilityScore
    participant P as Product
    participant I as Investment
    
    U->>S: Start questionnaire
    S->>Q: Load questions
    Q-->>S: Question list
    S->>U: Display question 1
    loop Each question
        U->>S: Submit answer
        S->>Q: Save answer
        Q-->>S: Acknowledge
        S->>U: Next question
    end
    U->>S: Complete questionnaire
    S->>RA: Calculate risk assessment
    RA-->>S: Risk level & score
    S->>AS: Calculate affordability
    AS-->>S: Affordable amount
    S->>U: Show recommendations
    U->>S: Select product
    S->>P: Check eligibility
    P-->>S: Eligible
    S->>U: Show investment form
    U->>S: Enter investment amount
    S->>AS: Validate affordability
    AS-->>S: Approved
    S->>I: Create investment
    I-->>S: Created
    S->>U: Show confirmation
```

### 3. Investment Decision Journey - Direct Purchase Path
*Based on UI/UX workflow: Direct Purchase Path*

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant P as Product
    participant I as Investment
    
    U->>S: Browse investment options
    S->>P: Get product list
    P-->>S: Product details
    S->>U: Display products
    U->>S: Select product directly
    S->>P: Get product details
    P-->>S: Details
    S->>U: Show investment form
    U->>S: Enter investment amount
    S->>P: Validate min/max investment
    P-->>S: Valid
    S->>I: Create investment
    I-->>S: Created
    S->>U: Show confirmation
```

### 4. Questionnaire Flow (Detailed Interaction)
*Based on UI/UX workflow: Questionnaire Flow*

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant Q as Question
    participant QA as QuestionnaireAnswer
    
    U->>S: Click "Start Questionnaire"
    S->>U: Show first question with progress
    U->>S: Select answer
    S->>QA: Save answer
    QA-->>S: Saved
    S->>U: Enable "Next" button
    U->>S: Click "Next"
    S->>Q: Load next question
    Q-->>S: Question data
    S->>U: Display next question
    Note over U,S: Repeat until all questions
    U->>S: Complete all questions
    S->>S: Calculate risk score
    S->>U: Show results & recommendations
```

### 5. Investment Process Flow
*Based on UI/UX workflow: Investment Process*

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant P as Product
    participant I as Investment
    participant PMT as Payment
    
    U->>S: Select investment
    S->>P: Get detailed information
    P-->>S: Details + risk disclosure
    S->>U: Show investment details
    U->>S: Click "Invest"
    S->>U: Show investment amount form
    U->>S: Enter amount
    S->>P: Validate min/max limits
    P-->>S: Valid
    S->>U: Show payment options
    U->>S: Select payment method
    S->>PMT: Process payment
    PMT-->>S: Payment successful
    S->>I: Create investment record
    I-->>S: Record created
    S->>U: Show confirmation
```

### 6. Dashboard Interaction Flow
*Based on UI/UX workflow: Dashboard Interactions*

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant I as Investment
    participant R as Report
    
    U->>S: Login
    S->>S: Load personalized data
    S->>U: Display dashboard
    U->>S: Hover over investment
    S->>I: Get investment details
    I-->>S: Details
    S->>U: Show tooltip
    U->>S: Click "Edit" on investment
    S->>U: Open edit modal
    U->>S: Adjust allocation
    S->>S: Recalculate portfolio balance
    S->>U: Update display
    U->>S: Request report
    S->>R: Generate PDF report
    R-->>S: Report ready
    S->>U: Download PDF
```

## Integrated View: Connecting Structure with Flow

### How Classes Participate in Workflows

| Workflow | Key Participating Classes | Interactions |
|----------|---------------------------|--------------|
| Visitor Registration | Customer, UserAccount, Decision | Customer registers → UserAccount created → Decision recorded |
| Questionnaire Path | Customer, Questionnaire, Question, QuestionnaireAnswer, RiskAssessment, AffordabilityScore | Customer answers questions → Answers stored → Risk & Affordability calculated |
| Direct Purchase Path | Customer, Product, Investment, Decision | Customer selects product → Investment created → Decision recorded |
| Investment Process | Customer, Product, Investment, Portfolio | Customer invests → Investment linked to Product → Added to Portfolio |
| Dashboard | Customer, Investment, Portfolio, DailyReport | Customer views dashboard → Investments displayed → Reports generated |

### Business Rules Implementation

1. **Path Decision**: 
   - `Decision.chosen_path` determines whether user took questionnaire or direct purchase
   - `Decision.completed_questionnaire` boolean flag

2. **Risk Matching**:
   - `Product.risk_level` must match `RiskAssessment.risk_level` for recommendations
   - `Investment.investment_amount` must be within `Product.min_investment` and `Product.max_investment`

3. **Affordability Validation**:
   - `Investment.investment_amount` ≤ `AffordabilityScore.affordable_amount`
   - Calculated as `Profile.monthly_income` × `AffordabilityScore.income_percentage`

4. **Portfolio Management**:
   - `Portfolio.total_value` = sum of `Investment.current_value` for all investments in portfolio
   - `DailyReport` generated daily for each active portfolio

## Relationship Summary

| Relationship | Cardinality | Description | Flow Involvement |
|--------------|-------------|-------------|------------------|
| Customer → UserAccount | 1:N | Customer can have multiple accounts | Registration flow |
| Customer → Decision | 1:N | Customer makes multiple decisions | Decision point flow |
| Customer → QuestionnaireAnswer | 1:N | Customer provides multiple answers | Questionnaire flow |
| Customer → Investment | 1:N | Customer makes multiple investments | Investment flow |
| Customer → Portfolio | 1:N | Customer owns multiple portfolios | Portfolio management flow |
| Questionnaire → Question | 1:N | Questionnaire contains multiple questions | Questionnaire flow |
| Question → QuestionnaireAnswer | 1:N | Question can have multiple answers | Questionnaire flow |
| QuestionnaireAnswer → RiskAssessment | 1:1 | Each answer generates one risk assessment | Risk assessment flow |
| QuestionnaireAnswer → AffordabilityScore | 1:1 | Each answer calculates one affordability score | Affordability flow |
| Product → Investment | 1:N | Product can be purchased as multiple investments | Investment flow |
| Product → Portfolio | M:N | Products can be included in multiple portfolios | Portfolio composition |
| Portfolio → DailyReport | 1:N | Portfolio generates multiple daily reports | Reporting flow |
| Decision → Investment | 1:N | Decision leads to multiple investments | Decision tracking |

## Conclusion

This integrated UML diagram with workflow provides a complete picture of the financial investment system:
- **Static structure** shows the entities and their relationships
- **Dynamic behavior** shows how users interact with the system through key workflows
- **Connection points** illustrate how classes participate in each workflow

The diagrams use the terminology and flow descriptions from the UI/UX workflow document, ensuring consistency between design and implementation.