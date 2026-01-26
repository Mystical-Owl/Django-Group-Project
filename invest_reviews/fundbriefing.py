# fundbriefing.py - Static fund briefings (fake data for illustration)

fund_briefs = {
    'A': {
        'short': "Conviction Growth Fund (A) offers a balanced USD-denominated portfolio for moderate growth, blending global stocks (US, Europe, Japan, China, emerging markets), bonds (Treasuries, corporates), and precious metals. Objective: 12–16% annual returns with controlled risk. From 2016–2025, it achieved **17.79% CAGR** (end value ~514 USD), delivering solid performance with reasonable volatility. Suitable for investors seeking balanced appreciation and income.",
        'long': """
**Investment Objective:**  
Conviction Growth Fund (A) is a balanced diversified portfolio fund denominated in USD, designed for moderate-risk investors seeking steady capital appreciation and income over the medium to long term. It aims to achieve a balanced return by allocating investments across global equities, fixed income, and alternative assets, while mitigating volatility through diversification. The fund targets an annual return of around 12–16% over rolling 5-year periods, focusing on sustainable growth with moderate exposure to global markets.

**Assets Invested:**  
The fund maintains a diversified allocation: approximately 50% in equities, including 20% US stocks (e.g., S&P 500 constituents like Apple and Microsoft), 15% European stocks (e.g., via FTSE Europe indices), 5% Japanese equities (e.g., Nikkei components like Toyota), 5% Chinese stocks (e.g., Alibaba, Tencent via ADRs), and 5% in other emerging markets (e.g., India, Brazil via ETFs). Fixed income comprises 35%, split between US Treasury bonds (20%) for stability and investment-grade corporate bonds (15%) from issuers like JPMorgan and Verizon. The remaining 15% is in precious metals, primarily gold and silver ETFs, acting as a hedge against inflation and geopolitical risks. Rebalancing occurs quarterly to maintain this mix, with a focus on ESG-compliant assets.

**Past Performance (2016–2025):**  
From 2016 to 2025, Conviction Growth Fund (A) delivered strong and relatively consistent performance, growing from a base value of 100 USD to approximately 514.24 USD by end-2025, reflecting a compound annual growth rate (CAGR) of **17.79%**. Early years (2016–2018) showed solid gains averaging around 12–14% annually, supported by global equity rallies and stable bond markets. The fund experienced moderate drawdowns in volatile periods but maintained resilience. It delivered particularly strong returns in the later years (2023–2025), contributing significantly to the overall period performance. Overall volatility was around 15–18%, making Conviction Growth Fund (A) a well-balanced choice between growth and stability compared to more aggressive or conservative peers. Past performance is not indicative of future results.
"""
    },
    'B': {
        'short': "Diversified Assets Fund (B) is a USD conservative portfolio emphasizing preservation, investing in global stocks (US, Europe, Japan, China, emerging), bonds (Treasuries, corporates), and precious metals. Objective: 9–13% returns with low risk. From 2016–2025, it achieved **10.57% CAGR** (end value ~273 USD), showing very good stability and better-than-expected performance. Ideal for cautious investors.",
        'long': """
**Investment Objective:**  
Diversified Assets Fund (B) is a conservative diversified portfolio fund in USD, tailored for risk-averse investors prioritizing capital preservation and modest income generation. It focuses on low-volatility growth, aiming for 9–13% annual returns over the long term, with an emphasis on defensive assets to weather market downturns while providing steady dividends and interest.

**Assets Invested:**  
Allocations are skewed toward stability: 40% in equities, with 15% US stocks (defensive sectors like utilities and consumer staples, e.g., Procter & Gamble), 10% European (stable blue-chips like Nestlé), 5% Japanese (yen-hedged firms like Uniqlo parent Fast Retailing), 5% Chinese (state-backed enterprises via ETFs), and 5% emerging markets (selective low-vol funds). Fixed income dominates at 50%, including 30% US Treasury bonds for safety and 20% high-quality corporate bonds (e.g., from AAA-rated issuers like Johnson & Johnson). Precious metals make up 10%, mainly gold as a safe-haven. The fund employs hedging strategies and annual rebalancing to minimize drawdowns.

**Past Performance (2016–2025):**  
Over 2016–2025, Diversified Assets Fund (B) grew from 100 USD to approximately 273.13 USD, achieving a compound annual growth rate (CAGR) of **10.57%** — exceeding its conservative target due to favorable market conditions in several years. The period showed steady progress with relatively mild drawdowns compared to more aggressive funds. Early years benefited from bond yields and defensive equity positions, while later years (especially 2023–2025) saw stronger contributions from stabilizing global markets. Overall volatility remained low at around 10–12%, confirming its position as the most defensive among the diversified equity-oriented funds. Past performance does not guarantee future results.
"""
    },
    'C': {
        'short': "Balanced Horizon Fund (C) aggressively pursues growth in USD, via heavy global equities (US, Europe, Japan, China, emerging), bonds (Treasuries, corporates), and precious metals. Objective: 15–25%+ returns for risk-tolerant investors. From 2016–2025, it achieved an exceptional **20.81% CAGR** (end value ~662 USD), driven by strong growth cycles. Best suited for high-reward, high-volatility seekers.",
        'long': """
**Investment Objective:**  
Balanced Horizon Fund (C) is an aggressive diversified portfolio fund in USD, geared toward high-growth investors willing to tolerate higher volatility for superior long-term returns. It seeks capital maximization, targeting 15–25%+ returns in favorable periods, by significantly overweighting equities and alternatives while using bonds for limited ballast.

**Assets Invested:**  
The fund is equity-heavy at 65%: 25% US stocks (growth-oriented like Tesla, Amazon), 15% European (tech and industrials, e.g., ASML), 10% Japanese (innovation sectors like Sony), 10% Chinese (high-growth tech via Hong Kong listings), and 5% other emerging markets (e.g., Taiwan Semiconductor). Fixed income is lighter at 20%, with 10% US Treasuries and 10% corporate bonds (higher-yield BBB-rated from growth companies). Precious metals allocate 15%, including silver for industrial demand exposure. Dynamic rebalancing allows tactical shifts toward high-potential regions.

**Past Performance (2016–2025):**  
Balanced Horizon Fund (C) exhibited very strong and volatile performance from 2016 to 2025, growing from 100 USD to approximately 662.10 USD by end-2025, delivering an outstanding compound annual growth rate (CAGR) of **20.81%** during this period. The fund capitalized on multiple growth cycles, particularly in technology and emerging markets, with several years of exceptional returns (including periods exceeding 30–40%). Drawdowns occurred during global risk-off events, but recoveries were rapid and powerful. Overall volatility was in the 20–22% range, clearly reflecting its aggressive nature. This period represents one of the strongest performances among the funds. Past performance is no indicator of future outcomes.
"""
    },
    'D': {
        'short': "Money Market Fund (D), a USD money market fund, focuses on preservation and liquidity via short-term Treasuries, corporates, and agencies. Objective: 2–4% stable returns. From 2016–2025, it achieved **2.42% CAGR** (end value ~127 USD), delivering very consistent performance with virtually zero volatility. Perfect for parking cash safely.",
        'long': """
**Investment Objective:**  
Money Market Fund (D) is a USD-denominated money market fund, ideal for conservative investors focused on liquidity, capital preservation, and short-term income. It aims for stable returns around 2–4% annually, exceeding inflation with minimal risk, by investing in high-quality, short-term instruments to ensure principal safety and easy access.

**Assets Invested:**  
Primarily in ultra-safe, liquid assets: 60% US Treasury bills and notes (maturing within 1 year), 30% high-grade corporate commercial paper and certificates of deposit from top-rated banks (e.g., Bank of America), and 10% in government agency securities or repurchase agreements. No equity or precious metal exposure to avoid volatility; all holdings are USD-based with average maturity under 60 days. Daily liquidity is prioritized, with no lock-up periods.

**Past Performance (2016–2025):**  
From 2016 to 2025, Money Market Fund (D) provided very consistent and low-volatility returns, growing from 100 USD to approximately 127.03 USD, with a compound annual growth rate (CAGR) of **2.42%**. Performance was highly stable across the entire period, with negligible drawdowns even during market turbulence. The fund benefited from gradually rising short-term rates in the later years, delivering slightly higher yields toward the end of the period while maintaining principal protection. Volatility remained extremely low at ~0.5–0.7%. This makes Money Market Fund (D) an excellent cash-equivalent option with reliable, if modest, returns. Past performance does not predict future results.
"""
    },
}