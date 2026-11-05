import asyncio
import logging

from Application.model import Model
from Comm.Messages.NMEA_RMC_message import RMCMessage
from Comm.Messages.NMEA_VTG_message import VTGMessage
from Comm.Messages.nmea_message import NMEAMessage
from Comm.async_serialconnector import AsyncSerialConnector
from Utils.settings import Settings
from WebServer.web_server import start_server


class Processor:
    """
    Doen:
        RMC message uit elkaar halen
        Model maken met daarin of er een fix is
            en de posities opslaan met timestamp
        Maar eerst voor de test kijken of een VTG message compleet is
    """
    def __init__(self, rs422_connector: AsyncSerialConnector):
        self.rs422_connector = rs422_connector
        self.model = Model()

    @staticmethod
    async def proc_rs422_line(line_bytes: bytes) -> None:
        print(f"Received RS422 Message: {line_bytes}")
        logging.debug(f"Received RS422 Message: {line_bytes}")

    async def proc_gps_line(self, line_bytes: bytes) -> None:
        logging.debug(f"proc_gps_line: {line_bytes}")
        # if NMEAMessage(line_bytes).sentence_id() == VTGMessage.SENTENCE_ID:
        #     await self.rs422_connector.write_message(line_bytes)
        #     logging.debug(f"wrote {line_bytes}, {NMEAMessage(line_bytes).is_consistent()}")
        if NMEAMessage(line_bytes).sentence_id() == RMCMessage.SENTENCE_ID:
            logging.debug(f"Processing RMC: {line_bytes}")
            rmc_msg = RMCMessage(line_bytes)
            if rmc_msg.has_fix:
                self.model.set_fix(rmc_msg.fix_datetime)
                speed = rmc_msg.speed_knots
                vtg_msg = VTGMessage.from_speed(speed)
                sentence = vtg_msg.msg.sentence
                await self.rs422_connector.write_message(sentence)
                logging.debug(f"Wrote {sentence}")


async def main() -> None:
    # Load parameters from your config.ini / settings.py configuration files
    gps_connector = AsyncSerialConnector(port=Settings().getSerialPort("GPS"), baudrate=Settings().getBaudrate("GPS"))
    rs422_connector = AsyncSerialConnector(port=Settings().getSerialPort("RS422"), baudrate=Settings().getBaudrate("RS422"))

    try:
        await gps_connector.connect()
        await rs422_connector.connect()
        processor = Processor(rs422_connector)

        await start_server()

        reading_task = asyncio.create_task(rs422_connector.read_messages(processor.proc_rs422_line))
        writing_task = asyncio.create_task(gps_connector.read_messages(processor.proc_gps_line))

        # Keep the app active or run your concurrent tasks here (e.g., UI loop)
        while True:
            await asyncio.sleep(3600)  # Keep running indefinitely

    except asyncio.exceptions.CancelledError:
        print("Stopping application...")
    finally:
        await gps_connector.close()
        await rs422_connector.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped manually.")

# app = web.Application()
# app.add_routes([web.get('/', handle),
#                 web.get('/{name}', handle)])
