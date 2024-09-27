import pandas as pd
import geopandas as gpd

# filepath to provincial shapefile
PROVINCES_SHAPEFILE = '../../data/drf-provinces'
SHAPEFILE_COLUMN = 'ADM1_FR'

def preprocess_province_map_data(data, parameters):
    """
    Preprocesses data for the province map plot.
    """
    time_col = parameters.get('time_col')
    deaths_only = parameters.get('deaths_only', False)
    date_range = parameters.get('date_range_inclusive', {})
    start_date = date_range.get('start_date')
    end_date = date_range.get('end_date')

    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # filter out non-death data if specified
    if deaths_only:
        data = data[data['status'] == 'died']

    # filter by date range
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (data[time_col] >= start_date) & (data[time_col] <= end_date)
        data = data.loc[mask]

    # aggregate data at provincial level
    province_cases = data.groupby('province').size().reset_index(name='count')

    return province_cases