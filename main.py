import streamlit as st
import pandas as pd
from Gplaces import Gplaces



#with open('./key', 'r') as file:
#    API_KEY = file.read()

API_KEY = st.secrets["API_KEY"]

def main():
    st.title("Business Competition Assessment")
    st.write("By Joab Cuevas, Dexter Gómez, Isaí Massa")

    # Get user inputs
    name = st.text_input("Enter place name:")
    lat = st.text_input("Latitude (optional):", "")
    lng = st.text_input("Longitude (optional):", "")
    radius = st.slider("Search Radius (in meters)", 500, 10000, 3000)

    # Initialize class
    business = Gplaces(API_KEY)

    if st.button("Search"):
        if lat and lng:
            place = business.get_place(name, float(lat), float(lng))
        else:
            place = business.get_place(name)
        
        if place:

            # Fetch detailed information about the place
            detailed_info = business.get_detailed_info(place['place_id'])
            if detailed_info:
                st.write(f"## {detailed_info['name']}")
                st.write(f"Type of Place: {', '.join(detailed_info['types'])}")
                st.write(f"Rating: {place['rating']}")
                st.write(f"## {detailed_info.get('user_ratings_total', 'N/A')} Reviews for {detailed_info['name']}")
                
                # Fetch and display the top 10 reviews
                reviews = detailed_info.get('reviews', [])[:10]
                for review in reviews:
                    st.write(f"Review by {review['author_name']} (Rating: {review['rating']}):")
                    st.write(review['text'])
                    st.write("---")

            similar_places = business.get_similar_places(radius=radius)
            if similar_places:
                st.write(f"## Found {len(similar_places)} similar places nearby")
                

                # Sort similar places by rating and display top businesses in a table
                sorted_places = sorted(similar_places, key=lambda x: x.get('rating', 0), reverse=True)
                
                top_business_df = pd.DataFrame({
                    'Name': [p['name'] for p in sorted_places],
                    'Rating': [p.get('rating', 'N/A') for p in sorted_places],
                    'Address': [p.get('vicinity', 'N/A') for p in sorted_places]
                })

                st.write("Top Similar Businesses and Their Ratings:")
                st.table(top_business_df)


                # Convert places to dataframe for displaying on map
                df = pd.DataFrame({
                    'lat': [p['geometry']['location']['lat'] for p in similar_places],
                    'lon': [p['geometry']['location']['lng'] for p in similar_places],
                    'name': [p['name'] for p in similar_places]
                })

                # Add the target place to the dataframe
                df_target = pd.DataFrame({
                    'lat': [business.lat],
                    'lon': [business.lng],
                    'name': [business.b_name]
                })

                df = pd.concat([df, df_target])

                # Display on map
                st.map(df, size=20)

                    
            else:
                st.write("No similar places found nearby")
        else:
            st.write("Place not found")

if __name__ == "__main__":
    main()