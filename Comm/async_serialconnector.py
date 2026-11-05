import asyncio
import logging

import serial_asyncio
from serial.serialutil import SerialException


class AsyncSerialConnector:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.reader = None
        self.writer = None
        self.is_running = False

    async def connect(self):
        """Establishes an asynchronous connection to the serial port."""
        logging.debug(f"Connecting to {self.port} at {self.baudrate} baud...")
        # open_serial_connection creates an asyncio StreamReader and StreamWriter
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(
                url=self.port,
                baudrate=self.baudrate
            )
            self.is_running = True
            logging.debug(f"Connector: {self.reader}, {self.writer} connected successfully")
        except SerialException as e:
            logging.error(f"Error connecting to {self.port}: {e}")

    async def read_messages(self, message_callback):
        """Asynchronously reads data line-by-line and triggers a callback function."""
        while self.is_running:
            try:
                # Execution yields here until a complete NMEA sentence ending in \n arrives
                line_bytes = await self.reader.readline()
                if line_bytes:
                    await message_callback(line_bytes)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error reading serial data: {e}")
                await asyncio.sleep(1)  # Simple retry backoff

    async def write_message(self, line_bytes: bytes):
        """Asynchronously writes data line-by-line and triggers a callback function."""
        if self.is_running:
            try:
                # Execution yields here until a complete NMEA sentence ending in \n arrives
                self.writer.write(line_bytes)
                await self.writer.drain()
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error writing serial data: {e}")
                await asyncio.sleep(1)  # Simple retry backoff

    async def close(self):
        """Gracefully closes the connection."""
        self.is_running = False
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        print("Serial connection closed.")
