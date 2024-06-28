import streamlit as st
import pandas as pd
import redis
import os

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

special_dataframe = None


# Function to parse CSV file and set data in Redis
def init_vehicle_info(resources):
    for loc, vinfo in resources.items():
        for vtype, vcount in vinfo.items():
                key = f'{loc}_{vtype}'
                r.set(f"{key}", vcount)

# Function to retrieve data from Redis
def get_vehicle_info(data_key):
    #i.e. key = Merzig-Wadern_TSF/LF/TLF_0
    keys = r.keys(f"{data_key}")
    data = {key: r.get(key) for key in keys}
    print(data)

def get_meta_deta(resources):
    return_results = resources.copy()
    for loc, vinfo in resources.items():
        for vtype, vcount in vinfo.items():
            key = f'{loc}_{vtype}'
            return_results[loc][vtype]= r.get(f"{key}")
    print(return_results)

def update_resources(location, vtype, deployment_value):
    key = f'{location}_{vtype}'
    old_value = int(r.get(key))
    new_value = old_value + deployment_value
    if new_value >= 0 :
        r.set(f"{key}",new_value )
        return "Deployment Done"
    else:
        return "Not possible"


def main():
    resources = {
        'Merzig-Wadern': {'TSF/LF/TLF': 87, 'DL': 4, 'GW': 21, 'KdoW': 8, 'ELW': 6, 'SW': 2, 'WLF': 20},
        'Neunkirchen': {'TSF/LF/TLF': 61, 'DL': 3, 'GW': 17, 'KdoW': 8, 'ELW': 13, 'SW': 3, 'WLF': 3, 'MTW': 22},
        'Saarbrücken': {'TSF/LF/TLF': 106, 'DL': 13, 'GW': 43, 'KdoW': 16, 'ELW': 8, 'SW': 3, 'WLF': 3, 'MTW': 33},
        'Saarlouis': {'TSF/LF/TLF': 101, 'DL': 7, 'GW': 26, 'KdoW': 17, 'ELW': 10, 'SW': 1, 'WLF': 2, 'MTW': 24},
        'Saarpfalz-Kreis': {'TSF/LF/TLF': 76, 'DL': 3, 'GW': 26, 'KdoW': 9, 'ELW': 6, 'SW': 1, 'WLF': 2, 'MTW': 26},
        'St. Wendel': {'TSF/LF/TLF': 73, 'DL': 2, 'GW': 20, 'KdoW': 7, 'ELW': 8, 'SW': 3, 'WLF': 5, 'MTW': 28}
    }
    # init_vehicle_info(resources)

    print(update_resources('Merzig-Wadern', 'GW', -20))
    get_meta_deta(resources)
# def process_data_for_(data_frame):
#     data_frame['dt_iso'] = pd.to_datetime(data_frame['dt_iso'], format='%Y-%m-%d %H:%M:%S %z UTC')
#
#     # Remove repeating timestamps for each city
#     data_frame = data_frame.drop_duplicates(subset=['city_name', 'dt_iso'], keep='first')
# def process_data_in_range(data_frame, start_date, end_date, city_name):
#     # Convert dt_iso to datetime with the correct format
#     data_frame['dt_iso'] = pd.to_datetime(data_frame['dt_iso'], format='%Y-%m-%d %H:%M:%S %z UTC')
#
#     data_frame = data_frame.drop_duplicates(subset=['city_name', 'dt_iso', 'rain_1h'], keep='first')
#
#     # Ensure rain_1h is a float for aggregation and fill NaN values with 0
#     data_frame['rain_1h'] = pd.to_numeric(data_frame['rain_1h'], errors='raise').fillna(0)
#
#     # Create a new column for the 24-hour window (start of each day)
#     data_frame['day'] = data_frame['dt_iso'].dt.floor('d')
#
#
#     # Convert start_date and end_date to datetime
#     start_date = pd.to_datetime(start_date, format='%Y-%m-%d').tz_localize('UTC')
#     end_date = pd.to_datetime(end_date, format='%Y-%m-%d').tz_localize('UTC')
#
#     # Filter data for the specified city and date range
#     city_data = data_frame[(data_frame['city_name'] == city_name) &
#                            (data_frame['day'] >= start_date) &
#                            (data_frame['day'] <= end_date)]
#
#     # Group by day and sum the rain_1h values
#     daily_rainfall = city_data.groupby('day')['rain_1h'].sum().reset_index()
#
#     # Calculate total rainfall for the period
#     total_rainfall = daily_rainfall['rain_1h'].sum()
#
#     # Print total rainfall and flood warning if applicable
#     if total_rainfall >= 50.00:
#         return {f"{city_name}":f"Flood Warning {total_rainfall:.2f}mm"}
#     else:
#         return {f"{city_name}": f"No Flood Warning {total_rainfall:.2f}mm"}
#
#     # Test the function with specific values
#     # calculate_rainfall(data_frame, 'Merzig', '2024-03-01', '2024-03-03')
#     # calculate_rainfall(data_frame, 'Saarbrücken', '2024-05-14', '2024-05-17')
#     # calculate_rainfall(data_frame, 'Homburg', '2024-04-01', '2024-04-05')
# # def main():
# #     # Set page configuration
# #     st.set_page_config(page_title="Multi-Functional Streamlit App", page_icon="🌟", layout="centered")
# #
# #     # Title of the application
# #     st.title("Multi-Functional Streamlit App")
# #
# #     # Feature 1: CSV File Upload Option with Input Field and Info Button
# #     st.header("CSV File Upload and Info")
# #
# #     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
#     input_text = st.text_input("Input Rainfall Threshold")
#     range_left = st.text_input("Input Left Interval")
#     range_right = st.text_input("Input Right Interval")
#
#     if st.button("Flood Predict"):
#         if uploaded_file is not None:
#             # Read the uploaded CSV file
#             special_dataframe = pd.read_csv(uploaded_file)
#             if input_text and range_left and range_right:
#                 st.write(f"You entered: {input_text}")
#                 data = process_data_in_range(special_dataframe, range_left, range_right, input_text)
#                 st.write(data)
#
#             else:
#                 pass
#
#         else:
#             st.warning("Please upload a CSV file first.")
#
#
#
#
#
#     # Divider
#     st.markdown("---")
#
#     # Feature 2: Three Input Fields to Print a Dictionary with Beautiful CSS
#     st.header("Manage Resources")
#
#     field1 = st.text_input("Enter Location", key="field1")
#     field2 = st.text_input("Enter Vehicle Type", key="field2")
#     field3 = st.text_input("Enter Deployment Amount", key="field3")
#
#     if st.button("Update Resources"):
#         if field1 and field2 and field3:
#             result_dict = {
#                 "Field 1": field1,
#                 "Field 2": field2,
#                 "Field 3": field3
#             }
#             st.markdown("""
#             <style>
#             .result-container {
#                 background-color: #f0f0f0;
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin-top: 20px;
#                 box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
#             }
#             .result-container h4 {
#                 color: #333333;
#             }
#             .result-container p {
#                 color: #555555;
#                 font-size: 16px;
#             }
#             </style>
#             """, unsafe_allow_html=True)
#
#             st.markdown('<div class="result-container">', unsafe_allow_html=True)
#             st.markdown(f'<h4>Generated Dictionary</h4>', unsafe_allow_html=True)
#             for key, value in result_dict.items():
#                 st.markdown(f'<p><strong>{key}:</strong> {value}</p>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.warning("Please fill in all three fields.")
#     if st.button("Resource Meta Data"):
#         st.markdown("""
#         <style>
#         .print-container {
#             background-color: #e0ffe0;
#             border-radius: 10px;
#             padding: 20px;
#             margin-top: 20px;
#             box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
#         }
#         .print-container h4 {
#             color: #333333;
#         }
#         .print-container p {
#             color: #555555;
#             font-size: 16px;
#         }
#         </style>
#         """, unsafe_allow_html=True)
#
#         st.markdown('<div class="print-container">', unsafe_allow_html=True)
#         st.markdown(f'<h4>Printed Dictionary</h4>', unsafe_allow_html=True)
#         for key, value in result_dict.items():
#             st.markdown(f'<p><strong>{key}:</strong> {value}</p>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
