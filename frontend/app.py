import streamlit as st
import requests

st.set_page_config(
   layout = "wide"
)

st.title("Twitter")

username = st.text_input("username")
content = st.text_area("what is in your mind?")

if st.button("post"):
   if username and content:
      try:
        response = requests.post("http://127.0.0.1:8000/tweets", json = {"username" : username, "content" : content})
        if response.status_code == 200:
            st.success("Tweeted")
      except Exception as e:
         st.error(f"Error: {e}")
   else:
      st.warning("enter username and password")

try:
   response = requests.get("http://127.0.0.1:8000/tweets")
   if response.status_code == 200:
      tweets = response.json()

      for tweet in tweets:
         st.subheader(f"{tweet['username']} : {tweet['content']}")
         st.caption(f"{tweet['create_at']}")
except Exception as e:
   st.error(f"{e}")

