import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the product review page
url = 'https://www.verkkokauppa.com/fi/product/601150/Fiskars-Hard-Face-paistokasari-26-cm-2-8-l/reviews'

# Add headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Send a GET request to fetch the page content
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code != 200:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
else:
    print(f"Page fetched successfully, status code: {response.status_code}")

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a list to store the review data
    reviews_data = []

    # Loop through each review container in the page
    reviews = soup.find_all('li', class_='sc-9sorzd-4 Ijieh')  # Update this class if needed

    # Check if reviews exist
    if not reviews:
        print("No reviews found.")
    else:
        print(f"Found {len(reviews)} reviews.")

        # Loop through the reviews and extract required fields
        for review in reviews:
            product_category = 'Fiskars Hard Face paistokasari 26 cm'

            # Extract the customer's age group
            name_and_age = review.find('div', class_='sc-p2iykm-2 ifXEcu')
            name_and_age_text = name_and_age.text.strip() if name_and_age else 'No Age Group'

            # Extract the date for each review
            date_time = review.find('time')
            date_text = date_time['datetime'] if date_time else 'No Date'

            overall_for_product = review.find('div', class_="sc-eXsaLi ffhteq sc-awkpk3-0 jwnjWg")
            overall_for_product = overall_for_product.text.strip() if overall_for_product else "No overall review"

            # Extract product quality percentage
            product_quality = review.find('div', class_='sc-eXsaLi hmiOvS sc-awkpk3-0 jwnjWg')
            product_quality_percentage = "No product quality review"
            if product_quality and product_quality.has_attr('percentage'):
                product_quality_percentage = product_quality['percentage']

            # Extract value for money percentage
            value_for_money = review.find('div', class_='sc-eXsaLi ffhteq sc-awkpk3-0 jwnjWg')
            money_percentage = "No value for money review"
            if value_for_money and value_for_money.has_attr('percentage'):
                money_percentage = value_for_money['percentage']

            # Extract ease of use percentage
            ease_of_use = review.find('div', class_='sc-eXsaLi hmiOvS sc-awkpk3-0 jwnjWg')
            ease_percentage = "No ease of use review"
            if ease_of_use and ease_of_use.has_attr('percentage'):
                ease_percentage = ease_of_use['percentage']

            # Extract the Feedback Text
            feedback_text = review.find('div', class_='review-content-wrapper')
            feedback_text = feedback_text.text.strip() if feedback_text else 'No Feedback'

            # Append the extracted data to the list
            reviews_data.append({
                'Customer Name and Age': name_and_age_text,
                'Feedback Date': date_text,
                'Overall for product': overall_for_product,
                'Product quality': product_quality_percentage,
                'Value for money': money_percentage,
                'Ease of use': ease_percentage,
                'Feedback Text': feedback_text,
                'Product/Service Category': product_category
            })

    # Convert the list to a pandas DataFrame
    if reviews_data:
        df = pd.DataFrame(reviews_data)

        # Save the DataFrame to a CSV file
        file_path = '/Users/administrator/Downloads/WebScraping/reviews.csv'
        df.to_csv(file_path, index=False, encoding='utf-8-sig')  # UTF-8 encoding for correct characters
        print(f"Scraping complete. Reviews saved to '{file_path}'.")
    else:
        print("No data to save.")
