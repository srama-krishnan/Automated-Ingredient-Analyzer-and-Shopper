# Automated-Ingredient-Analyzer-and-Shopper

This Python project is designed to simplify the grocery shopping experience for those who love cooking at home. By inputting the name of a dish, users can receive a detailed list of ingredients, along with the best options for purchasing these items from Ocado based on price, customer ratings, and review counts. This tool leverages web scraping, data cleaning, and analysis techniques to provide valuable insights, making grocery shopping more efficient and cost-effective.

## Features

- Fetches ingredients for a specified dish using OpenAI's language model.
- Scrapes Ocado for price, link, rating, and review count of each ingredient.
- Analyzes and filters data to select the best product options.
- Outputs a clean and concise summary for easy decision-making.

## Getting Started

### Prerequisites

- Python 3.6+
- OpenAI API Key
- Required Python packages: `requests`, `beautifulsoup4`, `pandas`

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/srama-krishnan/ocado-scraper-analyzer.git
cd ocado-scraper-analyzer
```
```bash
pip install -r requirements.txt
```
### Configuration
Create a .env file in the project directory.
Add your OpenAI API key to the .env file as follows:
```makefile
OPENAI_API_KEY=your_api_key_here
```
Ensure the script reads the API key from the .env file by updating the relevant code section.

### Usage
To use Automated Ingredient Analyzer and Shopper, follow these steps:
Run the script:
```bash
python script.py
```
When prompted, enter the dish name for which you wish to analyze ingredients.
The script will then output a summary of the best options for each ingredient based on the scraped data.

### Contribution
To contribute to Automated Ingredient Analyzer and Shopper, follow these steps:
```
1. Fork this repository.
2. Create a new branch: git checkout -b branch_name.
3. Make your changes and commit them: git commit -m 'commit_message'.
4. Push to the original branch: git push origin Automated Ingredient Analyzer and Shopper/branch_name.
5. Create the pull request.
```
Alternatively, see the GitHub documentation on creating a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

#### Acknowledgments
Thanks to OpenAI for providing the GPT API.
This project does not endorse any specific online grocery platform.
