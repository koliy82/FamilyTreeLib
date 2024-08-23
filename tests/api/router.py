from fastapi import APIRouter
from starlette.responses import PlainTextResponse, StreamingResponse

from familytreelib import TreeLib, GraphvizLib, IgraphLib
from tests.mongo import mongomock_client

router = APIRouter(
    prefix="/tree",
    tags=["tree"]
)

client = mongomock_client()
braks = client.db.braks

@router.get("/text/{user_id}")
async def family_tree(user_id: int, reverse: bool = True, kid_prefix = '👼 ', kid_suffix = '', partner_prefix = '🫂 ', partner_suffix = '', root_prefix = '', root_suffix = '❤️‍🔥', max_duplicate: int = 0):
    tree = TreeLib(user_id=user_id, kid_prefix=kid_prefix, kid_suffix=kid_suffix, partner_prefix=partner_prefix, partner_suffix=partner_suffix, root_prefix=root_prefix, root_suffix=root_suffix, max_duplicate=max_duplicate)
    tree.build_tree(braks)
    formatted_tree = tree.tree.show(stdout=False, reverse=reverse)
    return PlainTextResponse(formatted_tree)

@router.get("/image_graphviz/{user_id}", responses={404: {"description": "Family tree not found"}})
async def family_tree(user_id: int, kid_prefix = '', kid_suffix = '', partner_prefix = '', partner_suffix = '', root_prefix = '', root_suffix = '', max_duplicate: int = 1):
    tree = GraphvizLib(user_id, kid_prefix=kid_prefix, kid_suffix=kid_suffix, partner_prefix=partner_prefix, partner_suffix=partner_suffix, root_prefix=root_prefix, root_suffix=root_suffix, max_duplicate=max_duplicate)
    tree.build_tree(braks)
    image_stream = tree.render()
    return StreamingResponse(image_stream, media_type="image/png")

@router.get("/image_igraph/{user_id}", responses={404: {"description": "Family tree not found"}})
async def family_tree(user_id: int, kid_prefix = '', kid_suffix = '', partner_prefix = '', partner_suffix = '', root_prefix = '', root_suffix = '', max_duplicate: int = 0):
    tree = IgraphLib(user_id, kid_prefix=kid_prefix, kid_suffix=kid_suffix, partner_prefix=partner_prefix, partner_suffix=partner_suffix, root_prefix=root_prefix, root_suffix=root_suffix, max_duplicate=max_duplicate)
    tree.build_tree(braks)
    image_stream = tree.render()
    return StreamingResponse(image_stream, media_type="image/png")