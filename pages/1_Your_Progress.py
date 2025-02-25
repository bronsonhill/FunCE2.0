import streamlit as st
from mongodb.connector import get_all_modules

BASE_URL = "http://localhost:8501/"

def overview():
    st.title("Your Learning Progress")
    
    # Get the progress data
    progress_data = retrieve_progress()
    
    # Get module titles dynamically from the progress data
    module_titles = list(progress_data.keys())
    
    # Display progress for each module
    for module_num, module_key in enumerate(module_titles, 1):
        if module_key in progress_data:
            module_data = progress_data[module_key]
            
            # Calculate completion percentage
            total_questions = len(module_data)
            completed_questions = sum(1 for status in module_data.values() if status == '✅')
            completion_percentage = (completed_questions / total_questions) * 100 if total_questions > 0 else 0
            
            # Create an expander for each module
            with st.expander(f"Module {module_num}: {module_key} - {completion_percentage:.0f}% Complete", expanded=module_num == 1):
                
                # Create columns for the progress display
                col1, col2 = st.columns([3, 1])
                
                # Display module link in the first column
                with col1:
                    module_url = f"{BASE_URL}Tutor?module={module_num}"
                    st.page_link(module_url, label=f"Go to Module {module_num}")
                
                # Display progress bar in the second column
                with col2:
                    st.progress(completion_percentage / 100)
                
                # Display individual question progress with links to chatbot
                st.markdown("#### Topic Progress")
                
                # Create a counter for question numbering
                question_counter = 1
                
                for topic, status in module_data.items():
                    status_color = {
                        '✅': 'green',
                        '🟠': 'orange',
                        '🔴': 'red'
                    }.get(status, 'gray')
                    
                    # Create columns for status and link
                    q_col1, q_col2 = st.columns([1, 3])
                    
                    with q_col1:
                        st.markdown(f"<span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)
                    
                    with q_col2:
                        # Create link to chatbot with query parameters
                        chatbot_url = f"{BASE_URL}Tutor?module={module_num}&question={question_counter}"
                        st.page_link(
                            chatbot_url, 
                            label=topic, 
                            help=f"Try {topic} (Module {module_num}, Topic {question_counter})"
                        )
                    
                    question_counter += 1

def retrieve_progress():
    """
    Retrieve the progress data from MongoDB for all modules and their questions.
    
    Returns:
        dict: A dictionary where keys are module titles and values are 
              dictionaries of topics and their status.
    """

    return {
        "Introduction": {
            "Introduction to Chemical Engineering Fundamentals": '✅',
            "Principles of Material Balances": '✅',
            "Thermodynamics in Chemical Processes": '🟠',
            "Fluid Flow Operations": '🟠',
            "Process Safety & Ethics": '🔴',
        },
        "Heat": {
            "Heat Transfer Operations": '🔴',
            "Mass Transfer Principles": '🔴',
            "Separation Processes": '🔴',
            "Distillation Column Design": '🔴',
        },
        "Kinetics": {
            "Reaction Kinetics Fundamentals": '🔴',
            "Reactor Design Principles": '🔴',
            "Catalysis in Chemical Processes": '🔴',
            "Biochemical Reactor Systems": '🔴',
        },
        "Title": {
            "Process Control & Instrumentation": '🔴',
            "PID Controller Design": '🔴',
            "Dynamic Process Modeling": '🔴',
            "Advanced Control Strategies": '🔴',
        },
        "Titlex": {
            "Plant Design & Economics": '🔴',
            "Equipment Sizing & Selection": '🔴',
            "Process Optimization": '🔴',
            "Sustainable Process Engineering": '🔴',
        },
        "Titlexx": {
            "Polymer Process Engineering": '🔴',
            "Pharmaceutical Manufacturing": '🔴',
            "Petroleum Refining Operations": '🔴',
            "Renewable Energy Processes": '🔴',
        },
    }

    # Use the MongoDB connector to get all modules and their questions
    # return get_all_modules()
    
if __name__ == "__main__":
    overview()