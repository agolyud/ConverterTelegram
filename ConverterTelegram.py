import os
import shutil
import asyncio
from telethon.sessions import SQLiteSession, StringSession
from telethon import TelegramClient
from opentele.tl import TelegramClient as TC
from opentele.api import UseCurrentSession


TDATAS_DIR = "./res_tdatas/"
CONVERT_SESSION = "./sessions_to_tdata/"


def clear():
    try:
        shutil.rmtree(TDATAS_DIR)
    except OSError:
        for file in os.listdir(TDATAS_DIR):
            os.remove(file)
    os.mkdir(TDATAS_DIR)


class TData:
    def __init__(self, path: str = "./sessions_to_tdata/") -> None:
        self.path = path

    async def session_to_tdata(self, session_path: str) -> None:
        await self._session_to_tdata(session_path)

    async def _session_to_tdata(self, session_path: str) -> None:
        client = TC(os.path.join(self.path, session_path))
        tdesk = await client.ToTDesktop(flag=UseCurrentSession)

        tdata_dir = os.path.join(TDATAS_DIR, "tdata")
        if not os.path.exists(tdata_dir):
            os.mkdir(tdata_dir)

        try:
            tdesk.SaveTData(tdata_dir)
        except TypeError:
            pass

        await client.disconnect()


async def SessionToTData():
    tdata = TData()
    session_files = [f for f in os.listdir(CONVERT_SESSION) if f.endswith(".session")]

    if not session_files:
        print("No session files found in the directory.")
        return
    elif len(session_files) > 1:
        print("Multiple session files found. Please leave only one file in the directory.")
        return

    session_file = session_files[0]
    await tdata.session_to_tdata(session_path=session_file)

# Convert session to string session
async def convert_session_to_string(session_file_path: str, api_id: int, api_hash: str):
    session = SQLiteSession(session_file_path)

    async with TelegramClient(session, api_id, api_hash) as client:
        string_session = StringSession.save(client.session)
        return string_session


async def main():
    await SessionToTData()

    print("Successfully converted to tdata.")
    print("Insert tdata into Telegram and log in.")

    input("Press Enter when you've completed the action...")

    api_id = input("Enter your API ID (https://my.telegram.org): ")
    api_hash = input("Enter your API Hash (https://my.telegram.org): ")

    session_dir = "./sessions_to_tdata/"
    session_files = [f for f in os.listdir(session_dir) if f.endswith(".session")]

    if len(session_files) == 0:
        print("No session files found in the directory.")
        return
    elif len(session_files) > 1:
        print("Multiple session files found. Please leave only one file in the directory.")
        return

    session_file_path = os.path.join(session_dir, session_files[0])
    string_session = await convert_session_to_string(session_file_path, api_id, api_hash)

    print(f"String Session: {string_session}")

if __name__ == "__main__":
    asyncio.run(main())
