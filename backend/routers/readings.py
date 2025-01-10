from fastapi import APIRouter

router = APIRouter()

router.get("/")
async def list_readings():
    return None

router.post("/")
async def post_reading():
    return None

router.delete("/{date}")
async def delete_reading():
    return None

router.put("/{date}")
async def put_reading():
    return None
