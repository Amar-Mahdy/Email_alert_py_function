
# Created by: Amar Ibrahim

# This python script is to query BigQuery table and based on the calculation result it uses 
# the SMTP server to send an email alerts to the specified emails

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import bigquery



def gmp_alert(event, context):
  
  # Construct a BigQuery client object.
  client = bigquery.Client()
  
  # Set up query to check spent against target for each client
  query = """
      SELECT partner
      FROM `project.dataset.table`
      WHERE spend > budget_insured
  """

  # Run query and get results
  query_job = client.query(query)
  results = list(query_job.result())
  message = ""

  # If there are results, send email
  if len(results) > 0:
      # Set up message parameters
      sender_email = "name@gmail.com"
      emails = ['amar@Gmail.com', 'joo@Gmail.com']
      password = "xxxxxxxxxxxxxx"
      message = MIMEMultipart("alternative")
      message["Subject"] = "Failer Warning"
      message["From"] = sender_email
      message["To"] =  ', '.join(emails)

      # Create HTML content for email body
      html = """\
      <html>
      <head>
      <style>
      body {
          font-family: 'Calibri', sans-serif;
          font-size: 12pt;
      }
      .warning {
          font-family: 'Calibri', sans-serif;
          color: red;
          font-weight: bold;
          font-size: 12pt;
      }
      </style>
      </head>
      <body>
      <h1 class="warning">Warning</h1> 
      <p></p>
      <p>This is an alert to notify that one or more partner(s) has exceeded their GMP spending limit as defined by their credit limit. It regards the following partner(s):</p>
      <ol>
      """
      partners = [row.partner for row in results]
      html += "\n".join(f"<li>{partner.capitalize()}</li>" for partner in partners)
      html += """
      </ol>
      </body>
      </html>
      """
      # Attach HTML content to message object
      html_part = MIMEText(html, "html")
      message.attach(html_part)
    
      # Connect to Gmail SMTP server and send email
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
          server.login(sender_email, password)
          server.sendmail(sender_email, emails, message.as_string())

      return "Function executed successfully"
