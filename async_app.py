import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from Utils.settings import Settings
from Application.orchestrator import main


def initialize_logging():
    logging_path = Settings().getLoggingPath()
    if not os.path.exists(logging_path):
        os.mkdir(logging_path)
        print("{} created".format(logging_path))
    filename = os.path.join(logging_path, "log.txt")
    logging.basicConfig(handlers=[RotatingFileHandler(filename, maxBytes=1000000, backupCount=10)],
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Start application')


if __name__ == "__main__":
    initialize_logging()
    # TEST
    from Comm.Messages.NMEA_RMC_message import RMCMessage
    test=RMCMessage(b'$GPRMC,161335.00,A,5210.28418,N,00423.99276,E,0.432,,271026,,,A*71')
    print(f"{test.location=}")
    print(f"{test.fix_datetime=}")
    print(f"{test.has_fix=}")
    print(f"{test.speed_knots=}")

    # The entry point to start the async loop
    asyncio.run(main())
