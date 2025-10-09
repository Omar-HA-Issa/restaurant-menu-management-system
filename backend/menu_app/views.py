import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from .PDFreader import extract_text_from_pdf, extract_text_from_image
import json
import mysql.connector
from datetime import datetime
import anthropic
import unicodedata


def process_with_anthropic_api(text):
    try:
        # Get API key from environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = anthropic.Anthropic(api_key=api_key)

        # Print the extracted text for debugging
        print("Extracted text being sent to Claude:", text)

        # Simplify the prompt and make it more explicit
        prompt = f"""
        Given the following restaurant menu data:

        {text}

        Return ONLY valid JSON matching this structure:
        {{
            "restaurant": {{
                "name": "string",
                "location": "string"
            }},
            "menu_sections": [
                {{
                    "section_name": "string",
                    "items": [
                        {{
                            "name": "string",
                            "description": "string",
                            "price": number,
                            "dietary_restriction_id": number
                        }}
                    ]
                }}
            ]
        }}

        Rules:
        1. CRITICALLY IMPORTANT: Analyze each menu item and assign appropriate dietary restrictions:
           - 1: No restriction (for meat/seafood dishes)
           - 2: Vegan (no animal products)
           - 3: Vegetarian (no meat but may have dairy/eggs)
           - 4: Gluten-Free
           - 5: Lactose-Free
        2. Descriptions: 5 words max or null
        3. Prices: must be > 0
        4. Remove Spanish accents

        For every item in the menu analyze or infer the ingredients to your knowledge and assign the correct dietary restriction that the item has.
        This is obligatory, no item should end up without a dietary restriction

        Output ONLY valid JSON.
        """

        # Make the API request
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Get response text and clean it
        response_text = response.content[0].text.strip()

        # Remove any markdown code block formatting
        response_text = response_text.replace('```json', '').replace('```', '').strip()

        print("Raw response from Claude (after cleaning):", response_text)

        # Try to parse JSON to validate it
        try:
            # Parse and re-serialize to ensure valid JSON
            parsed_json = json.loads(response_text)
            return json.dumps(parsed_json)
        except json.JSONDecodeError as e:
            print(f"JSON validation error: {e}")
            print(f"Response that failed parsing: {response_text}")
            raise

    except Exception as e:
        print(f"Error processing with Anthropic's Claude API: {e}")
        print(f"Error type: {type(e)}")
        raise


def normalize_spanish_text(text):
    """
    Normalize Spanish text by removing accents and converting to standard characters
    """
    if isinstance(text, str):
        normalized = unicodedata.normalize('NFKD', text)
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


def insert_into_database(structured_data):
    try:
        conn = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default'].get('PORT', 3306),
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )
        cursor = conn.cursor(buffered=True)

        # Insert all dietary restrictions first
        dietary_restrictions = ['No Restriction', 'Vegan', 'Vegetarian', 'Gluten-Free', 'Lactose-Free']
        for label in dietary_restrictions:
            cursor.execute(
                "INSERT IGNORE INTO menu_app_dietaryrestriction (label) VALUES (%s)",
                (label,)
            )

        # Create a mapping of dietary restriction labels to their IDs
        cursor.execute("SELECT restriction_id, label FROM menu_app_dietaryrestriction")
        dietary_mapping = {label: id for id, label in cursor.fetchall()}

        # Get restaurant name from structured data
        restaurant_data = structured_data.get('restaurant', {})
        restaurant_name = restaurant_data.get('name')

        # Check if restaurant already exists
        cursor.execute("SELECT restaurant_id FROM menu_app_restaurant WHERE name = %s", (restaurant_name,))
        existing_restaurant = cursor.fetchone()

        if existing_restaurant:
            restaurant_id = existing_restaurant[0]
            print(f"Using existing restaurant with ID: {restaurant_id}")

            cursor.execute(
                "SELECT MAX(version) FROM menu_app_menu WHERE restaurant_id = %s",
                (restaurant_id,)
            )
            latest_version = cursor.fetchone()[0]
            new_version = (latest_version or 0) + 1
        else:
            cursor.execute(
                "INSERT INTO menu_app_restaurant (name, location) VALUES (%s, %s)",
                (restaurant_name or 'Unknown', 'Unknown')
            )
            restaurant_id = cursor.lastrowid
            new_version = 1
            print(f"Created new restaurant with ID: {restaurant_id}")

        cursor.execute(
            "INSERT INTO menu_app_menu (restaurant_id, version, date) VALUES (%s, %s, %s)",
            (restaurant_id, new_version, datetime.now().date())
        )
        menu_id = cursor.lastrowid

        for section_order, section in enumerate(structured_data.get('menu_sections', []), 1):
            cursor.execute(
                "INSERT INTO menu_app_menusection (menu_id, section_name, section_order) VALUES (%s, %s, %s)",
                (menu_id, section.get('section_name', 'Unknown Section'), section_order)
            )
            section_id = cursor.lastrowid

            for item in section.get('items', []):
                try:
                    price = float(item.get('price', 0))
                    if price <= 0:
                        price = 0.01
                except (TypeError, ValueError):
                    price = 0.01

                # Get dietary restriction ID from mapping or default to 'No Restriction'
                dietary_label = {
                    1: 'No Restriction',
                    2: 'Vegan',
                    3: 'Vegetarian',
                    4: 'Gluten-Free',
                    5: 'Lactose-Free'
                }.get(item.get('dietary_restriction_id', 1), 'No Restriction')

                dietary_id = dietary_mapping.get(dietary_label, dietary_mapping['No Restriction'])

                cursor.execute(
                    "INSERT INTO menu_app_menuitem (section_id, name, description, price, dietary_restriction_id) VALUES (%s, %s, %s, %s, %s)",
                    (section_id,
                     item.get('name', 'Unknown Item'),
                     item.get('description'),
                     price,
                     dietary_id)
                )

        cursor.execute(
            "INSERT INTO menu_app_processinglog (menu_id, status, error_message, timestamp) VALUES (%s, %s, %s, %s)",
            (menu_id, 'successful', None, datetime.now())
        )

        conn.commit()
        print("Data successfully inserted into database")
        return True

    except Exception as e:
        print(f"Database insertion error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@csrf_exempt
def process_menu_pdf(request):
    if request.method == 'POST':
        if 'pdf_file' not in request.FILES:
            return JsonResponse({
                'status': 'error',
                'message': 'No PDF file uploaded'
            }, status=400)

        pdf_file = request.FILES['pdf_file']

        # Print file info for debugging
        print(f"Received file: {pdf_file.name}, size: {pdf_file.size} bytes")

        temp_pdf_path = os.path.join(settings.MEDIA_ROOT, 'temp_menu.pdf')
        with open(temp_pdf_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        try:
            extracted_text = extract_text_from_pdf(temp_pdf_path)

            # Print extracted text for debugging
            print("Extracted text from PDF:", extracted_text)

            if not extracted_text:
                extracted_text = extract_text_from_image(temp_pdf_path)
                print("Extracted text from image:", extracted_text)

            if not extracted_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Could not extract text from PDF'
                }, status=400)

            structured_data_json = process_with_anthropic_api(extracted_text)

            if not structured_data_json:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to process menu data with Claude API'
                }, status=400)

            # Clean and parse JSON
            try:
                structured_data = json.loads(structured_data_json)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error. Raw data: {structured_data_json}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'JSON parsing error: {str(e)}'
                }, status=400)

            cleaned_data = clean_structured_data(structured_data)

            if insert_into_database(cleaned_data):
                return JsonResponse({
                    'status': 'success',
                    'message': 'Menu processed and inserted successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to insert data into database'
                }, status=500)

        except Exception as e:
            print(f"Processing error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)


def menu_upload_view(request):
    """
    Render the menu upload template
    """
    if request.method == 'GET':
        return render(request, 'menu_app/menu_upload.html')