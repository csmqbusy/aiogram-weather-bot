import logging
import structlog
from structlog.typing import EventDict


def add_callsite(_, __, event_dict: EventDict) -> EventDict:
    filename: str = event_dict.pop("filename")
    func_name: str = event_dict.pop("func_name")
    lineno: str = event_dict.pop("lineno")
    event_dict["logger"] = f"{filename}:{func_name}:{lineno}"
    return event_dict


def setup_logger(
        loglevel=logging.INFO,
        *,
        event_width=50,
) -> None:

    def format_message(_, __, event_dict: EventDict) -> EventDict:
        message = event_dict.get("event", "")
        formatted_message = message.ljust(event_width)
        event_dict["event"] = formatted_message
        return event_dict

    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        add_callsite,
        format_message,
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(loglevel)


if __name__ == '__main__':
    setup_logger(logging.INFO, event_width=60)

    default_logger = logging.getLogger()
    default_logger.debug("Hello privet!")
    default_logger.info("Hello privet!")
    logger = structlog.get_logger()
    logger.info("This is an info messagemessagemessagemessage")
