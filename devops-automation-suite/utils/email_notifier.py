"""
Email Notification Utility
Sends email notifications for alerts and events
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import setup_logger

logger = setup_logger('email')


def send_notification(subject, body, config):
    """
    Send email notification
    
    Args:
        subject: Email subject
        body: Email body
        config: Configuration dictionary
    """
    email_config = config.get('email', {})
    
    if not email_config.get('enabled', False):
        logger.debug("Email notifications disabled")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email_config.get('from_address')
        msg['To'] = email_config.get('to_address')
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(
            email_config.get('smtp_server'),
            email_config.get('smtp_port', 587)
        )
        server.starttls()
        server.login(
            email_config.get('username'),
            email_config.get('password')
        )
        
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email notification sent: {subject}")
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
