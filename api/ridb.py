import os
from dotenv import load_dotenv
import requests
from typing import Optional, Tuple, Dict, Any

load_dotenv()

RIDB_API_KEY = os.getenv("RIDB_API_KEY") or "DEMO_KEY"
GOOGLE_API_KEY = os.getenv("GOOGLE_GEOCODE_KEY") or "DEMO_KEY"


def get_city_coordinates(location_name: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude coordinates for a city using Google Maps Geocoding API.

    Args:
        location_name (str): Name of a location to search for.

    Returns:
        Optional[Tuple[float, float]]: Tuple of (latitude, longitude) if found, None if not found

    Raises:
        requests.RequestException: If there's an error with the API request
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "key": GOOGLE_API_KEY,
        "address": location_name,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        data = response.json()

        # Check if results were found and status is OK
        if data.get("status") == "OK" and "results" in data and len(data["results"]) > 0:
            # Get the first result
            first_result = data["results"][0]
            location = first_result["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            
            return (latitude, longitude)
          
        else:
            status = data.get("status", "UNKNOWN")
            print(f"No results found for city: {location_name}. Status: {status}")
            return None

    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        raise
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_camping_facilities(latitude: float, longitude: float, radius: int = 25,
                           limit: int = 50, offset: int = 0, activity: str = "CAMPING") -> Optional[Dict[str, Any]]:
    """
    Get camping facilities near given coordinates using Recreation.gov API.
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        radius (int): Search radius in miles (default: 25)
        limit (int): Maximum number of results to return (default: 50)
        offset (int): Number of results to skip (default: 0)
        activity (str): Activity type to search for (default: "CAMPING")
    Returns:
        Optional[Dict[str, Any]]: Dictionary with facilities data if found, None if error
    Raises:
        requests.RequestException: If there's an error with the API request
    """
    # Ensure RIDB_API_KEY is available
    if not RIDB_API_KEY:
        raise ValueError("RIDB_API_KEY is not configured")
    
    base_url = "https://ridb.recreation.gov/api/v1/facilities"
    params = {
        "limit": limit,
        "offset": offset,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "activity": activity
    }
    headers = {
        "accept": "application/json",
        "apikey": RIDB_API_KEY
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data and "RECDATA" in data:
            return data

    except requests.RequestException as e:
        print(f"Error making API request to Recreation.gov: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise  # Re-raise instead of returning None for consistency


def find_camping_near_city(location_name: str, radius: int = 25, limit: int = 50) -> Optional[Dict[str, Any]]:
    """
    Find camping facilities near a city or location combining geocoding and recreation facility search.

    Args:
        location_name (str): Name of a location to search for
        radius (int): Search radius in miles (default: 25)
        limit (int): Maximum number of results to return (default: 50)

    Returns:
        Optional[Dict[str, Any]]: Dictionary with facilities data if found, None if error
    """
    # First, get the coordinates for the city
    coordinates = get_city_coordinates(location_name)

    if coordinates is None:
        print(f"Could not find coordinates for city: {location_name}")
        return None

    latitude, longitude = coordinates

    # Then, search for camping facilities near those coordinates
    facilities = get_camping_facilities(latitude, longitude, radius, limit)

    if facilities and "RECDATA" in facilities:
        facility_count = len(facilities["RECDATA"])
        print(f"Found {facility_count} camping facilities within {radius} miles of {location_name}")
        return facilities
    else:
        print(f"No camping facilities found within {radius} miles of {location_name}")
        return None
