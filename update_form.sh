cat << 'EOF' > update_form.sh
#!/bin/bash
cat << 'INNEREOF' > templates/form.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B2B Audience Definer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: black;
            color: white;
            padding: 20px;
        }
        h1 {
            font-weight: 800;
        }
        label {
            font-weight: 300;
            display: block;
            margin-top: 15px;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            background-color: white;
            color: black;
            border: none;
            font-family: 'Inter', sans-serif;
            font-weight: 300;
        }
        input[type="submit"] {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: white;
            color: black;
            border: none;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
        }
    </style>
</head>
<body>
    <h1>B2B Audience Definer</h1>
    <form method="POST">
        <label for="industry_vertical">Industry Vertical:</label>
        <input type="text" id="industry_vertical" name="industry_vertical" required>

        <label for="existing_customers">Existing Customers:</label>
        <textarea id="existing_customers" name="existing_customers" rows="4"></textarea>

        <label for="target_industries">Target Industries:</label>
        <textarea id="target_industries" name="target_industries" rows="4"></textarea>

        <label for="competitors">Competitors:</label>
        <textarea id="competitors" name="competitors" rows="4"></textarea>

        <label for="company_size">Company Size to Target:</label>
        <input type="text" id="company_size" name="company_size" required>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
INNEREOF
EOF