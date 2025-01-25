import streamlit as st

def bi():

    
    def set_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: cover;
                background-position: top;
                background-repeat:repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    set_background("https://t4.ftcdn.net/jpg/02/52/46/25/360_F_252462576_koy7njo9iYx6gUcM26IZcDUs9fMKIKJs.jpg")
    
    st.markdown("""
    <style>
            html{
                font-family: Manrope;
                }
         
             .ea3mdgi5{
                max-width:100%;
                margin: auto;
                }
            
    </style>
        """, unsafe_allow_html=True)
    power_bi_embed_url = "https://app.powerbi.com/view?r=eyJrIjoiODlkNzUxYzMtNDM3OS00NWRlLWE3YmQtNWE1NDFjN2QxN2ViIiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D"
    
    st.components.v1.iframe(
        src=power_bi_embed_url,
        width=800,
        height=475,
        scrolling=False
    )

if __name__ == "_main_":
    bi()