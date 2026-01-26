# Financial Investment System Flow Diagram

## Overview
This flowchart shows the complete workflow of the financial investment system as described, with boxes representing key entities and arrows showing the flow of processes. Each box is numbered for easy referral (e.g., A1, B2, C3).

## Flowchart

```mermaid
graph TD
    %% Define nodes with numbered labels for easy referral
    A1[Customer] --> B2[User Account]
    B2 --> C3[Decision]
    
    %% Decision branching
    C3 --> D4[Investment]  %% Direct path
    C3 --> E5[Questionnaire]  %% Questionnaire path
    
    %% Questionnaire path
    E5 --> F6[QuestionAnswer]
    F6 --> G7[Risk Assessment]
    G7 --> H8[Affordability Score]
    H8 --> I9[Product]
    I9 --> D4  %% Join back to Investment
    
    %% Post-investment flow
    D4 --> J10[Portfolio]
    J10 --> K11[Daily Report]
    
    %% Additional relationship
    I9 --> J10  %% Portfolio sourced from Products
    
    %% Styling for clarity
    style A1 fill:#e1f5fe
    style B2 fill:#e1f5fe
    style C3 fill:#fff3e0
    style D4 fill:#f3e5f5
    style E5 fill:#e8f5e8
    style F6 fill:#e8f5e8
    style G7 fill:#e8f5e8
    style H8 fill:#e8f5e8
    style I9 fill:#fce4ec
    style J10 fill:#f3e5f5
    style K11 fill:#e8f5e8
    
    %% Add labels for paths
    linkStyle 2 stroke:#ff6b6b,stroke-width:2px,color:#ff6b6b;
    linkStyle 3 stroke:#4caf50,stroke-width:2px,color:#4caf50;
```

## Numbered Box Reference

| Box ID | Entity | Description |
|--------|--------|-------------|
| A1 | Customer | Individual user of the system |
| B2 | User Account | Login credentials and basic profile |
| C3 | Decision | User's choice of investment path (direct vs questionnaire) |
| D4 | Investment | Actual investment made by user |
| E5 | Questionnaire | Set of risk and demographic questions |
| F6 | QuestionAnswer | User's responses to questionnaire questions |
| G7 | Risk Assessment | Calculated risk tolerance level |
| H8 | Affordability Score | Calculated affordable investment amount |
| I9 | Product | Investment product (fund, insurance, etc.) |
| J10 | Portfolio | Collection of user's investments |
| K11 | Daily Report | Daily performance report for portfolio |

## Flow Description

### Primary Flow
1. **A1 (Customer)** creates a **B2 (User Account)**
2. **B2 (User Account)** leads to a **C3 (Decision)** point
3. **C3 (Decision)** branches into two possible paths:

### Path 1: Direct Investment (Red Arrow)
- **C3 (Decision)** → **D4 (Investment)** (direct purchase without questionnaire)

### Path 2: Questionnaire-Based Investment (Green Arrow)
- **C3 (Decision)** → **E5 (Questionnaire)** → **F6 (QuestionAnswer)** → **G7 (Risk Assessment)** → **H8 (Affordability Score)** → **I9 (Product)** → **D4 (Investment)**

### Post-Investment Flow
- **D4 (Investment)** → **J10 (Portfolio)** (investment added to portfolio)
- **J10 (Portfolio)** → **K11 (Daily Report)** (performance reporting)

### Additional Relationship
- **I9 (Product)** → **J10 (Portfolio)** (products are included in portfolios)

## Key Points

1. **Two Investment Paths**: The system supports both direct investment (for experienced users) and questionnaire-based investment (for personalized recommendations).

2. **Risk & Affordability Assessment**: The questionnaire path includes comprehensive assessment:
   - **F6 (QuestionAnswer)**: User's responses to risk and demographic questions
   - **G7 (Risk Assessment)**: Calculated risk tolerance level
   - **H8 (Affordability Score)**: Calculated affordable investment amount

3. **Product Selection**: Based on assessment results, appropriate products are recommended.

4. **Portfolio Management**: All investments are organized into portfolios for tracking.

5. **Reporting**: Daily reports track portfolio performance.

## Entity Definitions

| Entity | Description |
|--------|-------------|
| Customer | Individual user of the system |
| User Account | Login credentials and basic profile |
| Decision | User's choice of investment path (direct vs questionnaire) |
| Questionnaire | Set of risk and demographic questions |
| QuestionAnswer | User's responses to questionnaire questions |
| Risk Assessment | Calculated risk tolerance level |
| Affordability Score | Calculated affordable investment amount |
| Product | Investment product (fund, insurance, etc.) |
| Investment | Actual investment made by user |
| Portfolio | Collection of user's investments |
| Daily Report | Daily performance report for portfolio |

## Business Rules Embedded in Flow

1. **Path Selection**: User must choose either direct or questionnaire path at Decision point.
2. **Assessment Requirement**: Questionnaire path requires completion of all assessment steps before product selection.
3. **Product Eligibility**: Products must match user's risk assessment and affordability score.
4. **Portfolio Composition**: Portfolios can contain multiple investments from multiple products.
5. **Daily Tracking**: Every portfolio generates daily performance reports.

## Comparison with UML Class Diagram

This flowchart complements the UML class diagram by showing:
- **Temporal sequence** of interactions (vs static relationships)
- **Decision points** and branching logic
- **Process flow** through the system
- **Two distinct investment pathways**

The class diagram shows entity attributes and relationships, while this flowchart shows the operational workflow.