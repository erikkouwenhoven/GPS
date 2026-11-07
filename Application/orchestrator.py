import asyncio
import logging

from Application.model import Model
from Comm.Messages.NMEA_GGA_message import GGAMessage
from Comm.Messages.NMEA_RMC_message import RMCMessage
from Comm.Messages.NMEA_VTG_message import VTGMessage
from Comm.Messages.nmea_message import NMEAMessage
from Comm.async_serialconnector import AsyncSerialConnector
from Utils.settings import Settings
from WebServer.web_server import WebServer


class Processor:
    """
    Doen:
        RMC message uit elkaar halen
        Model maken met daarin of er een fix is
            en de posities opslaan met timestamp
        Maar eerst voor de test kijken of een VTG message compleet is
    """
    def __init__(self, rs422_connector: AsyncSerialConnector, model: Model):
        self.rs422_connector = rs422_connector
        self.model = model

    @staticmethod
    async def proc_rs422_line(line_bytes: bytes) -> None:
        print(f"Received RS422 Message: {line_bytes}")
        logging.debug(f"Received RS422 Message: {line_bytes}")

    async def proc_gps_line(self, line_bytes: bytes) -> None:
        logging.debug(f"proc_gps_line: {line_bytes}")
        sentence_id = NMEAMessage(line_bytes).sentence_id()
        if sentence_id == RMCMessage.SENTENCE_ID:
            logging.debug(f"Processing RMC: {line_bytes}")
            rmc_msg = RMCMessage(line_bytes)
            if rmc_msg.has_fix:
                self.model.set_fix_datetime(rmc_msg.fix_datetime)
                speed = rmc_msg.speed_knots
                location = rmc_msg.location
                self.model.set_reading(speed, location)
                vtg_msg = VTGMessage.from_speed(speed)
                sentence = vtg_msg.msg.sentence
                await self.rs422_connector.write_message(sentence)
                logging.debug(f"Wrote {sentence}")
        elif sentence_id == GGAMessage.SENTENCE_ID:
            logging.debug(f"Processing GGA: {line_bytes}")
            gga_msg = GGAMessage(line_bytes)
            if gga_msg.has_fix:
                self.model.set_num_satellites(gga_msg.num_satellites)
                self.model.set_height(gga_msg.height)
                self.model.set_height_unit(gga_msg.height_unit)
                self.model.set_hor_dilution(gga_msg.hor_dilution)


async def main() -> None:
    model = Model()
    # Load parameters from your config.ini / settings.py configuration files
    gps_connector = AsyncSerialConnector(port=Settings().getSerialPort("GPS"), baudrate=Settings().getBaudrate("GPS"))
    rs422_connector = AsyncSerialConnector(port=Settings().getSerialPort("RS422"), baudrate=Settings().getBaudrate("RS422"))
    web_server = WebServer(model)

    try:
        await gps_connector.connect()
        await rs422_connector.connect()
        processor = Processor(rs422_connector, model)

        await web_server.start_server()

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
        await web_server.stop_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped manually.")
