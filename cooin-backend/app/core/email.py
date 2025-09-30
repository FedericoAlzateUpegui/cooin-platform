"""
Email service for sending verification emails and notifications.
Supports both SMTP and development modes with template rendering.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from pathlib import Path
import os

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Enhanced email service with template support and multiple delivery methods."""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.from_email = settings.SMTP_USER

    def _create_smtp_connection(self) -> smtplib.SMTP:
        """Create and configure SMTP connection."""
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            raise ValueError("SMTP configuration is incomplete. Please check your .env file.")

        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        if self.smtp_tls:
            server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        return server

    def _send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """Send email using SMTP or development mode."""
        try:
            # Development mode - just log the email
            if settings.DEBUG or not self.smtp_host:
                logger.info("=== EMAIL (Development Mode) ===")
                logger.info(f"To: {', '.join(to_emails)}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {text_content or html_content}")
                logger.info("=== END EMAIL ===")
                return True

            # Production mode - send via SMTP
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)

            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f"attachment; filename= {attachment['filename']}"
                    )
                    msg.attach(part)

            # Send email
            with self._create_smtp_connection() as server:
                server.send_message(msg)

            logger.info(f"Email sent successfully to {', '.join(to_emails)}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {', '.join(to_emails)}: {str(e)}")
            return False

    def send_verification_email(self, email: str, username: str, verification_token: str) -> bool:
        """Send email verification email to new user."""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"

        subject = f"Welcome to {settings.PROJECT_NAME} - Verify Your Email"

        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .container {{ max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9fafb; }}
                .button {{
                    display: inline-block;
                    background: #4F46E5;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; color: #6B7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{settings.PROJECT_NAME}</h1>
                </div>
                <div class="content">
                    <h2>Welcome to {settings.PROJECT_NAME}, {username}!</h2>
                    <p>Thank you for registering with us. To complete your registration and start connecting with lenders and borrowers, please verify your email address by clicking the button below:</p>

                    <center>
                        <a href="{verification_url}" class="button">Verify My Email</a>
                    </center>

                    <p>This verification link will expire in 24 hours for your security.</p>

                    <p>If you didn't create an account with us, you can safely ignore this email.</p>

                    <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
                </div>
                <div class="footer">
                    <p>If you're having trouble clicking the button, copy and paste this link into your browser:</p>
                    <p>{verification_url}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text content
        text_content = f"""
        Welcome to {settings.PROJECT_NAME}, {username}!

        Thank you for registering with us. To complete your registration, please verify your email address by visiting:

        {verification_url}

        This verification link will expire in 24 hours for your security.

        If you didn't create an account with us, you can safely ignore this email.

        Best regards,
        The {settings.PROJECT_NAME} Team
        """

        return self._send_email([email], subject, html_content, text_content)

    def send_password_reset_email(self, email: str, username: str, reset_token: str) -> bool:
        """Send password reset email."""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        subject = f"{settings.PROJECT_NAME} - Reset Your Password"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .container {{ max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }}
                .header {{ background: #EF4444; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9fafb; }}
                .button {{
                    display: inline-block;
                    background: #EF4444;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; color: #6B7280; font-size: 14px; }}
                .warning {{ background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Hello {username},</h2>
                    <p>We received a request to reset your password for your {settings.PROJECT_NAME} account.</p>

                    <center>
                        <a href="{reset_url}" class="button">Reset My Password</a>
                    </center>

                    <div class="warning">
                        <strong>Important:</strong> This reset link will expire in 1 hour for your security.
                    </div>

                    <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>

                    <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
                </div>
                <div class="footer">
                    <p>If you're having trouble clicking the button, copy and paste this link into your browser:</p>
                    <p>{reset_url}</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {username},

        We received a request to reset your password for your {settings.PROJECT_NAME} account.

        Please visit this link to reset your password:
        {reset_url}

        This reset link will expire in 1 hour for your security.

        If you didn't request a password reset, you can safely ignore this email.

        Best regards,
        The {settings.PROJECT_NAME} Team
        """

        return self._send_email([email], subject, html_content, text_content)

    def send_connection_notification(
        self,
        recipient_email: str,
        recipient_name: str,
        sender_name: str,
        connection_type: str
    ) -> bool:
        """Send notification when someone wants to connect."""
        subject = f"New Connection Request - {settings.PROJECT_NAME}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .container {{ max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }}
                .header {{ background: #10B981; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9fafb; }}
                .button {{
                    display: inline-block;
                    background: #10B981;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; color: #6B7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Connection Request</h1>
                </div>
                <div class="content">
                    <h2>Hello {recipient_name},</h2>
                    <p><strong>{sender_name}</strong> wants to connect with you on {settings.PROJECT_NAME}!</p>

                    <p>Connection Type: <strong>{connection_type}</strong></p>

                    <p>Log in to your account to view their profile and respond to the connection request.</p>

                    <center>
                        <a href="{settings.FRONTEND_URL}/connections" class="button">View Connection Requests</a>
                    </center>

                    <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {recipient_name},

        {sender_name} wants to connect with you on {settings.PROJECT_NAME}!

        Connection Type: {connection_type}

        Log in to your account to view their profile and respond to the connection request.

        Visit: {settings.FRONTEND_URL}/connections

        Best regards,
        The {settings.PROJECT_NAME} Team
        """

        return self._send_email([recipient_email], subject, html_content, text_content)

    def send_loan_application_notification(
        self,
        lender_email: str,
        lender_name: str,
        borrower_name: str,
        loan_amount: float
    ) -> bool:
        """Send notification to lender when someone applies for their loan."""
        subject = f"New Loan Application - {settings.PROJECT_NAME}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .container {{ max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }}
                .header {{ background: #F59E0B; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background: #f9fafb; }}
                .button {{
                    display: inline-block;
                    background: #F59E0B;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                }}
                .amount {{
                    background: #FEF3C7;
                    border: 2px solid #F59E0B;
                    padding: 15px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Loan Application</h1>
                </div>
                <div class="content">
                    <h2>Hello {lender_name},</h2>
                    <p><strong>{borrower_name}</strong> has submitted a loan application.</p>

                    <div class="amount">
                        ${loan_amount:,.2f}
                    </div>

                    <p>Review their application and profile to make an informed decision.</p>

                    <center>
                        <a href="{settings.FRONTEND_URL}/loan-applications" class="button">Review Application</a>
                    </center>

                    <p>Best regards,<br>The {settings.PROJECT_NAME} Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {lender_name},

        {borrower_name} has submitted a loan application for ${loan_amount:,.2f}.

        Review their application and profile to make an informed decision.

        Visit: {settings.FRONTEND_URL}/loan-applications

        Best regards,
        The {settings.PROJECT_NAME} Team
        """

        return self._send_email([lender_email], subject, html_content, text_content)


# Global email service instance
email_service = EmailService()


def get_email_service() -> EmailService:
    """Get the global email service instance."""
    return email_service