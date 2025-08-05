#!/usr/bin/env python3
"""
EduRAG Web Application
Flask web interface for the NCERT RAG system
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.vectorstore import load_vectorstore
from src.retriever import get_retriever
from src.query_engine import build_rag_chain
from src.ingest import ingest_pdfs
from src.config import GEMINI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'edurag-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables for RAG components
rag_chain = None
system_status = {
    'initialized': False,
    'error': None,
    'last_updated': None,
    'pdf_count': 0,
    'vectorstore_ready': False
}

VECTORSTORE_DIR = Path("./docs")
PDF_DIR = Path("./data")
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def initialize_rag_system():
    """Initialize the RAG system components"""
    global rag_chain, system_status
    
    try:
        logger.info("Initializing RAG system...")
        
        # Check API key
        if not GEMINI_API_KEY:
            raise EnvironmentError("GEMINI_API_KEY not configured")
        
        # Check for PDF files
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        system_status['pdf_count'] = len(pdf_files)
        
        if not pdf_files:
            logger.warning("No PDF files found in data directory")
            system_status['error'] = "No PDF files found. Please upload some PDFs."
            return False
        
        # Check if vectorstore needs initialization
        if not VECTORSTORE_DIR.exists() or not any(VECTORSTORE_DIR.iterdir()):
            logger.info("Vectorstore not found, running ingestion...")
            ingest_pdfs()
        
        # Load vectorstore
        logger.info("Loading vectorstore...")
        vectordb = load_vectorstore()
        system_status['vectorstore_ready'] = True
        
        # Set up retriever
        logger.info("Setting up retriever...")
        retriever = get_retriever(vectordb)
        
        # Build RAG chain
        logger.info("Building RAG chain...")
        rag_chain = build_rag_chain(retriever)
        
        system_status['initialized'] = True
        system_status['error'] = None
        system_status['last_updated'] = datetime.now().isoformat()
        
        logger.info("RAG system initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        system_status['error'] = str(e)
        system_status['initialized'] = False
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', status=system_status)

@app.route('/api/status')
def api_status():
    """Get system status"""
    return jsonify(system_status)

@app.route('/api/query', methods=['POST'])
def api_query():
    """Process a query"""
    global rag_chain
    
    if not system_status['initialized'] or not rag_chain:
        return jsonify({
            'success': False,
            'error': 'System not initialized. Please check system status.'
        }), 500
    
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({
            'success': False,
            'error': 'No question provided'
        }), 400
    
    question = data['question'].strip()
    if not question:
        return jsonify({
            'success': False,
            'error': 'Empty question provided'
        }), 400
    
    try:
        start_time = time.time()
        logger.info(f"Processing query: {question}")
        
        # Get answer from RAG chain
        result = rag_chain.invoke(question)
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'answer': result,
            'question': question,
            'processing_time': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error processing query: {str(e)}'
        }), 500

@app.route('/api/reinitialize', methods=['POST'])
def api_reinitialize():
    """Reinitialize the RAG system"""
    logger.info("Reinitializing RAG system...")
    success = initialize_rag_system()
    
    return jsonify({
        'success': success,
        'status': system_status
    })

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload PDF files"""
    if request.method == 'GET':
        return render_template('upload.html', status=system_status)
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = PDF_DIR / filename
        
        try:
            file.save(file_path)
            logger.info(f"Uploaded file: {filename}")
            
            # Update PDF count
            system_status['pdf_count'] = len(list(PDF_DIR.glob("*.pdf")))
            
            return jsonify({
                'success': True,
                'message': f'File {filename} uploaded successfully',
                'filename': filename
            })
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return jsonify({'success': False, 'error': 'Invalid file type. Only PDF files are allowed.'}), 400

@app.route('/api/pdfs')
def api_list_pdfs():
    """List all PDF files"""
    pdf_files = []
    for pdf_path in PDF_DIR.glob("*.pdf"):
        pdf_files.append({
            'name': pdf_path.name,
            'size': pdf_path.stat().st_size,
            'modified': datetime.fromtimestamp(pdf_path.stat().st_mtime).isoformat()
        })
    
    return jsonify({
        'success': True,
        'files': pdf_files,
        'count': len(pdf_files)
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'system_initialized': system_status['initialized']
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure directories exist
    PDF_DIR.mkdir(exist_ok=True)
    VECTORSTORE_DIR.mkdir(exist_ok=True)
    
    # Initialize RAG system on startup
    logger.info("Starting EduRAG Web Application...")
    initialize_rag_system()
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)