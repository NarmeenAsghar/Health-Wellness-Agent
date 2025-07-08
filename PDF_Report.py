from fpdf import FPDF
from Context import UserSessionContext
from typing import Any
import tempfile
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Health & Wellness Progress Report", ln=True, align="C")
        self.ln(10)

def generate_user_report(context: UserSessionContext) -> str:
    """Generate a comprehensive PDF report for the user."""
    pdf = PDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Health & Wellness Progress Report", ln=True, align="C")
    pdf.ln(5)
    
    # User Information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "User Information:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Name: {context.name}", ln=True)
    pdf.cell(0, 8, f"User ID: {context.uid}", ln=True)
    if context.email:
        pdf.cell(0, 8, f"Email: {context.email}", ln=True)
    if context.created_at:
        pdf.cell(0, 8, f"Member Since: {context.created_at[:10]}", ln=True)
    if context.last_updated:
        pdf.cell(0, 8, f"Last Updated: {context.last_updated[:10]}", ln=True)
    pdf.ln(5)
    
    # Goals
    if context.goal:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Current Goals:", ln=True)
        pdf.set_font("Arial", size=10)
        if isinstance(context.goal, dict):
            for key, value in context.goal.items():
                pdf.cell(0, 8, f"{key}: {value}", ln=True)
        else:
            pdf.cell(0, 8, str(context.goal), ln=True)
        pdf.ln(5)
    
    # Preferences
    if context.diet_preferences:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Diet Preferences:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, context.diet_preferences, ln=True)
        pdf.ln(5)
    
    # Injury Notes
    if context.injury_notes:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Injury Notes:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, context.injury_notes, ln=True)
        pdf.ln(5)
    
    # Meal Plan
    if context.meal_plan:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Current Meal Plan:", ln=True)
        pdf.set_font("Arial", size=10)
        for i, meal in enumerate(context.meal_plan, 1):
            pdf.cell(0, 8, f"Day {i}: {meal}", ln=True)
        pdf.ln(5)
    
    # Workout Plan
    if context.workout_plan:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Current Workout Plan:", ln=True)
        pdf.set_font("Arial", size=10)
        if isinstance(context.workout_plan, dict):
            for key, value in context.workout_plan.items():
                if key == "days" and isinstance(value, list):
                    for i, day in enumerate(value, 1):
                        pdf.cell(0, 8, f"Day {i}: {day}", ln=True)
                else:
                    pdf.cell(0, 8, f"{key}: {value}", ln=True)
        else:
            pdf.cell(0, 8, str(context.workout_plan), ln=True)
        pdf.ln(5)
    
    # Progress Logs
    if context.progress_logs:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Progress Logs:", ln=True)
        pdf.set_font("Arial", size=10)
        for log in context.progress_logs:
            if isinstance(log, dict):
                for key, value in log.items():
                    pdf.cell(0, 8, f"{key}: {value}", ln=True)
            else:
                pdf.cell(0, 8, str(log), ln=True)
        pdf.ln(5)
    
    # Recent Conversation History
    if context.conversation_history:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Recent Conversations:", ln=True)
        pdf.set_font("Arial", size=9)
        
        # Show last 10 conversations
        recent_conversations = context.conversation_history[-10:]
        for msg in recent_conversations:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            
            # Truncate long content
            if len(content) > 80:
                content = content[:80] + "..."
            
            pdf.cell(0, 6, f"[{role.upper()}] {content}", ln=True)
            if timestamp:
                pdf.cell(0, 4, f"  Time: {timestamp[:19]}", ln=True)
        pdf.ln(5)
    
    # Handoff Logs
    if context.handoff_logs:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Agent Handoffs:", ln=True)
        pdf.set_font("Arial", size=10)
        for log in context.handoff_logs:
            pdf.cell(0, 8, log, ln=True)
        pdf.ln(5)
    
    # Footer
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    
    # Save to a file with user-specific name
    filename = f"health_report_{context.name}_{context.uid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filename = filename.replace(" ", "_")  # Remove spaces
    filepath = os.path.join(os.getcwd(), filename)
    
    pdf.output(filepath)
    return filepath

# Keep the old function for backward compatibility
def generate_pdf_report(context: UserSessionContext) -> str:
    return generate_user_report(context) 