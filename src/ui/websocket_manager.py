"""
WebSocket manager for real-time updates to the UI.

Provides functions to broadcast notifications, job updates, and phase updates
to all connected clients.

Requirements: 21.9
"""

from typing import Dict, Any, Set
from flask_socketio import SocketIO, emit
from flask import request
from datetime import datetime
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Global SocketIO instance (will be initialized by app)
socketio: SocketIO = None

# Track connected clients
connected_clients: Set[str] = set()


def init_socketio(app) -> SocketIO:
    """
    Initialize SocketIO with the Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        SocketIO instance
    """
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        client_id = request.sid
        connected_clients.add(client_id)
        logger.info(f"Client connected: {client_id} (total: {len(connected_clients)})")
        emit('connected', {'message': 'Connected to ResumAI'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        client_id = request.sid
        connected_clients.discard(client_id)
        logger.info(f"Client disconnected: {client_id} (total: {len(connected_clients)})")
    
    return socketio


def broadcast_toast(message: str, level: str = "info") -> None:
    """
    Broadcast a toast notification to all connected clients.
    
    Args:
        message: Notification message
        level: Notification level (info, success, warning, error)
    """
    if socketio is None:
        logger.warning("SocketIO not initialized, cannot broadcast toast")
        return
    
    payload = {
        "message": message,
        "level": level,
        "timestamp": datetime.now().isoformat()
    }
    
    socketio.emit('toast', payload, broadcast=True)
    logger.debug(f"Broadcast toast: {message} ({level})")


def broadcast_job_update(job_folder_name: str, updates: Dict[str, Any]) -> None:
    """
    Broadcast a job update to all connected clients.
    
    Args:
        job_folder_name: Name of the job folder
        updates: Dictionary of updated fields
    """
    if socketio is None:
        logger.warning("SocketIO not initialized, cannot broadcast job update")
        return
    
    payload = {
        "job_folder_name": job_folder_name,
        "updates": updates,
        "timestamp": datetime.now().isoformat()
    }
    
    socketio.emit('job_update', payload, broadcast=True)
    logger.debug(f"Broadcast job update: {job_folder_name}")


def broadcast_phase_update(phase: str, count: int) -> None:
    """
    Broadcast a phase count update to all connected clients.
    
    Args:
        phase: Phase name (e.g., "1_Queued", "2_Data_Generated")
        count: Number of jobs in the phase
    """
    if socketio is None:
        logger.warning("SocketIO not initialized, cannot broadcast phase update")
        return
    
    payload = {
        "phase": phase,
        "count": count,
        "timestamp": datetime.now().isoformat()
    }
    
    socketio.emit('phase_update', payload, broadcast=True)
    logger.debug(f"Broadcast phase update: {phase} = {count}")


def get_connected_clients_count() -> int:
    """
    Get the number of connected clients.
    
    Returns:
        Number of connected clients
    """
    return len(connected_clients)
