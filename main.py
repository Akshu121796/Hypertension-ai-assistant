import streamlit as st
import json
import time
import requests 

# --- 1. CONFIGURATION AND CONSTANTS ---

# IMPORTANT: API_KEY is set to an empty string to allow automatic injection 
 # in secure execution environments (like Gemini Canvas). 
# If running locally, st.secrets is used as a fallback if available.
API_KEY = "" 
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"

# Fallback mechanism for API Key (useful for local development where secrets are used)
# This uses .get() to avoid raising an error if st.secrets is empty or the key is missing.
if not API_KEY and hasattr(st, 'secrets'):
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")


meta = {
    "initial_greeting": "👋 Hi! I'm your **Hypertension Assistant**. I use advanced AI to answer your questions about high blood pressure. Ask away!",
    "greeting": "Hello there! How can I help you manage your hypertension today?",
    "api_fail": "⚠️ I'm sorry, I cannot connect to the AI service right now. Please try again later. This application requires a successful connection to the Gemini API.",
    "placeholder_fail": "I'm sorry, the AI could not generate a clear answer to that query. Please rephrase your question or try a suggestion below."
}

suggestions = [
    "What is the optimal diet for reducing blood pressure?",
    "What are the long-term effects of untreated hypertension?",
    "Can stress significantly raise my blood pressure reading?",
    "Explain the difference between systolic and diastolic pressure."
]


# --- 2. GEMINI API COMMUNICATION ---

def get_gemini_response(query):
    """
    Generates a response using the Gemini API with Google Search grounding.
    Uses exponential backoff for retries.
    """
    # Check if API Key is available
    if not API_KEY:
        st.error("API Key is missing. Please ensure it is set up correctly in your environment (Canvas or local secrets).")
        return meta['api_fail']
        
    # Construct API URL dynamically using the constant MODEL_NAME and API_KEY
    API_ENDPOINT_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    api_url = API_ENDPOINT_TEMPLATE.format(model=MODEL_NAME, key=API_KEY)
    
    # Define the persona and constraints for the LLM
    system_prompt = (
        "You are a helpful, professional, and medically aware assistant specializing in hypertension "
        "and blood pressure management. Provide a concise, easy-to-understand answer based on the information "
        "you find. When discussing medical topics, explicitly advise the user to consult a doctor for diagnosis or treatment."
    )

    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "tools": [{"google_search": {} }], # Enable Google Search for grounding
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    headers = {'Content-Type': 'application/json'}
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=20)
            response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            
            if candidate and candidate.get('content') and candidate['content']['parts']:
                text = candidate['content']['parts'][0].get('text', meta['placeholder_fail'])
                
                # Extract grounding sources
                sources = []
                grounding_metadata = candidate.get('groundingMetadata')
                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = grounding_metadata['groundingAttributions']
                
                citations = ""
                if sources:
                    citations = "\n\n---\n**Sources:**\n"
                    unique_uris = set()
                    
                    for source in sources:
                        uri = source.get('web', {}).get('uri')
                        title = source.get('web', {}).get('title', 'Link')
                        
                        if uri and uri not in unique_uris:
                            citations += f"- [{title}]({uri})\n"
                            unique_uris.add(uri)
                            if len(unique_uris) >= 3:
                                break
                                
                return text + citations

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            # Use exponential backoff
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                # If all retries fail, return the API fail message
                st.error(f"Failed to connect to Gemini API after {max_retries} attempts.")
                return meta['api_fail']
            
    return meta['placeholder_fail']


# --- 3. STREAMLIT UI AND CHAT LOGIC ---

def app():
    """Renders the Streamlit application."""
    st.set_page_config(page_title="Hypertension Assistant 💬", page_icon="💉", layout="centered")

    # Inject external CSS from gui_style.css
    try:
        # Load the content of the CSS file
        with open("gui_style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Could not load 'gui_style.css'. Displaying unstyled content. Make sure 'gui_style.css' is present.")

    # Header
    st.markdown("<h1 style='text-align:center;'>💬 Hypertension Assistant Bot</h1>", unsafe_allow_html=True)
    st.write("I'm here to help you learn and manage your blood pressure effectively. **All information is AI-generated and grounded in search results. Always consult your doctor.** 🩺")
    st.divider()

    # Session chat history initialization
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "bot", "text": meta["initial_greeting"]}]

    # Chat display (Scrollable)
    chat_container = st.container(height=400)
    with chat_container:
        for chat in st.session_state.messages:
            if chat["role"] == "user":
                st.markdown(f"<div class='user-bubble'>🧑‍💬 {chat['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'>🤖 {chat['text']}</div>", unsafe_allow_html=True)

    # Function to process chat logic and update messages
    def process_query(user_query):
        if not user_query:
            return
        
        # 1. Append user message
        st.session_state.messages.append({"role": "user", "text": user_query})
        
        # 2. Get AI response using spinner
        with st.spinner("Searching and synthesizing an answer via Gemini..."):
            response = get_gemini_response(user_query)
        
        # 3. Append bot response
        st.session_state.messages.append({"role": "bot", "text": response})

    # --- Input field and Send button ---
    
    # Use clear_on_submit=True to natively clear the text input.
    with st.form(key='chat_form', clear_on_submit=True): 
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("Type your question...", key="user_input_text", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Send")
    
    # Process form submission outside the form block
    if submitted:
        process_query(st.session_state.user_input_text)
        st.rerun() 

    # --- Suggestion buttons ---
    st.write("### 💡 Try asking:")
    
    cols = st.columns(3) 
    
    for i, sug in enumerate(suggestions):
        if cols[i % 3].button(sug, key=f"sug_btn_{i}"):
            process_query(sug)
            st.rerun()

            
if __name__ == "__main__":
    app()
