#!/usr/bin/env python3
"""
UI Feedback Manager - Provides comprehensive, real-time feedback during generation

This module manages progress tracking and user feedback for all generation processes,
ensuring users always know the current status with updates at least every 5 seconds.
"""

import logging
import time
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class PhaseStatus(Enum):
    """Status values for generation phases."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class SectionStatus(Enum):
    """Status values for individual sections."""
    PENDING = "pending"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class SectionProgress:
    """Progress information for a single section."""
    status: SectionStatus = SectionStatus.PENDING
    progress: float = 0.0
    duration: Optional[float] = None
    error: Optional[str] = None
    retry_count: int = 0
    start_time: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'status': self.status.value,
            'progress': self.progress,
            'duration': self.duration,
            'error': self.error,
            'retry_count': self.retry_count
        }

@dataclass
class PhaseProgress:
    """Progress information for a generation phase."""
    status: PhaseStatus = PhaseStatus.PENDING
    duration: Optional[float] = None
    start_time: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'status': self.status.value,
            'duration': self.duration
        }

@dataclass
class JobProgress:
    """Complete progress information for a job."""
    job_id: str
    batch_id: Optional[str] = None
    batch_position: Optional[str] = None
    overall_status: str = "initializing"
    current_phase: str = "job_preparation"
    phases: Dict[str, PhaseProgress] = field(default_factory=dict)
    sections: Dict[str, SectionProgress] = field(default_factory=dict)
    overall_progress: float = 0.0
    estimated_completion: Optional[str] = None
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())
    next_update_in: float = 5.0
    start_time: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Initialize default phases."""
        if not self.phases:
            self.phases = {
                'job_preparation': PhaseProgress(),
                'content_generation': PhaseProgress(),
                'template_rendering': PhaseProgress(),
                'pdf_conversion': PhaseProgress()
            }

class UIFeedbackManager:
    """
    Provides comprehensive, real-time feedback to users during all generation processes.
    
    Manages progress tracking with maximum 5-second update intervals and immediate
    updates for phase transitions, completions, and errors.
    """
    
    def __init__(self, update_interval: float = 5.0):
        """
        Initialize UI feedback manager.
        
        Args:
            update_interval: Maximum seconds between progress updates (default 5.0)
        """
        self.update_interval = max(1.0, min(update_interval, 10.0))  # Clamp to 1-10 seconds
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Storage for job progress
        self.job_progress: Dict[str, JobProgress] = {}
        self.batch_progress: Dict[str, Dict] = {}
        
        # Threading for periodic updates
        self._update_lock = threading.Lock()
        self._update_thread = None
        self._stop_updates = False
        
        # Callbacks for real-time updates
        self.progress_callbacks: Dict[str, Callable] = {}
        
        self.logger.info(f"UIFeedbackManager initialized with {self.update_interval}s update interval")
    
    def start_job_tracking(self, job_id: str, batch_id: str = None) -> None:
        """
        Begin tracking a job with optional batch context.
        
        Args:
            job_id: Unique identifier for the job
            batch_id: Optional batch identifier for batch operations
        """
        with self._update_lock:
            batch_position = None
            if batch_id and batch_id in self.batch_progress:
                batch_info = self.batch_progress[batch_id]
                batch_position = f"{len(batch_info['jobs']) + 1}/{batch_info['total_jobs']}"
            
            self.job_progress[job_id] = JobProgress(
                job_id=job_id,
                batch_id=batch_id,
                batch_position=batch_position
            )
            
            # Add to batch tracking if applicable
            if batch_id:
                if batch_id not in self.batch_progress:
                    self.batch_progress[batch_id] = {
                        'batch_id': batch_id,
                        'total_jobs': 1,
                        'jobs': {},
                        'start_time': time.time(),
                        'status': 'in_progress'
                    }
                
                self.batch_progress[batch_id]['jobs'][job_id] = {
                    'status': 'starting',
                    'progress': 0.0
                }
        
        self.logger.info(f"Started tracking job {job_id}" + 
                        (f" in batch {batch_id}" if batch_id else ""))
        
        # Start update thread if not running
        self._ensure_update_thread_running()
        
        # Immediate update
        self._broadcast_update(job_id)
    
    def update_phase(self, job_id: str, phase: str, status: str) -> None:
        """
        Update current phase (job_preparation, content_generation, etc.).
        
        Args:
            job_id: Job identifier
            phase: Phase name
            status: Phase status (pending, in_progress, completed, failed)
        """
        with self._update_lock:
            if job_id not in self.job_progress:
                self.logger.warning(f"Job {job_id} not found for phase update")
                return
            
            job = self.job_progress[job_id]
            
            # Update phase status
            if phase in job.phases:
                old_status = job.phases[phase].status
                job.phases[phase].status = PhaseStatus(status)
                
                if status == "in_progress":
                    job.phases[phase].start_time = time.time()
                    job.current_phase = phase
                elif status in ["completed", "failed"]:
                    if job.phases[phase].start_time:
                        job.phases[phase].duration = time.time() - job.phases[phase].start_time
            
            # Update overall status
            if status == "in_progress":
                job.overall_status = f"{phase.replace('_', ' ')}"
            elif status == "completed":
                # Check if this was the last phase
                if phase == "pdf_conversion":
                    job.overall_status = "completed"
                    job.overall_progress = 1.0
            elif status == "failed":
                job.overall_status = f"failed_in_{phase}"
            
            job.last_update = datetime.now().isoformat()
            
            # Update batch progress if applicable
            if job.batch_id and job.batch_id in self.batch_progress:
                self.batch_progress[job.batch_id]['jobs'][job_id]['status'] = status
        
        self.logger.info(f"Job {job_id} phase '{phase}' updated to '{status}'")
        
        # Immediate update for phase transitions
        self._broadcast_update(job_id)
    
    def update_section_progress(self, job_id: str, section: str, 
                              progress: float, status: str) -> None:
        """
        Update individual section progress.
        
        Args:
            job_id: Job identifier
            section: Section name (summary, skills, experience, etc.)
            progress: Progress value (0.0 to 1.0)
            status: Section status
        """
        with self._update_lock:
            if job_id not in self.job_progress:
                self.logger.warning(f"Job {job_id} not found for section update")
                return
            
            job = self.job_progress[job_id]
            
            # Initialize section if not exists
            if section not in job.sections:
                job.sections[section] = SectionProgress()
            
            section_prog = job.sections[section]
            old_status = section_prog.status
            
            # Update section progress
            section_prog.status = SectionStatus(status)
            section_prog.progress = max(0.0, min(1.0, progress))
            
            if status == "starting" and not section_prog.start_time:
                section_prog.start_time = time.time()
            elif status in ["completed", "failed", "timeout"]:
                if section_prog.start_time:
                    section_prog.duration = time.time() - section_prog.start_time
            
            # Calculate overall progress for content generation phase
            if job.current_phase == "content_generation":
                completed_sections = sum(1 for s in job.sections.values() 
                                       if s.status == SectionStatus.COMPLETED)
                total_sections = len(job.sections)
                if total_sections > 0:
                    phase_progress = completed_sections / total_sections
                    job.overall_progress = 0.1 + (phase_progress * 0.6)  # 10% prep + 60% content
            
            job.last_update = datetime.now().isoformat()
            
            # Update batch progress
            if job.batch_id and job.batch_id in self.batch_progress:
                self.batch_progress[job.batch_id]['jobs'][job_id]['progress'] = job.overall_progress
        
        self.logger.debug(f"Job {job_id} section '{section}' updated: {status} ({progress:.1%})")
        
        # Immediate update for section completions and failures
        if status in ["completed", "failed", "timeout"]:
            self._broadcast_update(job_id)
    
    def get_progress_update(self, job_id: str) -> dict:
        """
        Get current progress for UI polling.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Progress dictionary for JSON response
        """
        with self._update_lock:
            if job_id not in self.job_progress:
                return {
                    'error': f'Job {job_id} not found',
                    'job_id': job_id
                }
            
            job = self.job_progress[job_id]
            
            # Calculate estimated completion
            estimated_completion = None
            if job.overall_progress > 0.1:  # Only estimate after some progress
                elapsed = time.time() - job.start_time
                estimated_total = elapsed / job.overall_progress
                estimated_remaining = estimated_total - elapsed
                estimated_completion = (datetime.now() + 
                                      timedelta(seconds=estimated_remaining)).isoformat()
            
            return {
                'job_id': job.job_id,
                'batch_id': job.batch_id,
                'batch_position': job.batch_position,
                'overall_status': job.overall_status,
                'current_phase': job.current_phase,
                'phases': {name: phase.to_dict() for name, phase in job.phases.items()},
                'sections': {name: section.to_dict() for name, section in job.sections.items()},
                'overall_progress': job.overall_progress,
                'estimated_completion': estimated_completion,
                'last_update': job.last_update,
                'next_update_in': self.update_interval
            }
    
    def broadcast_batch_progress(self, batch_id: str) -> None:
        """
        Send batch-level progress updates.
        
        Args:
            batch_id: Batch identifier
        """
        if batch_id not in self.batch_progress:
            return
        
        batch_info = self.batch_progress[batch_id]
        
        # Calculate batch statistics
        total_jobs = len(batch_info['jobs'])
        completed_jobs = sum(1 for job in batch_info['jobs'].values() 
                           if job['status'] in ['completed', 'failed'])
        
        batch_progress = completed_jobs / total_jobs if total_jobs > 0 else 0
        
        batch_update = {
            'batch_id': batch_id,
            'total_jobs': total_jobs,
            'completed_jobs': completed_jobs,
            'batch_progress': batch_progress,
            'jobs': batch_info['jobs'],
            'status': 'completed' if completed_jobs == total_jobs else 'in_progress',
            'elapsed_time': time.time() - batch_info['start_time']
        }
        
        self.logger.info(f"Batch {batch_id} progress: {completed_jobs}/{total_jobs} jobs completed")
        
        # Broadcast to any registered callbacks
        for callback in self.progress_callbacks.values():
            try:
                callback('batch_update', batch_update)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {str(e)}")
    
    def register_progress_callback(self, callback_id: str, callback: Callable) -> None:
        """Register callback for real-time progress updates."""
        self.progress_callbacks[callback_id] = callback
        self.logger.info(f"Registered progress callback: {callback_id}")
    
    def unregister_progress_callback(self, callback_id: str) -> None:
        """Unregister progress callback."""
        if callback_id in self.progress_callbacks:
            del self.progress_callbacks[callback_id]
            self.logger.info(f"Unregistered progress callback: {callback_id}")
    
    def _broadcast_update(self, job_id: str) -> None:
        """Broadcast immediate update to registered callbacks."""
        update_data = self.get_progress_update(job_id)
        
        for callback in self.progress_callbacks.values():
            try:
                callback('job_update', update_data)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {str(e)}")
    
    def _ensure_update_thread_running(self) -> None:
        """Ensure the periodic update thread is running."""
        if self._update_thread is None or not self._update_thread.is_alive():
            self._stop_updates = False
            self._update_thread = threading.Thread(
                target=self._periodic_update_loop,
                daemon=True
            )
            self._update_thread.start()
            self.logger.info("Started periodic update thread")
    
    def _periodic_update_loop(self) -> None:
        """Periodic update loop running in background thread."""
        while not self._stop_updates:
            try:
                time.sleep(self.update_interval)
                
                with self._update_lock:
                    active_jobs = [job_id for job_id, job in self.job_progress.items()
                                 if job.overall_status not in ['completed', 'failed']]
                
                # Send periodic updates for active jobs
                for job_id in active_jobs:
                    self._broadcast_update(job_id)
                    # Also log periodic status to ensure logging continues
                    job = self.job_progress.get(job_id)
                    if job:
                        self.logger.info(f"Job {job_id} status: {job.overall_status} ({job.overall_progress:.1%}) - {job.current_phase}")
                
                # Send batch updates
                for batch_id in list(self.batch_progress.keys()):
                    self.broadcast_batch_progress(batch_id)
                
                # Clean up old completed jobs (older than 1 hour)
                self._cleanup_old_jobs()
                
            except Exception as e:
                self.logger.error(f"Error in periodic update loop: {str(e)}")
    
    def _cleanup_old_jobs(self) -> None:
        """Clean up job progress data for old completed jobs."""
        cutoff_time = time.time() - 3600  # 1 hour ago
        
        with self._update_lock:
            jobs_to_remove = []
            
            for job_id, job in self.job_progress.items():
                if (job.overall_status in ['completed', 'failed'] and 
                    job.start_time < cutoff_time):
                    jobs_to_remove.append(job_id)
            
            for job_id in jobs_to_remove:
                del self.job_progress[job_id]
                self.logger.debug(f"Cleaned up old job progress: {job_id}")
    
    def stop_tracking(self) -> None:
        """Stop all progress tracking and cleanup resources."""
        self._stop_updates = True
        
        if self._update_thread and self._update_thread.is_alive():
            self._update_thread.join(timeout=1.0)
        
        with self._update_lock:
            self.job_progress.clear()
            self.batch_progress.clear()
            self.progress_callbacks.clear()
        
        self.logger.info("Stopped progress tracking")
    
    def get_all_active_jobs(self) -> Dict[str, dict]:
        """Get progress for all active jobs."""
        with self._update_lock:
            return {
                job_id: self.get_progress_update(job_id)
                for job_id in self.job_progress.keys()
            }