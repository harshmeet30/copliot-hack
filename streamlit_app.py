import os
import streamlit as st
from dotenv import load_dotenv
from counter_narrative import CounterNarrativeGenerator
from moderator import Category, MediaType
from moderator import ContentSafety
from languageservice import LanguageService
from data_storage_tbl import DataStorage
from streamlit_option_menu import option_menu
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load environment variables from .env file
load_dotenv()
st.set_page_config(layout="wide")

# Initialize the CounterNarrativeGenerator
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
generator = CounterNarrativeGenerator(endpoint, deployment, subscription_key)

# Initialize the ContentModerator
moderator_endpoint = os.getenv("MODERATOR_ENDPOINT")
moderator_subscription_key = os.getenv("MODERATOR_API_KEY")
moderator_api_version = "2024-09-01"
moderator_ = ContentSafety(moderator_endpoint, moderator_subscription_key, moderator_api_version)

# Initialize the LanguageService
language_service_endpoint = os.getenv("LANGUAGE_SERVICE_ENDPOINT")
language_service_key = os.getenv("LANGUAGE_SERVICE_KEY")
language_service = LanguageService(language_service_endpoint, language_service_key)

# Initialize DataStorage
connection_string = os.getenv("TABLE_STORAGE_CONN_STRING")

# Sidebar navigation with emojis and tab-style selection
with st.sidebar:
    selected_page = option_menu(
        menu_title="Navigation",
        options=["Textual Post", "Image Post", "Dashboard"],
        icons=["file-text", "image", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "blue", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#e0e0e0",
            },
            "nav-link-selected": {"background-color": "#ffcc00"},
        },
    )



if selected_page == "Textual Post":
    st.title("Textual Post Analysis")
    #st.header("Generate Counter-Narrative and Analyze Text")
    input_text = st.text_area("### Enter text to generate a counter-narrative and analyze sentiment:")

    if st.button("Generate Counter-Narrative and Analyze Text"):
        if input_text:
            # Generate counter-narrative
            counter_narrative = generator.generate_counter_narrative(input_text)
            st.subheader("Counter-Narrative:")
            st.write(counter_narrative)

            # Analyze text
            analysis_result = language_service.analyze_text(input_text)
            st.subheader("Text Analysis Result:")

            # Add sentiment and severity with emojis
            sentiment = analysis_result.get("sentiment", "neutral")
            severity = analysis_result.get("severity", "low")

            sentiment_emoji = {
                "positive": "😊",
                "neutral": "😐",
                "negative": "😔"
            }.get(sentiment, "❓")

            severity_emoji = {
                "low": "🟢",
                "medium": "🟠",
                "high": "🔴"
            }.get(severity, "❓")

            st.markdown(f"**Sentiment:** {sentiment.capitalize()} {sentiment_emoji}")
            st.markdown(f"**Severity:** {severity.capitalize()} {severity_emoji}")

            # Highlight key phrases in the original text
            key_phrases = analysis_result.get("key_phrases", [])
            if key_phrases:
                highlighted_text = input_text
                for phrase in key_phrases:
                    highlighted_text = highlighted_text.replace(
                        phrase, f"<span style='background-color: lightgreen;'>{phrase}</span>"
                    )

                st.markdown("### Highlighted Input Text:")
                st.markdown(highlighted_text, unsafe_allow_html=True)
            else:
                st.write("No key phrases identified.")

            # Display sentiment scores in a sidebar chart
            scores = analysis_result.get("scores", {})
            if scores:
                st.markdown("### Sentiment Scores")
                st.bar_chart(scores)
            else:
                st.write("No sentiment scores available.")

            # Create dictionary for table storage
            key_phrases_str = "; ".join(key_phrases)
            my_dict = {
                "Text": input_text,
                "sentiment": sentiment.capitalize(),
                "severity": severity.capitalize(),
                "key_phrases": key_phrases_str,
                "positive_score": scores.get("positive", 0),
                "neutral_score": scores.get("neutral", 0),
                "negative_score": scores.get("negative", 0),
                "C_Narrative": counter_narrative,
            }

            table_name = "MyNewTable"  # Update table name as needed
            storage = DataStorage(connection_string, table_name)
            storage.upload_session_data(my_dict)
            st.success("Data uploaded successfully!")

        else:
            st.write("Please enter some text.")

        



# Streamlit page code for "Image Post"
elif selected_page == "Image Post":
    severity_emojis = {
    0: "✅",  # Acceptable
    1: "⚠️",  # Warning
    2: "⚠️",  # Warning
    3: "⚠️",  # Warning
    4: "🚫",  # Rejected
    5: "🚫",  # Rejected
    6: "🚫",  # Rejected
}
    st.title("Image Post")
    st.header("Content Moderation")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_path = f"temp_{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        with open(image_path, "rb") as image_file:
            base64_encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        content = base64_encoded_image

        # Detect content safety
        media_type = MediaType.Image
        blocklists = []
        detection_result = moderator_.detect(media_type, content, blocklists)

        # Set reject thresholds for each category
        reject_thresholds = {
            Category.Hate: 4,
            Category.SelfHarm: 4,
            Category.Sexual: 4,
            Category.Violence: 4,
        }

        # Make a decision based on detection result and thresholds
        decision_result = moderator_.make_decision(detection_result, reject_thresholds)

        # Display the content moderation results
        st.write("### Content Moderation Result:")
        
            
        # Display category results with severity levels and emojis
        st.write("#### Categories and Severity Levels:")
        for category, action in decision_result.action_by_category.items():
            severity = detection_result['categoriesAnalysis'][category.value-1]['severity']
            severity_emoji = severity_emojis.get(severity, "⚪")  # Default to a neutral emoji if not found
            action_emojis = {
            action.Accept: "🟢",  # Green Circle for Accept
            action.Reject: "🔴",  # Red Circle for Reject
            }
            action_emoji = action_emojis.get(action, "⚪")  # Default to neutral emoji if not found
            
            st.write(f"- **{category.name}**: Severity = {severity_emoji} {severity}, Action = {action_emoji} {action.name}")

        # Display the final suggested action with emoji
        st.write("#### Final Suggested Action:")
        final_action = decision_result.suggested_action
        final_action_emoji = action_emojis.get(final_action, "⚪")
        st.write(f"**{final_action_emoji} {final_action.name}**")

        # Optionally, add further details or customized messages based on the action
        if final_action == action.Reject:
            st.warning("The content has been flagged for moderation and rejected.")
        else:
            st.success("The content is safe to post.")

# Display the detailed results from the table
elif selected_page == "Dashboard":
    st.title("Dashboard")
    table_name = "MyNewTable"
    storage = DataStorage(connection_string, table_name)

    # Retrieve all session data
    session_data = storage.download_all_sessions_data()

    if session_data:
        # st.write("### All Session Data:")
        # st.write(session_data)

        # Convert to DataFrame for easier manipulation
        import pandas as pd
        df = pd.DataFrame(session_data)

        # Create graphs in rows of two
        # st.markdown("##")

        # Row 1: Sentiment Count and Severity Count
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Distribution (Pie Chart)")
            sentiment_counts = df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']  # Rename columns for clarity
            sentiment_pie_chart = px.pie(
                sentiment_counts,
                names='Sentiment', values='Count',
                title="Sentiment Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(sentiment_pie_chart, use_container_width=True)

        with col2:
            st.subheader("Severity Count")
            severity_counts = df['severity'].value_counts().reset_index()
            severity_counts.columns = ['Severity', 'Count']  # Rename columns for clarity
            severity_count_chart = px.bar(
                severity_counts,
                x='Severity', y='Count',
                labels={'Severity': 'Severity', 'Count': 'Count'},
                title="Severity Distribution",
                color='Severity'
            )
            st.plotly_chart(severity_count_chart, use_container_width=True)

        # Row 2: Sentiment Scores and Key Phrase Word Cloud
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Sentiment Scores (Average)")
            avg_scores = df[['positive_score', 'neutral_score', 'negative_score']].mean().reset_index()
            avg_scores.columns = ['Score Type', 'Average Score']
            avg_scores_chart = px.bar(
                avg_scores,
                x='Score Type', y='Average Score',
                labels={'Score Type': 'Score Type', 'Average Score': 'Average Score'},
                title="Average Sentiment Scores",
                color='Score Type'
            )
            st.plotly_chart(avg_scores_chart, use_container_width=True)

        with col4:
            st.subheader("Key Phrase Word Cloud")
            all_phrases = ' '.join(df['key_phrases'].dropna())
            wordcloud = WordCloud(background_color='white').generate(all_phrases)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

        # Row 3: Sentiment vs Severity
        col5, col6 = st.columns(2)

        with col5:
            st.subheader("Sentiment vs Severity")
            sentiment_severity_chart = px.scatter(
                df, x='sentiment', y='severity',
                size='negative_score', color='sentiment',
                title="Sentiment vs Severity",
                labels={'sentiment': 'Sentiment', 'severity': 'Severity'}
            )
            st.plotly_chart(sentiment_severity_chart, use_container_width=True)

        with col6:
            st.subheader("Session Overview")
            session_chart = px.line(
                df, x=df.index, y='positive_score',
                title="Positive Score Over Sessions",
                labels={'x': 'Session', 'positive_score': 'Positive Score'}
            )
            st.plotly_chart(session_chart, use_container_width=True)

    else:
        st.info("No session data available.")
