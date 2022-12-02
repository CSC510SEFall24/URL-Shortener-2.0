from operator import and_
from flask import Blueprint, jsonify               #import dependancies
from flask_cors import cross_origin
from string import ascii_letters, digits
from flask import request
from random import choice
try:
    from ..models.links import Link, db, load_link
    from ..models.user import User, login_required2
    from ..models.engagements import Engagements
except ImportError:
    from models.links import Link, db, load_link
    from models.user import User, login_required2
    from models.engagements import Engagements

links_bp = Blueprint(
    'links_bp', __name__
)

@links_bp.route('/links/<id>', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getlink(id):
    '''This method is called when we want to fetch a single link, we pass user_id'''
    try:
        link = Link.query.get(id)
        return jsonify(
            link = link.to_json(),
            message = 'Fetched link successfully',
            status = 200
        ), 200
    except Exception as e:
        return jsonify(
            message = f"An error occurred: {e}",
            status = 400
        ), 400
        
@links_bp.route('/links/stub/<stub>', methods = ['GET'])
@cross_origin(supports_credentials=True)
def get_link_by_stub(stub):
    '''This method is called when we want to fetch a single link, we pass user_id'''
    try:
        link = db.session.query(Link).filter(Link.stub==stub).first()
        return jsonify(
            link = link.to_json(),
            message = 'Fetched link successfully',
            status = 200
        ), 200
    except Exception as e:
        return jsonify(
            message = f"An error occurred: {e}",
            status = 400
        ), 400

@links_bp.route('/links/all', methods = ['GET'])
@login_required2()
@cross_origin(supports_credentials=True)
def getalllinks():
    '''This method is called when we want to fetch all of the links of a particular user. Here, we check if the user is authenticated, 
    if yes show all the decks made by the user.'''
    args = request.args
    user_id = args and args['user_id']
    try:
        links = db.session.query(Link).join(User).filter(User.id==user_id).all()    
        return jsonify(
            links = links,
            message = 'Fetching links successfully',
            status = 200
        ), 200
    except Exception as e:
        return jsonify(
            message = f"An error occurred {e}",
            status = 400
        ), 400

def create_shortlink():
    CHARS = ascii_letters + digits
    stub = "".join(choice(CHARS) for _ in range(10))
    
    return stub


@links_bp.route('/links/create', methods = ['POST'])
@login_required2()
@cross_origin(supports_credentials=True)
def create():
    '''This method is routed when the user requests to create a new link.'''
    args = request.args
    user_id = args and args['user_id']
    try:
        data = request.get_json()
        long_url=data['long_url']
        stub=create_shortlink()
        title=data.get('title')
        disabled=data.get('disabled')
        utm_source=data.get('utm_source')
        utm_medium=data.get('utm_medium')
        utm_campaign=data.get('utm_campaign')
        utm_term=data.get('utm_term')
        utm_content=data.get('utm_content')
        password_hash=data.get('password_hash') 
        expire_on=data.get('expire_on')

        link = Link(user_id=user_id, stub=stub, long_url=long_url, title=title, disabled=disabled, utm_source=utm_source, utm_medium=utm_medium,utm_campaign=utm_campaign, utm_term=utm_term, utm_content=utm_content, password_hash=password_hash, expire_on=expire_on)
        link.user_id = user_id
        db.session.add(link)
        db.session.commit()

        return jsonify(
            link = link.to_json(),
            message = 'Create Link Successful',
            status = 201
        ), 201
    except Exception as e:
        return jsonify(
            message = f'Create Link Failed {e}',
            status = 400
        ), 400

@links_bp.route('/links/update/<id>', methods = ['PATCH'])
@login_required2()
@cross_origin(supports_credentials=True)
def update(id):
    '''This method is called when the user requests to update the link.'''
    try:
        request_data = request.get_json()
        data = {k: v for k, v in request_data.items() if v is not None}
        long_url=data['long_url']
        stub=data.get('stub')
        title=data.get('title')
        disabled=data.get('disabled')
        utm_source=data.get('utm_source')
        utm_medium=data.get('utm_medium')
        utm_campaign=data.get('utm_campaign')
        utm_term=data.get('utm_term')
        utm_content=data.get('utm_content')
        password_hash=data.get('password_hash') 
        expire_on=data.get('expire_on')

        link = load_link(id)
        if 'stub' in data:
            link.stub=stub
        if 'long_url' in data:
            link.long_url=long_url 
        if 'title' in data:
            link.title=title
        if 'disabled' in data:
            link.disabled=disabled
        if 'utm_source' in data:
            link.utm_source=utm_source
        if 'utm_medium' in data:
            link.utm_medium=utm_medium
        if 'utm_campaign' in data:
            link.utm_campaign=utm_campaign
        if 'utm_content' in data:
            link.utm_content=utm_content
        if 'utm_term' in data:
            link.utm_term=utm_term
        if 'password_hash' in data:
            link.password_hash=password_hash
        if 'expire_on' in data:
            link.expire_on=expire_on
        # db.session.query(Link).filter_by(id=id).update(stub=stub,long_url=long_url, title=title, disabled=disabled, utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign, utm_content=utm_content, utm_term=utm_term, password_hash=password_hash, expire_on=expire_on)
        # db.session.update()
        db.session.commit()

        return jsonify(
            link = link.to_json(),
            message = 'Update Link Successful',
            status = 201
        ), 201
    except Exception as e:
        return jsonify(
            message = f'Update Link Failed {e}',
            status = 400
        ), 400

@links_bp.route('/links/delete/<id>', methods = ['DELETE'])
@login_required2()
@cross_origin(supports_credentials=True)
def delete(id):
    '''This method is called when the user requests to delete the link. Only the link id is required to delete the deck.'''
    try:
        db.session.query(Link).filter_by(id=id).delete()
        db.session.commit()
        return jsonify(
            message = 'Delete link Successful',
            status = 200
        ), 200
    except Exception as e:
        return jsonify(
            message = f'Delete link Failed {e}',
            status = 400
        ), 400
    
    
@shorten_links_bp.route('/links/engagements', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getlinksengagement():
    '''This method is called when we want to fetch the analytics of the links'''
    args = request.args
    user_id = args and args['user_id']
    try:
        if localId:
            all_links = db.session.query(Link).filter_by(user_id=localId).all()
            links = []
            for link in all_links:
                links.append(link.stub)
                links.append(link.utm_source)
                links.append(link.utm_medium) 
                links.append(link.utm_campaign)
                links.append(link.utm_term)
                links.append(link.utm_content)
                links.append(link.created_on)
                
            return jsonify(
                links = links,
                message = 'Fetching Analytics data successfully',
                status = 200
            ), 200
        else:
             return jsonify(
                links = "",
                message = 'Please login to see analytics data',
                status = 200
            ), 200
    except Exception as e:
        return jsonify(
            decks = [],
            message = f"Fetching Analytics data failed {e}",
            status = 400
        ), 400

@shorten_links_bp.route('/links/engagements/<id>', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getsinglelinkengagements():
    '''This method is routed when the user requests analytics for a single link.'''
    try:
        data = request.get_json()
        stub =data['id']

        Analytics_data = db.session.query(Link).filter_by(stub=stub).all()
        ana_data=[]
        for ad in Analytics_data:
                ana_data.append(ad.stub)
                ana_data.append(ad.utm_source)
                ana_data.append(ad.utm_medium) 
                ana_data.append(ad.utm_campaign)
                ana_data.append(ad.utm_term)
                ana_data.append(ad.utm_content)
                ana_data.append(ad.created_on)
        

        return jsonify(
           ad=ana_data,
                message = 'Fetching Analytics data successfully',
                status = 200
            ), 200
    except Exception as e:
        return jsonify(
            message = f'Fetching Analytics failed {e}',
            status = 400
        ), 400

