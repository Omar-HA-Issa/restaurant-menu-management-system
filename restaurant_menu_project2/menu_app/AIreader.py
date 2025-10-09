import mysql.connector
from datetime import datetime
import json
import os
from .PDFreader import extract_text_from_pdf, extract_text_from_image
import anthropic
import unicodedata


def process_with_anthropic_api(text):
    try:
        # Use API key from environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = anthropic.Anthropic(api_key=api_key)

        # Constructing the prompt
        prompt = f"""
        Given the following restaurant menu data:

        {text}

        Organize it into structured data that matches the following schema:
        - Restaurant: [(restaurant_id, name, location)]
        - Menu: [(menu_id, restaurant_id, version, date)]
        - MenuSection: [(section_id, menu_id, section_name, order)]
        - MenuItem: [(item_id, section_id, name, description, price, dietary_restriction_id)]
        - DietaryRestriction: [(restriction_id, label)]
        - ProcessingLog: [(log_id, menu_id, status, error_message, timestamp)]

        Output the schema into a JSON file

        Process this restaurant menu with the following CRITICAL requirements:
        -For the `menu` and `menu_items` tables ensure the following:

            1. Every menu item must:
                - Include a `price` (greater than 0).
                - A brief description of the dish (5 words max), ensuring it accurately reflects the dish.
                - Contain a valid `dietary_id`, which refers to an entry in the `dietary_restrictions` table.
                - DESCRIPTION HANDLING REQUIREMENTS:
                    - If NO description is available for a menu item:
                        * Set description to NULL
                        * Do NOT use placeholder text like "No description available"
                    - Ensure description field can be truly empty/null when no meaningful description exists
           . 

        -ACCENT & CHARACTER HANDLING:
            - Convert ALL Spanish accented characters to their non-accented equivalents
            - Examples: 
                  * 'ñ' → 'n'
                  * 'á' → 'a'
                  * 'é' → 'e'
                  * 'í' → 'i'
                  * 'ó' → 'o'
                  * 'ú' → 'u'

        -Please process the following data and include the `ProcessingLog` in your response. The log should contain the following details:
            - `log_id`: A unique identifier for the log entry.
            - `menu_id`: The ID associated with the menu.
            - `status`: The processing status (success or failure).
            - `error_message`: Any error messages that occurred during processing.
            - `timestamp`: The timestamp of when the log was created.

            Ensure the `ProcessingLog` is populated and not empty.

        -DIETARY RESTRICTION REQUIREMENTS:
            - MANDATORY: Analyze EVERY SINGLE menu item for dietary restrictions
            - Create dietary restriction tags for ALL menu items
            - Assign at least ONE dietary restriction to EACH menu item. 
            - Possible restrictions include:
                1. No restriction
                2. Vegan
                3. Vegetarian
                4. Gluten-Free
                5. Lactose-Free

        IMPORTANT: 
        - Respond ONLY with a valid JSON string
        - Ensure the JSON is properly formatted
        - Do not include any additional text or explanation
        """

        # Make the API request using messages method
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Print the full response to see what's being returned
        structured_data_json = response.content[0].text

        return structured_data_json

    except Exception as e:
        print(f"Error processing with Anthropic's Claude API: {e}")
        return None


def normalize_spanish_text(text):
    """
    Normalize Spanish text by removing accents and converting to standard characters
    This method preserves the base character while removing diacritical marks
    """
    if isinstance(text, str):
        # Decompose characters into base character and accent
        normalized = unicodedata.normalize('NFKD', text)
        # Keep only the base characters
        return ''.join(c for c in normalized if not unicodedata.combining(c))
    return text


def clean_structured_data(structured_data):
    """
    Clean the structured data by applying accent normalization
    """

    def deep_normalize(obj):
        if isinstance(obj, dict):
            return {k: deep_normalize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [deep_normalize(item) for item in obj]
        elif isinstance(obj, str):
            return normalize_spanish_text(obj)
        return obj

    return deep_normalize(structured_data)


# Function to insert data into the MySQL database
def insert_into_database(structured_data):
    try:
        # Use database credentials from environment variables
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'restaurant_menus')
        )
        cursor = conn.cursor()

        # Insert Restaurant
        cursor.execute(
            "INSERT INTO menu_app_restaurant (name, location) VALUES (%s, %s)",
            (structured_data.get('restaurant_name', 'Unknown'),
             structured_data.get('restaurant_location', 'Unknown'))
        )
        restaurant_id = cursor.lastrowid

        # Insert Menu
        cursor.execute(
            "INSERT INTO menu_app_menu (restaurant_id, version, date) VALUES (%s, %s, %s)",
            (restaurant_id, 1, datetime.now().date())
        )
        menu_id = cursor.lastrowid

        # Ensure a default dietary restriction exists
        cursor.execute("INSERT IGNORE INTO menu_app_dietaryrestriction (label) VALUES ('No Restriction')")
        cursor.execute("SELECT restriction_id FROM menu_app_dietaryrestriction WHERE label = 'No Restriction'")
        default_dietary_id = cursor.fetchone()[0]

        # Insert Menu Sections and Items
        for section_order, section in enumerate(structured_data.get('menu_sections', []), 1):
            cursor.execute(
                "INSERT INTO menu_app_menusection (menu_id, section_name, section_order) VALUES (%s, %s, %s)",
                (menu_id, section.get('section_name', 'Unknown Section'), section_order)
            )
            section_id = cursor.lastrowid

            for item in section.get('items', []):
                cursor.execute(
                    "INSERT INTO menu_app_menuitem (section_id, name, description, price, dietary_restriction_id) VALUES (%s, %s, %s, %s, %s)",
                    (section_id,
                     item.get('name', 'Unknown Item'),
                     item.get('description'),
                     item.get('price', 0.00),
                     default_dietary_id)
                )

        # Insert Processing Log
        cursor.execute(
            "INSERT INTO menu_app_processinglog (menu_id, status, error_message) VALUES (%s, %s, %s)",
            (menu_id, 'successful', None)
        )

        conn.commit()
        print("Data successfully inserted into database")
    except Exception as e:
        print(f"Database insertion error: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Main function to process the PDF and integrate with the database
def main():
    pdf_file_path = r"C:\Users\User\Downloads\PETRUS-PRESTIGE-211024.pdf"
    image_credentials_path = r"C:\Users\User\Downloads\database-443218-8d1a699e81ad.json"

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_file_path)

    if not extracted_text:
        print("No text extracted from the PDF. Attempting to extract text from an image.")
        extracted_text = extract_text_from_image("path_to_image.jpg", image_credentials_path)

    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)

        # Process the text using the Anthropics Claude API
        structured_data_json = process_with_anthropic_api(extracted_text)

        if structured_data_json:
            try:
                # Clean the JSON string of extra backticks or formatting
                structured_data_json = structured_data_json.strip('`')
                structured_data_json = structured_data_json.replace('```json', '').replace('```', '').strip()
                structured_data_json = structured_data_json.split('{', 1)[-1]
                structured_data_json = '{' + structured_data_json

                # Debug: Check what the cleaned string looks like
                print("Cleaned JSON String:")
                print(structured_data_json)

                # Parse the JSON string
                structured_data = json.loads(structured_data_json)
                print("Successfully parsed JSON:")
                print(json.dumps(structured_data, indent=2))
                cleaned_data = clean_structured_data(structured_data)

                # Apply normalization to clean accents
                if "MenuItems" in structured_data:
                    for item in structured_data["MenuItems"]:
                        for i in range(len(item)):
                            if isinstance(item[i], str):
                                item[i] = normalize_spanish_text(item[i])

                # Save JSON to a file
                with open("normalized_menu_data.json", "w", encoding="utf-8") as f:
                    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

                # Insert structured data into the database
                insert_into_database(structured_data)
            except json.JSONDecodeError as e:
                print("JSON Decode Error:")
                print(f"Error details: {e}")
                print("Problematic JSON string:")
                print(structured_data_json)
        else:
            print("Failed to process structured data with the Anthropics Claude API.")

    else:
        print("No text could be extracted from the PDF or image.")


if __name__ == "__main__":
    main()