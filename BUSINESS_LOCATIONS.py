import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import plotly.graph_objs as go
import plotly.express as px
from folium.plugins import MarkerCluster, HeatMap
from folium import plugins
from folium.plugins import MarkerCluster
from streamlit_extras.metric_cards import style_metric_cards

def bussiness_loc():
    # Set page configuration

    # Load Style CSS
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar style customization
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] {
                color: white;
                font-size: 24px;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Load data
    load_df = pd.read_excel('coordinates.xlsx')

    name = st.sidebar.multiselect(
        "SELECT OFFICE",
        options=load_df["Name"].unique(),
        default=load_df["Name"].unique(),
    )
    
    # Filter the dataframe based on selected office
    df = load_df.query("Name == @name")

    # Load dataset
    try:
        st.header("BUSINESS TRENDS BY GEO-REFERENCING")
        items = load_df['Name'].count()
        total_price = float(load_df['TotalPrice'].sum())

        with st.expander("ANALYTICS"):
            a1, a2 = st.columns(2)
            a1.metric(label="Office Branches", value=items, help=f"Total Price: {total_price}", delta=total_price)
            a2.metric(label="Total Price", value=total_price, help=f"Total Price: {total_price}", delta=total_price)
            style_metric_cards(background_color="#FFFFFF", border_left_color="#00462F", border_color="#070505", box_shadow="#F71938")

        # Create a map
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

        marker_cluster = MarkerCluster().add_to(m)
        for i, row in df.iterrows():
            popup_content = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <ul class="list-group">
            <h3>Information of {row['Name']}</h3>
            <hr class'bg-danger text-primary'>
            <div style='width:400px;height:200px;margin:10px;color:gray;text-size:18px;'>
            <li class="list-group-item"><b>Branch Manager:</b> {row['Manager']}</li>
            <li class="list-group-item"><b>Collection:</b> {row['Collection']} USD<br></li>
            <li class="list-group-item"><b>Name:</b> {row['Name']}<br></li>
            <li class="list-group-item"><b>Quantity:</b> {row['Quantity']}<br></li>
            <li class="list-group-item"><b>Unit Price:</b> {row['UnitPrice']}<br></li>
            <li class="list-group-item"><h4>Total Price: {row['TotalPrice']} USD</b><br></li>
            <li class="list-group-item"><h4>Phone {row['Phone']}</h4></li>
            """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=row['Name'],
                icon=folium.Icon(color='red', icon='fa-dollar-sign', prefix='fa'),
            ).add_to(marker_cluster).add_child(folium.Popup(popup_content, max_width=600))  

        # Heatmap Layer
        heat_data = [[row['Latitude'], row['Longitude']] for i, row in df.iterrows()]
        HeatMap(heat_data).add_to(m)

        # Fullscreen Control
        plugins.Fullscreen(position='topright', title='Fullscreen', title_cancel='Exit Fullscreen').add_to(m)

        # Drawing Tools
        draw = plugins.Draw(export=True)
        draw.add_to(m)

        def add_google_maps(m):
            tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
            attr = "Google Digital Satellite"
            folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)
            label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
            label_attr = "Google Labels"
            folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)
            return m

        with st.expander("OFFICE MAP VIEW & ANALYTICS"):
            m = add_google_maps(m)
            m.add_child(folium.LayerControl(collapsed=False))
            folium_static(m, width=1350, height=600)
            folium.LayerControl().add_to(m)

        # Show table data
        with st.expander("SELECT DATA"):
            selected_city = st.selectbox("Select a city", df['Name'])
            selected_row = df[df['Name'] == selected_city].squeeze()
            st.table(selected_row)

        # Graphs
        col1, col2 = st.columns(2)
        with col1:
            fig2 = go.Figure(
                data=[go.Bar(x=df['Name'], y=df['TotalPrice'])],
                layout=go.Layout(
                    title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
                    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper
                    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                    font=dict(color='#cecdcd'),
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            fig = px.pie(df, values='TotalPrice', names='Name', title='TotalPrice by Name')
            fig.update_traces(hole=0.4)  # Donut chart
            fig.update_layout(width=800)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Unable to display data: {e}")

if __name__ == "__main__":
    bussiness_loc()