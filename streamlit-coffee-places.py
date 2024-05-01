import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import urllib.parse

data = pd.read_csv('database.csv', delimiter=';')

df = pd.DataFrame(data)

# Streamlit app setup
st.set_page_config(layout="wide")
col11, mid, col22 = st.columns([1,1,40])
with col11:
    st.image('logo.png', width=80)
with col22:
    st.title("PražskáKavárna.cz")

st.write('Ať už jste studenti, pracanti nebo milovníci kávy, jste tu na správném místě. PražskáKavárna.cz je váš odrazový můstek, kde si vyberete vaši kancelář mimo domov. Řídím se heslem: Venku to roste. A také káva tvoří den. Pokud to vidíte stejně, prozkoumejte nové místo, ať víte do čeho jdete. Vyzkoušeno za vás:).')
st.write("Autor blogu se vyhraňuje nálepce „pražská kavárna”, nevidí na tom nic špatného.")
st.write("Vyberte si lokalitu z postranního panelu a z nabídky vyberte kavárnu, která vás zaujme.")
st.markdown('#')

col1, col2 = st.columns((1, 1.5))

# Filters in sidebar
locality = st.sidebar.multiselect("1/ Vyberte lokalitu", options=df["locality"].unique(), default=df["locality"].unique())
#rating = st.sidebar.slider("Hodnocení", 1, 3, (1, 3))
#budget = st.sidebar.slider("Budget", 1, 3, (1, 3))

# Filter data based on user selections
filtered_data = df[
    (df["locality"].isin(locality)) #& 
    #(df["rating"] >= rating[0]) & 
    #(df["rating"] <= rating[1]) & 
    #(df["budget"] >= budget[0]) & 
    #(df["budget"] <= budget[1])
]

# Function to generate Google Maps iframe for a given location with a marker and name
def create_map(name):
    # URL encode the name for use in a query parameter
    name_encoded = urllib.parse.quote(name)
    return f"""
    <iframe width="700" height="800" style="border:0" loading="lazy" allowfullscreen
    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyAcd9MxsEkda0ApfQGwl0WPXMKaunX_lE0&q={name_encoded}&zoom=17">
    </iframe>
    """

with col1:
    # Display selectable list of coffee shops
    selected_cafe = st.selectbox("2/ Prozkoumejte kavárnu:", filtered_data['name'].unique())

    # Display information for the selected coffee shop
    if selected_cafe:
        cafe_info = filtered_data[filtered_data['name'] == selected_cafe].iloc[0]
        st.write(f"## {cafe_info['name']}")
        st.write(f"📍 {cafe_info['locality']},",f"{cafe_info['address']}","|", f"{'⭐' * cafe_info['rating']} hvězdiček","|", f"{'💵' * cafe_info['budget']} cena")
        components.html(
            """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        * {box-sizing: border-box;}
        body {font-family: Verdana, sans-serif;}
        .mySlides {display: none;}
        img {vertical-align: middle;}

        /* Slideshow container */
        .slideshow-container {
          max-width: 1000px;
          position: relative;
          margin: auto;
        }

        /* Caption text */
        .text {
          color: #f2f2f2;
          font-size: 15px;
          padding: 8px 12px;
          position: absolute;
          bottom: 8px;
          width: 100%;
          text-align: center;
        }

        /* Number text (1/3 etc) */
        .numbertext {
          color: #f2f2f2;
          font-size: 12px;
          padding: 8px 12px;
          position: absolute;
          top: 0;
        }

        /* The dots/bullets/indicators */
        .dot {
          height: 15px;
          width: 15px;
          margin: 0 2px;
          background-color: #bbb;
          border-radius: 50%;
          display: inline-block;
          transition: background-color 0.6s ease;
        }

        .active {
          background-color: #717171;
        }

        /* Fading animation */
        .fade {
          animation-name: fade;
          animation-duration: 1.5s;
        }

        @keyframes fade {
          from {opacity: .4} 
          to {opacity: 1}
        }

        /* On smaller screens, decrease text size */
        @media only screen and (max-width: 300px) {
          .text {font-size: 11px}
        }
        </style>
        </head>
        <body>

        <div class="slideshow-container">

        <div class="mySlides fade">
          <div class="numbertext"></div>
          <img src="https://fastly.4sqi.net/img/general/600x600/76845684_N-4cBJXNIXL5LTwF5HWFylubjY6pp5_xHT2qnWP6GQk.jpg?force=true&w=100" style="width:100%">
          <div class="text"></div>
        </div>

        <div class="mySlides fade">
          <div class="numbertext"></div>
          <img src="https://pekarnakrusta.cz/wp-content/uploads/2022/10/img_3921_optimized.jpg?force=true&w=100" style="width:100%">
          <div class="text"></div>
        </div>

        <div class="mySlides fade">
          <div class="numbertext"></div>
          <img src="https://apetee.com/img/10000/5000/700/15730/1440x960_15730_0.jpg?force=true&w=100" style="width:100%">
          <div class="text"></div>
        </div>

        </div>
        <br>

        <div style="text-align:center">
          <span class="dot"></span> 
          <span class="dot"></span> 
          <span class="dot"></span> 
        </div>

        <script>
        let slideIndex = 0;
        showSlides();

        function showSlides() {
          let i;
          let slides = document.getElementsByClassName("mySlides");
          let dots = document.getElementsByClassName("dot");
          for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";  
          }
          slideIndex++;
          if (slideIndex > slides.length) {slideIndex = 1}    
          for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
          }
          slides[slideIndex-1].style.display = "block";  
          dots[slideIndex-1].className += " active";
          setTimeout(showSlides, 8000); // Change image every 2 seconds
        }
        </script>

        </body>
        </html> 

            """,
            height=430,
        )
        st.write(f"Recenze: {cafe_info['review']}")
        #st.write(f"[Více informací na webu]({cafe_info['url']})")
        st.link_button("Více informací na webu ->", f"{cafe_info['url']}")

with col2:
    # If a coffee shop is selected, display it on the map with a marker and name
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    if selected_cafe:
        cafe_info = filtered_data[filtered_data['name'] == selected_cafe].iloc[0]
        st.markdown(create_map(cafe_info['name']), unsafe_allow_html=True)



#    "latitude": [
#        50.0755, 50.0878, 50.1010, 50.0755, 50.0878, 50.1010, 50.0755, 50.0878, 50.1010, 50.1010
#        ],
#    "longitude": [
#        14.4378, 14.4205, 14.3995, 14.4378, 14.4205, 14.3995, 14.4378, 14.4205, 14.3995, 14.3995
#        ],
