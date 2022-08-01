import asyncio
import threading
from monitoring import start_sheet_monitoring, start_delivery_monitoring


loop = asyncio.get_event_loop()
sheet_thread = threading.Thread(target=start_sheet_monitoring)
sheet_thread.start()
loop.run_until_complete(start_delivery_monitoring())
