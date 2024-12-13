from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps
from typing import Callable, Optional
import logging
from contextlib import contextmanager

# Initialize metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'api_active_requests',
    'Number of active requests',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'api_errors_total',
    'Total number of API errors',
    ['method', 'endpoint', 'error_type']
)

# Service-specific metrics
CRAWLER_REQUESTS = Counter(
    'crawler_requests_total',
    'Total number of crawling requests',
    ['status']
)

CRAWLER_LATENCY = Histogram(
    'crawler_latency_seconds',
    'Crawling latency in seconds'
)

ANALYSIS_REQUESTS = Counter(
    'analysis_requests_total',
    'Total number of analysis requests',
    ['status']
)

ANALYSIS_LATENCY = Histogram(
    'analysis_latency_seconds',
    'Analysis latency in seconds'
)


class MetricsLogger:
    """Handler for logging and tracking metrics"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def track_time(
            self,
            metric: Histogram,
            labels: Optional[dict] = None
    ):
        """Context manager to track execution time"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            if labels:
                metric.labels(**labels).observe(duration)
            else:
                metric.observe(duration)

    def track_request(
            self,
            method: str,
            endpoint: str,
            status_code: int,
            duration: float
    ):
        """Track API request metrics"""
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def track_error(
            self,
            method: str,
            endpoint: str,
            error_type: str
    ):
        """Track API error metrics"""
        ERROR_COUNT.labels(
            method=method,
            endpoint=endpoint,
            error_type=error_type
        ).inc()

        self.logger.error(
            f"API Error - Method: {method}, Endpoint: {endpoint}, "
            f"Error Type: {error_type}"
        )