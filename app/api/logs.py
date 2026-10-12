import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.auth.dependencies import require_role
from app.services.log_service import add_log, get_logs, latest_log_id, wait_for_logs


router = APIRouter(
    prefix="/api/admin/logs",
    tags=["Admin Logs"],
    dependencies=[Depends(require_role("ADMIN"))],
)


@router.get("")
def list_logs(limit: int = Query(default=100, ge=1, le=500)):
    return {
        "items": get_logs(limit),
        "count": len(get_logs(limit)),
    }


@router.get("/stream")
async def stream_logs() -> StreamingResponse:
    async def event_generator() -> AsyncIterator[str]:
        last_id = latest_log_id()

        yield "retry: 3000\n\n"

        while True:
            await asyncio.to_thread(wait_for_logs, 15.0)
            entries = get_logs(500)

            # Send only entries newer than the last delivered record.
            if last_id is not None:
                entries.reverse()
                newer = []
                found_last = False

                for entry in entries:
                    if entry["id"] == last_id:
                        found_last = True
                        continue
                    if found_last:
                        newer.append(entry)

                if found_last:
                    entries = newer
                else:
                    entries = [
                        entry for entry in entries
                        if entry["id"] != last_id
                    ]
            else:
                entries.reverse()

            for entry in entries:
                last_id = entry["id"]
                yield f"id: {last_id}\ndata: {json.dumps(entry, ensure_ascii=False)}\n\n"

            if not entries:
                yield ": keep-alive\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/test-event")
def create_test_event():
    entry = add_log(
        "Admin tarafından test olayı oluşturuldu.",
        level="INFO",
        source="admin-log-test",
    )
    return {"message": "Test logu oluşturuldu.", "item": entry}
