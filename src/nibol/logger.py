import structlog
import logging
import sys
import json
from enum import Enum
from typing import Optional, Literal, Union
from datetime import datetime, timezone

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# GCP Severity mappings
SEVERITY_MAPPING = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
}


class LoggerType(str, Enum):
    """Available logger types."""

    NONE = "none"
    JSON = "json"
    GCP = "gcp"


class HTTPXFilter(logging.Filter):
    """Filter out HTTPX logs unless they're errors."""

    def filter(self, record):
        return not (record.name.startswith("httpx") and record.levelno < logging.WARNING)


class JSONRenderer:
    """Simple JSON renderer for structured logging."""

    def __call__(self, logger, name: str, event_dict: dict) -> str:
        return json.dumps(event_dict)


class GCPRenderer:
    """Custom renderer for Google Cloud Logging format."""

    def __call__(self, logger, name: str, event_dict: dict) -> str:
        """
        Format the log entry according to GCP structured logging specs.
        https://cloud.google.com/logging/docs/structured-logging
        """
        timestamp = event_dict.pop("timestamp", f"{datetime.now(timezone.utc).isoformat()}Z")
        level = event_dict.pop("level", "INFO")

        gcp_entry = {
            "timestamp": timestamp,
            "severity": SEVERITY_MAPPING.get(level.upper(), "DEFAULT"),
            "message": event_dict.pop("event", ""),
        }

        # Opcional: añadir campos de localización (archivo, línea, función)
        if "code_location" in event_dict:
            gcp_entry["sourceLocation"] = {
                "file": event_dict.pop("code_file", ""),
                "line": event_dict.pop("code_line", ""),
                "function": event_dict.pop("code_func", ""),
            }

        # Añadir resto de campos en jsonPayload
        if event_dict:
            gcp_entry["jsonPayload"] = event_dict

        return json.dumps(gcp_entry)


def get_renderer(logger_type: LoggerType):
    """
    Devuelve el renderer apropiado en función del logger_type.
    """
    renderer_map = {
        LoggerType.GCP: GCPRenderer(),
        LoggerType.JSON: JSONRenderer(),
    }
    # Si no está en el mapa, usar por defecto structlog.processors.JSONRenderer
    return renderer_map.get(logger_type, structlog.processors.JSONRenderer())


def setup_logger(
    logger_type: Union[LoggerType, str] = LoggerType.JSON,
    level: LogLevel = "INFO",
    service_name: str = "nibol-client",
    project_id: Optional[str] = None,
    filter_http_logs: bool = True,
) -> Optional[structlog.BoundLogger]:
    """
    Configura el logger con Structlog y retorna la instancia.

    Args:
        logger_type: Tipo de logger a usar ('none', 'json', 'gcp').
        level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        service_name: Nombre del servicio para log.
        project_id: ID opcional del proyecto (usado en GCP).
        filter_http_logs: Filtra logs de HTTPX por debajo de WARNING.

    Returns:
        Configured logger instance or None if logger_type is 'none'.
    """
    # Acepta logger_type como string
    if isinstance(logger_type, str):
        logger_type = LoggerType(logger_type.lower())

    # Si logger_type es NONE, no configuramos nada
    if logger_type == LoggerType.NONE:
        return None

    # Nivel de log
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Handler a stdout
    console_handler = logging.StreamHandler(sys.stdout)
    if filter_http_logs:
        console_handler.addFilter(HTTPXFilter())

    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Limpiar handlers previos y usar el nuevo
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Filtrar logs HTTPX y httpcore
    if filter_http_logs:
        for http_logger in ("httpx", "httpcore"):
            logging.getLogger(http_logger).setLevel(logging.WARNING)

    # Contexto común para todos los logs
    base_context = {"service": service_name}
    if project_id:
        base_context["project_id"] = project_id

    # Procesadores de structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        get_renderer(logger_type),
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(**base_context)


def set_log_level(level: LogLevel) -> None:
    """
    Cambia dinámicamente el nivel de log.

    Args:
        level: Nuevo nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logging.getLogger().setLevel(getattr(logging, level.upper()))
