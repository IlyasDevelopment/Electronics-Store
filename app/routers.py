from aws import get_link

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status
from fastapi_sqlalchemy import db

from helpers import make_pagination_links

from models import ItType, Item

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy import desc, func

from typing import Optional, Union


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request, page_num: int = 1, page_size: int = 9):

    items = db.session.query(Item)\
        .order_by(desc(Item.id))\
        .limit(page_size)\
        .offset((page_num-1)*page_size)

    items_len = db.session.query(Item.id).count()

    response = {
        "items": items,
        "pagination": {},
        "pages_amt": items_len // page_size + 1,
        "items_count": items_len,
        "action": "/"
    }

    make_pagination_links(response, page_num, page_size, items_len)

    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request,
                                          "response": response
                                      })


@router.get("/add")
def add_get(request: Request):
    return templates.TemplateResponse("create.html",
                                      {
                                          "request": request
                                      })


@router.post("/add")
def add_post(
        name: str = Form(...),
        it_type: ItType = Form(...),
        price: int = Form(...),
        photo: UploadFile = File(...),
):

    if photo.filename:
        photo_url = get_link(photo)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db_item = Item(
        name=name,
        it_type=it_type,
        price=price,
        photo_url=photo_url,
        )

    db.session.add(db_item)
    db.session.commit()

    url = router.url_path_for("home")

    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/update/{item_id}")
def update_get(request: Request, item_id: int):

    try:
        item = db.session.query(Item).filter(Item.id == item_id).one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse("update.html",
                                      {
                                          "request": request,
                                          "item": item,
                                      })


@router.post("/update/{item_id}")
def update_post(
        item_id: int,
        name: str = Form(...),
        it_type: ItType = Form(...),
        price: int = Form(...),
        photo: UploadFile = File(...),
):

    if photo.filename:
        photo_url = get_link(photo)
        db.session.query(Item).filter(Item.id == item_id).update(
            {
                "name": name,
                "it_type": it_type,
                "price": price,
                "photo_url": photo_url,
            }
        )
    else:
        db.session.query(Item).filter(Item.id == item_id).update(
            {
                "name": name,
                "it_type": it_type,
                "price": price,
            }
        )

    db.session.commit()

    url = router.url_path_for("home")

    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.post("/delete/{item_id}")
def delete(item_id: int):

    try:
        item = db.session.query(Item).filter(Item.id == item_id).one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.session.delete(item)
    db.session.commit()

    url = router.url_path_for("home")

    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/search")
def find_items(
        request: Request,
        name: Optional[str] = None,
        it_type: Optional[ItType] = None,
        min_price: Optional[Union[int, str]] = None,
        max_price: Optional[Union[int, str]] = None,
        page_num: int = 1,
        page_size: int = 9
        ):

    all_filters = []
    response = {
        "pagination": {},
        "action": "/search"
    }

    if name:
        all_filters.append(func.lower(Item.name).contains(name.lower()))
        response["wanted_name"] = name
    if min_price:
        all_filters.append(Item.price >= min_price)
        response["wanted_min_price"] = min_price
    if max_price:
        all_filters.append(Item.price <= max_price)
        response["wanted_max_price"] = max_price
    if it_type:
        all_filters.append(Item.it_type == it_type)
        response["wanted_type"] = it_type.name

    items = db.session.query(Item)\
        .filter(*all_filters)\
        .order_by(desc(Item.id))\
        .limit(page_size)\
        .offset((page_num-1)*page_size)

    items_len = db.session.query(Item).filter(*all_filters).count()

    response["items"] = items
    response["items_count"] = items_len
    response["pages_amt"] = items_len // page_size + 1

    make_pagination_links(response, page_num, page_size, items_len)

    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request,
                                          "response": response,
                                      })
