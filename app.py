from flask import Flask, render_template, request, send_from_directory, jsonify
from markupsafe import Markup
import os
from dotenv import load_dotenv
import requests
import json
import re
import time

app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

# Set up Anthropic API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

def format_response(text):
    # Use regex to wrap each numbered section in HTML tags
    formatted = re.sub(r'(\d+\.\s*[A-Z\s]+)', r'<h3>\1</h3>', text)
    # Replace newlines with <br> tags
    formatted = formatted.replace('\n', '<br>')
    return formatted

def generate_analysis(host_company, industry_vertical, existing_customers, target_industries, competitors, company_size, country):
    messages = [
        {
            "role": "user",
            "content": f"""You are a market research analyst tasked with providing meaningful insights to help define target audiences for a marketing team.
Your goal is to analyze the given information and generate detailed responses for various categories. These insights should be actionable and assist in creating effective audience marketing strategies.

Here is the information provided from the form response:

HOST COMPANY: <host_company>{host_company}</host_company>
INDUSTRY VERTICAL: <industry_vertical>{industry_vertical}</industry_vertical>
TARGET COMPANY SIZE: <company_size>{company_size}</company_size>
COUNTRY: <country>{country}</country>
EXISTING CUSTOMERS: <existing_customers>{existing_customers}</existing_customers>
TARGET INDUSTRIES: <target_industries>{target_industries}</target_industries>
COMPETITORS: <competitors>{competitors}</competitors>

Using this information as a basis, conduct research that adds to the information provided, building up a profile of prospective audience(s) for marketing, including additional companies, value proposition, for the following categories:

1. HOST COMPANY
2. INDUSTRY VERTICAL
3. TARGET COMPANY SIZE
4. COUNTRY
5. EXISTING CUSTOMERS
6. TARGET INDUSTRIES
7. COMPETITORS
8. TRENDS
9. UNIQUE INSIGHT
10. REFINE TARGET AUDIENCE
11. POTENTIAL CHALLENGES
12. COUNTRY TARGETS
13. CREATIVE IDEA
14. USEFUL RESOURCES

For each category, follow these specific instructions:

1-7. For the first seven categories, summarize and enhance on the provided information, offering additional companies in the same catergory with context and insights relevant to marketing strategies.

8. TRENDS: Highlight any recent patterns or trends in the industry or market.

9. UNIQUE INSIGHT: Identify and explain any unexpected or unique information that could be valuable for marketing purposes.

10. REFINE TARGET AUDIENCE: Suggest ways the information you provided could be used to refine target audiences.

11. POTENTIAL CHALLENGES: Provide two potential challenges and how to overcome them.

12. COUNTRY TARGETS: Provide ten similar other target companies as a list on a new line numbered i, ii, etc.

13. CREATIVE IDEA: Provide one recommendation for a creative marketing tactic to try that's not obvious.

14. USEFUL RESOURCES: Provide ten useful resources (with URLs) as a list on a new line numbered i, ii, etc.

Format your response as follows:
1. Use numbered sectioned headings for each category (1. HOST COMPANY, 2. INDUSTRY VERTICAL, etc.)
2. Present your insights for each category in the following format:
   <category_name>
   Your detailed analysis and insights here with a line break after each.
   </category_name>
3. Use sub-points (i., ii., iii., etc.) where appropriate, such as for the lists in TARGET INDUSTRIES, COMPETITORS, COUNTRY TARGETS, and USEFUL RESOURCES.

Throughout your analysis, focus on extracting insights that will be particularly useful for the marketing team in defining and understanding target audiences. If you notice any gaps in the information provided or areas where additional research could be beneficial, mention these in your analysis.

Remember to base your insights on thorough research and provide detailed, actionable information that goes beyond the initial form responses. Your goal is to offer valuable insights that will help the marketing team create effective strategies for reaching their target audiences."""
        }
    ]

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            headers = {
                "x-api-key": anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 4000,
                "messages": messages
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            response_json = response.json()
            
            if response.status_code == 200:
                analysis = response_json['content'][0]['text']
                formatted_analysis = format_response(analysis)
                return formatted_analysis
            elif response.status_code == 429 or "Overloaded" in str(response_json):
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    return "<h4>We're experiencing high demand. Please try again in a few minutes.</h4>"
            else:
                error_message = response_json.get('error', {}).get('message', 'Unknown error')
                return f"<h4>An error occurred: {error_message}</h4>"
    
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"<h4>An unexpected error occurred. Please try again later.</h4>"

    return "<h4>Unable to complete the analysis after multiple attempts. Please try again later.</h4>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        host_company = request.form.get('host_company')
        industry_vertical = request.form.get('industry_vertical')
        existing_customers = request.form.get('existing_customers')
        target_industries = request.form.get('target_industries')
        competitors = request.form.get('competitors')
        company_size = request.form.get('company_size')
        country = request.form.get('country')

        analysis = generate_analysis(host_company, industry_vertical, existing_customers, 
                                  target_industries, competitors, company_size, country)
        return render_template('result.html', analysis=Markup(analysis))

    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)