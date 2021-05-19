from http import HTTPStatus

from aiohttp import web
from aiohttp_session import get_session


async def update_session(request, session):
    if request is not None and request.user is not None:
        session['user_id'] = request.user.get('_id', None)


async def is_authorized(request):
    session = await get_session(request)
    await update_session(request, session)
    return 'user_id' in session and session['user_id'] is not None
