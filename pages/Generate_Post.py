import streamlit as st

from backend import Platform, generate_post, get_trending_topics

# Configure the page with a title, icon, and wide layout
st.set_page_config(page_title="Lively Post Generator 🎉", page_icon="🎉", layout="wide")
st.title("Generate Social Media Post")
# Import a modern font from Google Fonts
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# Custom CSS styles for a cleaner, modern UI
st.markdown(
    """
    <style>
        /* General body and container styling */
        body {
            background-color: #f9f9f9;
            font-family: 'Roboto', sans-serif;
        }
        .reportview-container .main .block-container {
            padding: 2rem;
        }
        .reportview-container .main .block-container h1,
        .reportview-container .main .block-container h2,
        .reportview-container .main .block-container h3 {
            font-weight: 500;
            color: #212121;
        }
        .reportview-container .main .block-container p,
        .reportview-container .main .block-container label,
        .reportview-container .main .block-container div {
            color: #424242;
            font-size: 16px;
        }
        
        /* topic (trending) button styling: light blue pill-style */
        .topic-button > button {
            background-color: #BBDEFB !important;  /* light blue */
            color: #0D47A1 !important;             /* dark blue text */
            border: none !important;
            border-radius: 18px !important;
            padding: 0.2rem 0.8rem !important;
            font-size: 14px !important;
            margin: 0.1rem !important;
        }
        .topic-button > button:hover {
            background-color: #90CAF9 !important;
        }
        
        /* Sidebar styling */
        .css-1aumxhk, .stSidebar {
            background-color: #ECEFF1 !important;
        }
        .css-1aumxhk .sidebar-content, .stSidebar .sidebar-content {
            color: #212121;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for selected topics if not already set
if "selected_topics" not in st.session_state:
    st.session_state.selected_topics = []


# Get platform options from the Platform enum
platform_options = [p.value for p in Platform]
st.markdown("### **📊 Select a platform to get trending topics**")
platform = st.selectbox("", platform_options)
trending_topics = get_trending_topics(platform)

st.markdown("**Click a topic to select:**")
cols = st.columns(len(trending_topics))
for i, topic in enumerate(trending_topics):
    with cols[i]:
        st.markdown('<div class="topic-button">', unsafe_allow_html=True)
        if st.button(topic, key=f"trending_kw_{i}"):
            if topic not in st.session_state.selected_topics:
                st.session_state.selected_topics.append(topic)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("**Or add a topic manually:**")
manual_topic = st.text_input("New topic", key="manual_topic_input")

if st.button("Add Topic", key="add_topic_button"):
    if manual_topic:
        if manual_topic not in st.session_state.selected_topics:
            st.session_state.selected_topics.append(manual_topic)
            st.rerun()

st.markdown("**Selected topics:**")
if st.session_state.selected_topics:
    for i, topic in enumerate(st.session_state.selected_topics):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(
                f"<span style='background-color: #E3F2FD; color: #0D47A1; padding: 0.3rem 0.8rem; border-radius: 16px; font-size: 14px;'>{topic}</span>",
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("X", key=f"remove_{topic}"):
                st.session_state.selected_topics.pop(i)
                st.rerun()
else:
    st.write("No topics selected yet.")

# Combine manual input and selected topics to form the topic
topics = []
if manual_topic:
    topics.append(manual_topic)
if st.session_state.selected_topics:
    topics.extend(st.session_state.selected_topics)

if st.button("Generate Post", key="generate_post_button"):
    if not topics:
        st.error("Please enter a topic or select/add at least one topic.")
    else:
        post = generate_post(topics, platform)
        st.success("Generated Post:")
        st.write(post)
