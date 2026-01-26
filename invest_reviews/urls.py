from django.urls import path
from .views import (
    invest_reviews_view,
    portfolio_view,
    fund_descriptions_view,  # placeholder
    fund_detail_view,        # placeholder
    performance_since_founded_view,  # placeholder
    fund_individual_since_founded_view,  # placeholder
    this_year_performance_view,  # placeholder
    more_to_see_view,  # placeholder
)

app_name = 'invest_reviews'  # MUST have this

urlpatterns = [
    path('', invest_reviews_view, name='main'),  # Main page
    path('portfolio/', portfolio_view, name='portfolio'),
    
    # Add these lines (even if views are placeholders)
    path('fund-descriptions/', fund_descriptions_view, name='fund_descriptions'),
    path('fund-detail/<str:fund_key>/', fund_detail_view, name='fund_detail'),
    path('performance-since-founded/', performance_since_founded_view, name='performance_since_founded'),
    path('fund-since-founded/<str:fund_key>/', fund_individual_since_founded_view, name='fund_since_founded'),
    path('this-year-performance/', this_year_performance_view, name='this_year_performance'),
    path('more-to-see/', more_to_see_view, name='more_to_see'),
]