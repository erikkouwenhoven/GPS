import asyncio
import logging

from Comm.Messages.NMEA_VTG_message import VTGMessage
from Comm.Messages.nmea_message import NMEAMessage
from Comm.async_serialconnector import AsyncSerialConnector
from Utils.settings import Settings


class Processor:
    def __init__(self, rs422_connector: AsyncSerialConnector):
        self.rs422_connector = rs422_connector

    @staticmethod
    async def proc_rs422_line(line_bytes: bytes):
        print(f"Received RS422 Message: {line_bytes}")
        logging.debug(f"Received RS422 Message: {line_bytes}")

    async def proc_gps_line(self, line_bytes: bytes):
        print(f"proc_gps_line: {line_bytes}")
        if NMEAMessage(line_bytes).sentence_id() == VTGMessage.SENTENCE_ID:
            await self.rs422_connector.write_message(line_bytes)
            logging.debug(f"wrote {line_bytes}")


async def main():
    # Load parameters from your config.ini / settings.py configuration files
    gps_connector = AsyncSerialConnector(port=Settings().getSerialPort("GPS"), baudrate=Settings().getBaudrate("GPS"))
    rs422_connector = AsyncSerialConnector(port=Settings().getSerialPort("RS422"), baudrate=Settings().getBaudrate("RS422"))

    try:
        await gps_connector.connect()
        await rs422_connector.connect()

        processor = Processor(rs422_connector)

        reading_task = asyncio.create_task(rs422_connector.read_messages(processor.proc_rs422_line))
        writing_task = asyncio.create_task(gps_connector.read_messages(processor.proc_gps_line))

        # Keep the app active or run your concurrent tasks here (e.g., UI loop)
        while True:
            await asyncio.sleep(3600)  # Keep running indefinitely

    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        print("Stopping application...")
    finally:
        await gps_connector.close()
        await rs422_connector.close()


if __name__ == "__main__":
    # The entry point to start the async loop
    asyncio.run(main())
