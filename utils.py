import os
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import logging

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'tif'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    """General image processing utilities"""
    try:
        # Add any common image processing steps here
        logging.info(f"Processing image: {image_path}")
        return True
    except Exception as e:
        logging.error(f"Image processing failed: {str(e)}")
        return False

def generate_report_pdf(session, report):
    """Generate PDF diagnostic report"""
    try:
        # Create PDF file path
        pdf_filename = f"report_{session.session_id}.pdf"
        pdf_path = os.path.join('generated', pdf_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Title
        story.append(Paragraph("Virtual IHC Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Patient/Session Information
        story.append(Paragraph("Analysis Information", heading_style))
        
        info_data = [
            ['Session ID:', session.session_id],
            ['Original File:', session.original_filename],
            ['Analysis Date:', session.created_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Processing Time:', str(session.completed_at - session.created_at) if session.completed_at else 'N/A'],
            ['Status:', session.processing_status.upper()]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Analysis Results
        story.append(Paragraph("Analysis Results", heading_style))
        
        results_data = [
            ['HER2 Status:', session.her2_prediction or 'Not determined'],
            ['Confidence Score:', f"{session.confidence_score:.1%}" if session.confidence_score else 'N/A'],
            ['Cancer Grade:', session.cancer_grade or 'Not determined'],
            ['Biomarker Expression:', f"{session.biomarker_percentage:.1f}%" if session.biomarker_percentage else 'N/A'],
            ['Staining Intensity:', session.staining_intensity or 'Not assessed']
        ]
        
        results_table = Table(results_data, colWidths=[2*inch, 3*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 20))
        
        # Quantitative Analysis (if available)
        if report and report.positive_cell_count:
            story.append(Paragraph("Quantitative Analysis", heading_style))
            
            quant_data = [
                ['Positive Cells:', str(report.positive_cell_count)],
                ['Total Cells:', str(report.total_cell_count)],
                ['Positive Percentage:', f"{(report.positive_cell_count/report.total_cell_count)*100:.1f}%"],
                ['Stained Area:', f"{report.stained_area_percentage:.1f}%"]
            ]
            
            quant_table = Table(quant_data, colWidths=[2*inch, 3*inch])
            quant_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(quant_table)
            story.append(Spacer(1, 20))
        
        # Summary
        if report and report.summary:
            story.append(Paragraph("Summary", heading_style))
            story.append(Paragraph(report.summary.replace('\n', '<br/>'), styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Recommendations
        if report and report.recommendations:
            story.append(Paragraph("Recommendations", heading_style))
            story.append(Paragraph(report.recommendations.replace('\n', '<br/>'), styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Technical Notes
        if report and report.technical_notes:
            story.append(Paragraph("Technical Notes", heading_style))
            story.append(Paragraph(report.technical_notes.replace('\n', '<br/>'), styles['Normal']))
        
        # Disclaimer
        story.append(Spacer(1, 30))
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.red,
            alignment=1
        )
        story.append(Paragraph(
            "<b>DISCLAIMER:</b> This report is generated using AI-based virtual IHC analysis for research and educational purposes. "
            "Results should be validated with traditional IHC methods for clinical decision-making.",
            disclaimer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        logging.info(f"PDF report generated: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logging.error(f"PDF generation failed: {str(e)}")
        raise

def format_confidence(confidence):
    """Format confidence score for display"""
    if confidence is None:
        return "N/A"
    return f"{confidence:.1%}"

def format_percentage(percentage):
    """Format percentage for display"""
    if percentage is None:
        return "N/A"
    return f"{percentage:.1f}%"

def get_status_badge_class(status):
    """Get Bootstrap badge class for status"""
    status_classes = {
        'uploaded': 'bg-secondary',
        'processing': 'bg-warning',
        'completed': 'bg-success',
        'failed': 'bg-danger'
    }
    return status_classes.get(status, 'bg-secondary')

def get_her2_badge_class(her2_status):
    """Get Bootstrap badge class for HER2 status"""
    her2_classes = {
        'positive': 'bg-danger',
        'negative': 'bg-success',
        'equivocal': 'bg-warning'
    }
    return her2_classes.get(her2_status, 'bg-secondary')
