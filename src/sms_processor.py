"""
Base example of a service processor within the child image
"""
from rococo.config import BaseConfig
from rococo.messaging import BaseServiceProcessor

from rococo.sms.factory import sms_factory

from logger import Logger
import rollbar

import logging
logging.getLogger("pika").setLevel(logging.WARNING)


class SmsServiceProcessor(BaseServiceProcessor):
    """
    Service processor that sends SMS messages
    """
    sms_service = None

    def __init__(self):
        super().__init__()
        config = BaseConfig()

        self.logger = Logger().get_logger()
        
        # Initialize Rollbar for error and exception logs
        rollbar_token = config.get_env_var('ROLLBAR_ACCESS_TOKEN') or config.get_env_var('ROLLBAR_SECRET')
        rollbar_env = config.get_env_var('APP_ENV') or 'unknown'
        
        if rollbar_token:
            rollbar.init(
                rollbar_token,
                environment=rollbar_env,
                handler='blocking'
            )
            
            # Add Rollbar handler to logger
            rollbar_handler = logging.Handler()
            rollbar_handler.setLevel(logging.ERROR)
            
            class RollbarHandler(logging.Handler):
                def emit(self, record):
                    try:
                        if record.exc_info:
                            rollbar.report_exc_info(record.exc_info)
                        else:
                            rollbar.report_message(self.format(record), level=record.levelname.lower())
                    except Exception:
                        self.handleError(record)
            
            rollbar_handler = RollbarHandler()
            rollbar_handler.setLevel(logging.ERROR)
            self.logger.addHandler(rollbar_handler)
        else:
            self.logger.warning("Rollbar token not found. Error tracking disabled.")

        if config.get_env_var("SMS_PROVIDER").lower() == "twilio":
            self.logger.info("Twilio Account SID : %s",config.get_env_var("TWILIO_ACCOUNT_SID"))
            if config.get_env_var("TWILIO_ACCOUNT_SID") in [None, "", False]:
                raise ValueError("TWILIO_ACCOUNT_SID cant be empty")
            if config.get_env_var("TWILIO_AUTH_TOKEN") in [None,"",False]:
                raise ValueError("TWILIO_AUTH_TOKEN cant be empty")
        self.sms_service = sms_factory.get(**config.get_env_vars())

        assert self.sms_service is not None


    def process(self, message):
        self.logger.info("Received message: %s to the service processor image", message)
        try:
            event_name = message['event']
            event_parameters = message['parameters']
            recipient_phone_number = message['to']
            response = self.sms_service.send_sms(
                event_name,
                recipient_phone_number,
                event_parameters
            )
            self.logger.debug(f"Processing result: {response}")
        except Exception as e:
            self.logger.exception("Failed to process message", e)
