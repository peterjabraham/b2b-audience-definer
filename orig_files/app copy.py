from flask import Flask, render_template, request, send_from_directory
from markupsafe import Markup
import os
from dotenv import load_dotenv
import anthropic
import re

app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

# Set up Anthropic API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

def format_response(text):
    # Remove any trailing spaces at the end of lines
    text = re.sub(r' +\n', '\n', text)
    # Replace all newlines with spaces
    text = text.replace('\n', ' ')
    
    # Split the text into sections based on numbered points
    sections = re.split(r'(\d+\.)', text)[1:]  # Skip the first empty split
    
    formatted_html = ""
    for i in range(0, len(sections), 2):
        number = sections[i]
        content = sections[i+1] if i+1 < len(sections) else ""
        
        # Extract the title and content
        parts = content.split(':', 1)
        title = parts[0].strip()
        section_content = parts[1].strip() if len(parts) > 1 else ""
        
        # Format each section with HTML
        formatted_html += f"<h3>{number} {title}</h3>"
        
        # Format sub-points (i, ii, iii, etc.)
        sub_points = re.split(r'([ivx]+\.)', section_content, flags=re.IGNORECASE)
        formatted_content = ""
        for j in range(0, len(sub_points), 2):
            sub_point_numeral = sub_points[j]
            sub_point_content = sub_points[j+1].strip() if j+1 < len(sub_points) else ""
            if sub_point_numeral:
                formatted_content += f"<h6><strong>{sub_point_numeral}</strong> {sub_point_content}</h6>"
            else:
                formatted_content += f"<h6>{sub_point_content}</h6>"
        
        # Special handling for URLs in section 14
        if number.strip() == "14.":
            urls = re.findall(r'(https?://\S+)', formatted_content)
            if urls:
                formatted_content = "<ul>"
                for url in urls:
                    formatted_content += f'<li><a href="{url}" target="_blank">{url}</a></li>'
                formatted_content += "</ul>"
        
        formatted_html += formatted_content if formatted_content else f"<h6>{section_content}</h6>"
    
    return formatted_html

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect form data
        host_company = request.form.get('host_company')
        industry_vertical = request.form.get('industry_vertical')
        existing_customers = request.form.get('existing_customers')
        target_industries = request.form.get('target_industries')
        competitors = request.form.get('competitors')
        company_size = request.form.get('company_size')
        country = request.form.get('country')

        # Prepare the prompt for Claude
        prompt = f"""Human: You are a market research analyst tasked with providing meaningful insights to help define target audiences for a marketing team.
        Your goal is to analyze the given information and generate detailed responses for various categories. These insights should be actionable and assist in creating effective audience marketing strategies.

        Here is the information provided from the form response:

        HOST COMPANY: <host_company>{host_company}</host_company>
        INDUSTRY VERTICAL: <industry_vertical>{industry_vertical}</industry_vertical>
        TARGET COMPANY SIZE: <company_size>{company_size}</company_size>
        COUNTRY: <country>{country}</country>
        EXISTING CUSTOMERS: <existing_customers>{existing_customers}</existing_customers>
        TARGET INDUSTRIES: <target_industries>{target_industries}</target_industries>
        COMPETITORS: <competitors>{competitors}</competitors>

        Using this information as a starting point, conduct research and provide detailed insights for the following categories:

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

        1-7. For the first seven categories, summarize and expand on the provided information, offering additional context and insights relevant to marketing strategies.

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

        Remember to base your insights on thorough research and provide detailed, actionable information that goes beyond the initial form responses. Your goal is to offer valuable insights that will help the marketing team create effective strategies for reaching their target audiences.
        """

        # Call Anthropic API
        try:
            response = client.completions.create(
                model="claude-3-sonnet-20240229",
                prompt=prompt,
                max_tokens_to_sample=4000,
            )
            analysis = response.completion
            formatted_analysis = format_response(analysis)
        except Exception as e:
            formatted_analysis = f"<h4>An error occurred: {str(e)}</h4>"

        # Render the result template
        return render_template('result.html', 
                               host_company=host_company,
                               industry_vertical=industry_vertical,
                               existing_customers=existing_customers,
                               target_industries=target_industries,
                               competitors=competitors,
                               company_size=company_size,
                               country=country,
                               analysis=Markup(formatted_analysis))
    
    # If it's a GET request, show the form
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)