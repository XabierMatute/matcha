# import logging
# from models.profile_model import (
#     get_profile_by_user_id,
#     update_profile,
#     get_location,
#     update_location,
#     create_profile as create_profile_entry
# )
# from typing import Dict
# from flask import current_app

# # Configure logging
# # logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_profile(user_id: int) -> Dict:
#     """
#     Creates an initial profile for a new user.

#     Args:
#         user_id (int): The ID of the user.

#     Returns:
#         Dict: The created profile data.
#     """
#     logger.info("Creating profile for user_id: %d", user_id)
#     try:
#         profile = create_profile_entry(user_id)
#         logger.info("Profile created successfully: %s", profile)
#         return profile
#     except Exception as e:
#         logger.error("Failed to create profile for user_id %d: %s", user_id, str(e))
#         raise Exception("Error creating profile") from e

# def get_user_profile(user_id: int) -> Dict:
#     """
#     Retrieves the profile data for a given user.

#     Args:
#         user_id (int): The ID of the user.

#     Returns:
#         Dict: The user's profile data.
#     """
#     logger.info("Fetching profile for user_id: %d", user_id)
#     try:
#         profile = get_profile_by_user_id(user_id)
#         if not profile:
#             logger.error("Profile not found for user_id: %d", user_id)
#             raise ValueError("Profile not found.")
#         logger.info("Profile fetched successfully: %s", profile)
#         return profile
#     except Exception as e:
#         logger.error("Failed to fetch profile for user_id %d: %s", user_id, str(e))
#         raise Exception("Error fetching profile") from e

# def update_user_profile(user_id: int, data: Dict) -> Dict:
#     """
#     Updates the profile data for a user.

#     Args:
#         user_id (int): The ID of the user.
#         data (Dict): Profile fields to update.

#     Returns:
#         Dict: The updated profile data.
#     """
#     logger.info("Updating profile for user_id: %d with data: %s", user_id, data)
#     try:
#         updated_profile = update_profile(user_id, **data)
#         logger.info("Profile updated successfully: %s", updated_profile)
#         return updated_profile
#     except Exception as e:
#         logger.error("Failed to update profile for user_id %d: %s", user_id, str(e))
#         raise Exception("Error updating profile") from e

# def get_user_location(user_id: int) -> Dict:
#     """
#     Retrieves the location data for a given user.

#     Args:
#         user_id (int): The ID of the user.

#     Returns:
#         Dict: The user's location data.
#     """
#     logger.info("Fetching location for user_id: %d", user_id)
#     try:
#         location = get_location(user_id)
#         if not location:
#             logger.error("Location not found for user_id: %d", user_id)
#             raise ValueError("Location not found.")
#         logger.info("Location fetched successfully: %s", location)
#         return location
#     except Exception as e:
#         logger.error("Failed to fetch location for user_id %d: %s", user_id, str(e))
#         raise Exception("Error fetching location") from e

# def update_user_location(user_id: int, location: str, latitude: float, longitude: float) -> Dict:
#     """
#     Updates the location data for a user.

#     Args:
#         user_id (int): The ID of the user.
#         location (str): New location.
#         latitude (float): Latitude of the location.
#         longitude (float): Longitude of the location.

#     Returns:
#         Dict: Updated location data.
#     """
#     logger.info("Updating location for user_id: %d", user_id)
#     try:
#         updated_location = update_location(user_id, location, latitude, longitude)
#         logger.info("Location updated successfully: %s", updated_location)
#         return updated_location
#     except Exception as e:
#         logger.error("Failed to update location for user_id %d: %s", user_id, str(e))
#         raise Exception("Error updating location") from e



