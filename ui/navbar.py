import streamlit as st

def navbar() -> None:
    """
    A navbar function that renders a Streamlit navbar element.
    The navbar has text 'LiveStreaming' on the left side.
    The navbar will be at the top, take 20% of the screen height, and have full screen width.
    """
    st.markdown(
        """
        <style>
            .navbar {
                background-color: #262730;
                padding: 0.5rem 1rem;
                height: 15vh; /* 20% of viewport height */
                width: 100vw; /* 100% of viewport width */
                position: fixed; /* Fix to top */
                top: 0;
                left: 0;
                z-index: 999; /* Ensure it's on top of other elements */
                display: flex; /* For aligning items */
                align-items: center; /* Vertically center content */
            }
            .navbar-brand {
                color: white;
                font-size: 1.5rem;
                font-weight: bold;
            }
        </style>
        <nav class="navbar">
            <span class="navbar-brand">LiveStreaming</span>
        </nav>
        <div style="height: 15vh;"></div> <!-- Placeholder to push content below fixed navbar -->
        """,
        unsafe_allow_html=True
    )