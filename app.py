"""
Financial Decision Support System (FDSS)
Interactive Streamlit Application

Research project for the Avishkar Research Convention.
Bridges applied mathematics, numerical methods, and stochastic simulation
for transparent retail and institutional financial decision-making.
"""

import streamlit as st

def main():
    st.set_page_config(
        page_title="Financial Decision Support System | FDSS",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Financial Decision Support System (FDSS)")
    st.caption("A Mathematical & Stochastic Framework for Rigorous Financial Decision Analysis")

    st.info(
        "Welcome to FDSS. The system is currently undergoing modular development. "
        "Explore the documentation and codebase to follow the mathematical foundations."
    )

if __name__ == "__main__":
    main()
