from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_ingredients():
    llm = ChatOpenAI(openai_api_key="Your API KEY Here")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class technical documentation writer."),
        ("user", "{input}")
    ])
    chain = prompt | llm

    ip1= ": for the dish given below, give me all ingredients one by one only with the name without giving options or any other unnecessary detail only with the ingredient name one by one separated by comma in a single line. give me in the format of Sure, here are the ingredients for the dish:"
    user_input = input("Enter your request: ")
    ingredients = chain.invoke({"input": user_input + ip1}).content
    ingredients_list = ingredients.split(':', 1)[-1].strip().split(',')
    return ingredients_list

def scrape_ocado_prices(ingredients):
    base_url = "https://www.ocado.com/search?entry="
    results = []

    for ingredient in ingredients:
        full_url = base_url + ingredient
        response = requests.get(full_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            li_elements = soup.find_all('li', class_=lambda x: x and ('fops-item--featured' in x or 'fops-item--cluster' in x))
            for li in li_elements:
                fop_item = li.find('div', class_='fop-item')
                if fop_item:
                    fop_content_wrapper = fop_item.find('div', class_='fop-contentWrapper')
                    if fop_content_wrapper:
                        price_group_wrapper = fop_content_wrapper.find('div', class_='price-group-wrapper')
                        if price_group_wrapper:
                            price_span = price_group_wrapper.find('span', class_='fop-price')
                            price = price_span.text.strip() if price_span else "Price not found"
                        else:
                            price = "Price not found"
                        a_tag = fop_content_wrapper.find('a')
                        href = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None
                        full_href = f'www.ocado.com{href}' if href else 'Link not found'
                        review_wrapper = fop_content_wrapper.find('div', class_='review-wrapper')
                        if review_wrapper:
                            rating_span = review_wrapper.find('span', class_='fop-rating-inner')
                            rating = rating_span['title'].split()[1] if rating_span and 'title' in rating_span.attrs else "Rating not found"
                            count_span = review_wrapper.find('span', class_='fop-rating__count')
                            count_text = count_span.text.strip() if count_span else "Count not found"
                            count = count_text[count_text.find("(")+1:count_text.find(")")] if "(" in count_text and ")" in count_text else "Count not found"
                        else:
                            rating = "Rating not found"
                            count = "Count not found"
                        results.append({"Ingredient": ingredient, "Price": price, "Link": full_href, "Rating": rating, "Count": count})
        else:
            results.append({"Ingredient": ingredient, "Price": "Failed to fetch data", "Link": "Link not found", "Rating": "Rating not found", "Count": "Count not found"})
    return pd.DataFrame(results)

def clean_and_filter_data(df):
    df = df[df['Rating'] != "Rating not found"]
    df['Rating'] = df['Rating'].astype(float)
    df['Price'] = df['Price'].str.replace('[^\d.]', '', regex=True).astype(float)
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    return df

def aggregate_data(df):
    grouped_df = df.groupby('Ingredient')
    max_counts = grouped_df['Count'].max() / 50
    min_counts = grouped_df['Count'].min() / 50
    scores = max_counts - min_counts
    selected_ingredients = []
    for ingredient, group in grouped_df:
        max_score_index = group['Count'].idxmax()
        selected_ingredients.append(df.loc[max_score_index])
    return pd.DataFrame(selected_ingredients)

def pipeline():
    ingredients_list = get_ingredients()
    df_prices = scrape_ocado_prices(ingredients_list)
    df_prices.to_csv("result.csv")
    df = pd.read_csv("result.csv")
    df = clean_and_filter_data(df)
    selected_df = aggregate_data(df)
    return selected_df

if __name__ == "__main__":
    result_df = pipeline()
    newdf = result_df.filter(['Ingredient','Price','Rating','Count'],axis=1)
    print(newdf)
