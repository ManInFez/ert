import asyncio
from asyncio.queues import Queue
import websockets
from ert_shared.ensemble_evaluator.ws_util import wait_for_ws
import queue
import logging
import threading
from cloudevents.http import from_json
from cloudevents.http.event import CloudEvent
from cloudevents.http import to_json
import ert_shared.ensemble_evaluator.entity.identifiers as identifiers
import uuid


logger = logging.getLogger(__name__)


class _Monitor:
    def __init__(self, host, port):
        self._base_uri = f"ws://{host}:{port}"
        self._client_uri = f"{self._base_uri}/client"

        self._loop = asyncio.new_event_loop()
        self._incoming = asyncio.Queue(loop=self._loop)
        self._receive_future = None
        self._id = str(uuid.uuid1()).split("-")[0]

    def get_base_uri(self):
        return self._base_uri

    def _send_event(self, cloud_event):
        async def _send():
            async with websockets.connect(self._client_uri) as websocket:
                message = to_json(cloud_event)
                await websocket.send(message)

        # TODO: if run was never called, the monitor's loop is not running.
        # Improve this, or not? But this will fail if run _was_ called, and it
        # is attempted to exit_server after the fact.
        # See https://github.com/equinor/ert/issues/1227
        if self._loop.is_running():
            asyncio.run_coroutine_threadsafe(_send(), self._loop).result()
        else:
            self._loop.run_until_complete(_send())

    def signal_cancel(self):
        logger.debug(f"monitor-{self._id} asking server to cancel...")

        out_cloudevent = CloudEvent(
            {
                "type": identifiers.EVTYPE_EE_USER_CANCEL,
                "source": "/ert/monitor/{self._id}",
                "id": str(uuid.uuid1()),
            }
        )
        self._send_event(out_cloudevent)
        logger.debug(f"monitor-{self._id} asked server to cancel")

    def signal_done(self):
        logger.debug(f"monitor-{self._id} informing server monitor is done...")

        out_cloudevent = CloudEvent(
            {
                "type": identifiers.EVTYPE_EE_USER_DONE,
                "source": "/ert/monitor/{self._id}",
                "id": str(uuid.uuid1()),
            }
        )
        self._send_event(out_cloudevent)
        logger.debug(f"monitor-{self._id} informing server monitor is done...")

    async def _receive(self):
        logger.debug(f"monitor-{self._id} starting receive")
        async with websockets.connect(
            self._client_uri, max_size=2 ** 26, max_queue=500
        ) as websocket:
            async for message in websocket:
                event = from_json(message)
                self._incoming.put_nowait(event)
                if event["type"] == identifiers.EVTYPE_EE_TERMINATED:
                    logger.debug(f"monitor-{self._id} client received terminated")
                    break

        logger.debug(f"monitor-{self._id} disconnected")

    def _run(self, done_future):
        asyncio.set_event_loop(self._loop)
        self._receive_future = self._loop.create_task(self._receive())
        try:
            self._loop.run_until_complete(self._receive_future)
        except asyncio.CancelledError:
            logger.debug(f"monitor-{self._id} receive cancelled")
        self._loop.run_until_complete(done_future)

    def track(self):
        wait_for_ws(self._base_uri)

        done_future = asyncio.Future(loop=self._loop)

        thread = threading.Thread(
            name=f"ert_monitor-{self._id}_loop", target=self._run, args=(done_future,)
        )
        thread.start()

        event = None
        try:
            while event is None or event["type"] != identifiers.EVTYPE_EE_TERMINATED:
                event = asyncio.run_coroutine_threadsafe(
                    self._incoming.get(), self._loop
                ).result()
                yield event
            self._loop.call_soon_threadsafe(done_future.set_result, None)
        except GeneratorExit:
            logger.debug(f"monitor-{self._id} generator exit")
            self._loop.call_soon_threadsafe(self._receive_future.cancel)
            if not done_future.done():
                self._loop.call_soon_threadsafe(done_future.set_result, None)
        thread.join()


def create(host, port):
    return _Monitor(host, port)
