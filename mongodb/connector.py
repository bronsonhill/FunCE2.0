import pymongo
import streamlit as st

def get_mongo_client():
    """
    Establish a connection to MongoDB using credentials from Streamlit secrets.
    
    Returns:
        pymongo.MongoClient: A MongoDB client instance.
    """
    # Get connection details from secrets
    username = st.secrets["MONGODB_USERNAME"]
    password = st.secrets["MONGODB_PASSWORD"]
    connection_string = st.secrets["MONGODB_CONNECTION_STRING"].replace("<db_password>", password)
    
    # Connect to MongoDB
    client = pymongo.MongoClient(connection_string)
    
    # Validate connection
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    
    return client

def get_question_details(module_num, question_num):
    """
    Retrieve details for a specific question from MongoDB.
    
    Args:
        module_num (int or str): The module number.
        question_num (int or str): The question number within the module.
        
    Returns:
        dict: A dictionary containing question details.
    """
    # Convert to integers in case they're strings
    module_num = int(module_num)
    question_num = int(question_num)
    
    # Connect to MongoDB
    client = get_mongo_client()
    db = client["FunCE"]
    questions_collection = db["questions"]
    
    # Query the database
    question_data = questions_collection.find_one({
        "module": module_num, 
        "question_number": question_num
    })
    
    # If question not found, return placeholder data
    if not question_data:
        return {
            "title": f"Module {module_num} - Question {question_num}",
            "description": "This question hasn't been added to the database yet.",
            "hints": ["No hints available for this question yet."],
            "module": module_num,
            "question_number": question_num
        }
    
    # Return the question data
    return question_data

def get_module_topics(module_num):
    """
    Retrieve all topics for a specific module from MongoDB.
    
    Args:
        module_num (int or str): The module number.
        
    Returns:
        list: A list of dictionaries containing topic information.
    """
    # Convert to integer in case it's a string
    module_num = int(module_num)
    
    # Connect to MongoDB
    client = get_mongo_client()
    db = client["FunCE"]
    questions_collection = db["questions"]
    
    # Query the database for all questions in the module
    topics = list(questions_collection.find({"module": module_num}, {"title": 1, "description": 1, "question_number": 1, "status": 1}))
    
    # Sort by question number
    topics.sort(key=lambda x: x.get("question_number", 0))
    
    return topics

def get_all_modules():
    """
    Retrieve all modules with their questions from MongoDB.
    
    Returns:
        dict: A dictionary where keys are module titles and values are 
              dictionaries of topics and their status.
    """
    # Connect to MongoDB
    client = get_mongo_client()
    db = client["FunCE"]
    modules_collection = db["modules"]
    questions_collection = db["questions"]
    
    # Get all modules
    modules = list(modules_collection.find({}, {"module_number": 1, "title": 1}))
    
    # Initialize the result dictionary
    result = {}
    
    # For each module, get its topics
    for module in modules:
        module_num = module.get("module_number")
        module_title = module.get("title")
        
        # Get all questions for this module
        questions = list(questions_collection.find({"module": module_num}, {"title": 1, "status": 1}))
        
        # Add to result with default status of "🔴" if not specified
        module_topics = {}
        for question in questions:
            module_topics[question.get("title")] = question.get("status", "🔴")
        
        result[module_title] = module_topics
    
    # If no modules were found, return placeholder data
    if not result:
        return {
            "Introduction": {
                "Introduction to Chemical Engineering Fundamentals": '✅',
                "Principles of Material Balances": '✅',
                "Thermodynamics in Chemical Processes": '🟠',
                "Fluid Flow Operations": '🟠',
                "Process Safety & Ethics": '🔴',
            },
            # ... other placeholder modules ...
        }
    
    return result