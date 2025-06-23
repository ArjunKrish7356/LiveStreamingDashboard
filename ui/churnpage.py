import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from features.churn import total_and_categorial_churn

def churnpage(event_df, users_df, churn_model, churn_reason_model):
    """
    This is a streamlit page. The background color should be white and the default color of text should be black.
    The components in this page are
        - A donut chart in the top left area(center) and inside it should be percentage
        - A graph which has vertical graph lines in 4 category(name them as 1, 2 ,3 ,4) and the y axis should be percentage from 0 to 100
        - The bottom will have a table. For now have 10 people from 1 to 10. The table should be scrollable and it should only take 40 percentage of screen height and 80 percentage of screen width
    """
    
    # Apply custom CSS for white background, black text, and full screen utilization
    st.markdown("""
        <style>
        .main {
            background-color: white !important;
            color: black !important;
            padding: 0rem 1rem !important;
        }
        .stApp {
            background-color: white !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        /* Make all text black and visible */
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: black !important;
        }
        .stDataFrame {
            color: black !important;
        }
        div[data-testid="metric-container"] {
            background-color: white !important;
            border: 1px solid #ddd;
            padding: 5% 5% 5% 10%;
            border-radius: 5px;
            color: black !important;
        }
        /* Force table text to be black */
        .dataframe thead tr th {
            color: black !important;
            background-color: #f0f0f0 !important;
        }
        .dataframe tbody tr td {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: black; margin-bottom: 1rem;">Churn Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")

    # using calculate churn function from features find the churn stats
    total_churn_percent, user_data = total_and_categorial_churn(event_df, users_df, churn_model, churn_reason_model)
    each_type_of_user = {}
    for user_id, reason in user_data:
        if reason not in each_type_of_user:
            each_type_of_user[reason] = 1
        else:
            each_type_of_user[reason] += 1
 
    # The data will be used by the bar chart (top right).
    if len(user_data) > 0:
        category_data = {
            'Category': [key for key in each_type_of_user.keys()],
            'Percentage': [val*100/len(user_data) for val in each_type_of_user.values()]
        }
    else:
        category_data = {
            'Category': ['No Risk Users'],
            'Percentage': [100]
        }

   # Data for the table at bottom. The keys ('User ID, Reason..etc) are column names
    bottom_table_data = {
        'User ID': [user[0] for user in user_data],
        'Reason': [user[1] for user in user_data]
    }

    # DONUT CHART (Left column)
    with col1:
        st.markdown('<h3 style="color: black;">Overall Churn Rate</h3>', unsafe_allow_html=True)
        
        # Get total user count for hover display
        total_users = len(event_df['user_id'].unique()) if not event_df.empty else 1
        at_risk_count = int(total_churn_percent * total_users)
        safe_count = total_users - at_risk_count
        
        # Create donut chart
        fig_donut = go.Figure(data=[go.Pie(
            labels=['At Risk', 'Safe'], 
            values=[total_churn_percent * 100, 100 - (total_churn_percent * 100)],
            hole=.6,
            marker_colors=['#ff6b6b', '#51cf66'],
            hovertemplate='<b>%{label}</b><br>Count: %{customdata}<br>Percentage: %{percent}<extra></extra>',
            customdata=[at_risk_count, safe_count]
        )])
        
        # Add percentage text in the center
        fig_donut.add_annotation(
            text=f"{total_churn_percent*100}%",
            x=0.5, y=0.5,
            font_size=35,
            font_color="black",
            showarrow=False
        )
        
        fig_donut.update_layout(
            showlegend=True,
            height=300,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='black', size=12),
            legend=dict(font=dict(color='black'))
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # VERTICAL BAR CHART (Right column)
    with col2:
        
        st.markdown('<h3 style="color: black;">Risk Category Distribution</h3>', unsafe_allow_html=True)
        
        # Create vertical bar chart
        import pandas as pd
        df_category = pd.DataFrame(category_data)
        fig_bar = px.bar(
            df_category,
            x='Category',
            y='Percentage',
            labels={'Category': 'Risk Category', 'Percentage': 'Percentage (%)'},
            color='Category',
            color_discrete_sequence=['#51cf66', '#ffd43b', '#ff8787', '#ff6b6b']
        )
        
        fig_bar.update_layout(
            height=300,
            yaxis=dict(range=[0, 100]),
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='black'),
            margin=dict(t=20, b=40, l=40, r=20)
        )
        
        fig_bar.update_xaxes(showgrid=False, color='black')
        fig_bar.update_yaxes(showgrid=True, gridcolor='lightgray', color='black')
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # USER TABLE (Bottom section) - fit remaining height
    st.markdown('<h3 style="color: black; margin-top: 1rem;">Users at Risk</h3>', unsafe_allow_html=True)
    
    # Convert mock data to DataFrame
    df_users = pd.DataFrame(bottom_table_data)
    
    # Display table with remaining height
    st.dataframe(
        df_users,
        height=280,  # Fixed height to fit in remaining space
        use_container_width=True
    )