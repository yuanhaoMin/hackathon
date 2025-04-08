import streamlit as st

from backend import Language, generate_reply, get_platforms, get_social_media_posts, translate_reply

# Use Streamlit's session_state to keep track of replies for each post
if "replies" not in st.session_state:
    # Key is the index of the post (as string), value is a list of reply records, each reply is a dict {reply, language}
    st.session_state.replies = {}

# Page title
st.title("Social Media Interaction and Replies")
st.write(
    "Displays posts from different social platforms, and allows direct replies under each post (supports multiple languages)."
)
posts = get_social_media_posts()
platforms = get_platforms()

selected_platforms = st.multiselect("Platforms:", options=[platform["name"] for platform in platforms], default=[platform["name"] for platform in platforms])

for idx, post in enumerate(posts):
    
    if post["platform"] not in selected_platforms:
        continue

    with st.expander(f"[{post['platform']}] {post['sender']} posted at {post['time']}"):
        st.write("***Message Content***")
        with st.container(border=True):
          st.write(f"{post['message']}")

        st. write("***Original Language***")
        with st.container(border=True):
          st.write(f"{post['language']}")

        if str(idx) in st.session_state.replies:
            st.markdown("**Reply History:**")
            for reply in st.session_state.replies[str(idx)]:
                st.write(f"- ({reply['language']}) {reply['reply']}")
        else:
            st.write("No replies yet.")

        st.markdown("----")
        # Custimize reply
        st.markdown("### Add Custom Reply")
        custom_reply_key = f"custom_reply_input_{idx}"
        custom_display_key = f"custom_reply_display_{idx}"
        custom_lang_key = f"custom_lang_{idx}"

        custom_reply = st.text_area(
            "Your Reply:",
            value=st.session_state.get(custom_reply_key, ""),
            key=custom_reply_key,
        )
        selected_lang = st.selectbox(
            "Select Reply Language:",
            [Language.ENGLISH.value, Language.GERMAN.value, Language.SPANISH.value],
            key=custom_lang_key,
        )

        # Translate and generate
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Translate", key=f"translate_btn_{idx}"):
                result = translate_reply(text=custom_reply, language=selected_lang)
                st.session_state[custom_display_key] = result
                st.rerun()
        with col2:
            if st.button("Generate", key=f"generate_btn_{idx}"):
                result = generate_reply(text=custom_reply, language=selected_lang, original=post["message"])
                st.session_state[custom_display_key] = result
                st.rerun()

        # Display translated or generated content
        if custom_display_key in st.session_state:
            st.markdown("**Translated / Generated Result:**")
            st.write(st.session_state[custom_display_key])

        # Send button logic
        if st.button("Send Custom Reply", key=f"send_custom_{idx}"):
            reply_text = custom_reply.strip()
            if reply_text:
                new_reply = {"reply": reply_text, "language": selected_lang}
                st.session_state.replies.setdefault(str(idx), []).append(new_reply)
                st.success("Custom reply added!")
                st.rerun()
            else:
                st.warning("Please enter reply content before sending.")
# test
