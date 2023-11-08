import requests
import logging


def get_faker_data(resource, locale="en_US", quantity=None, seed=None):
    # Construct the request URL with the correct query parameters
    params = {"_locale": locale, "_quantity": quantity, "_seed": seed}
    request_url = f"https://fakerapi.it/api/v1/{resource}"

    # Initialize session
    session = requests.Session()
    try:
        # Pass params to request method to ensure proper encoding
        response = session.get(request_url, params=params)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returns an unsuccessful status code

        # Assuming the successful response will always have a 'data' key.
        return response.json()["data"]
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTPError: {e}")
    except requests.exceptions.RequestException as e:
        # A base class for all requests exceptions.
        logging.error(f"RequestException: {e}")
    except KeyError:
        logging.error(f"KeyError: 'data' not found in the response.")
    except ValueError as e:  # Includes JSONDecodeError
        logging.error(f"ValueError: There was an error decoding the response JSON. {e}")

    # Return an empty list or None if there was an error.
    return None
