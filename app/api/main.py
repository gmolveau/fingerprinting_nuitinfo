import geoip2.database
import os
import pygeoip
from flask import render_template, jsonify, request, abort
from hashlib import sha256
from ua_parser import user_agent_parser
from . import api
from .. import db
from ..models.user import User


def get_final_weight(user,language,country,size_screen,os,provider,os_version,browser):
    weight = 0
    if user.language != language:
        weight += 25
    if user.country != country:
        weight += 20
    if user.size_screen != size_screen:
        weight += 15
    if user.os != os:
        weight += 15
    if user.provider != provider:
        weight += 10
    if user.os_version != os_version:
        weight += 10
    if user.browser != browser:
        weight += 5
    return weight

def verify_login_data(data):
    if data.get('username','') == '':
        return False
    if data.get('password','') == '':
        return False
    if data.get('size_screen','') == '':
        return False
    if data.get('lat','') == '':
        return False
    if data.get('long','') == '':
        return False
    return True

def verify_register_data(data):
    if data.get('username','') == '':
        return False
    if data.get('password','') == '':
        return False
    if data.get('phone','') == '':
        return False
    if data.get('email','') == '':
        return False
    if data.get('size_screen','') == '':
        return False
    if data.get('lat','') == '':
        return False
    if data.get('long','') == '':
        return False
    return True


def get_hash_global(language, country, size_screen, os_client, provider, os_version, browser, phone):
    return hash_data(
        language + country + size_screen + os_client + provider + os_version + browser + phone
    )


def hash_data(word):
    return sha256(word.encode('utf-8')).hexdigest()


def get_provider_from_ip(ip):
    if ip != "127.0.0.1":
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        reader = geoip2.database.Reader(os.path.join(SITE_ROOT, '../../geo_ip_db/', "GeoLite2-City.mmdb" ))
        response = reader.city(ip)
        db_asn = os.path.join(SITE_ROOT, '../../geo_ip_db/', "GeoIPASNum.dat" )
        ai = pygeoip.GeoIP(db_asn, pygeoip.MEMORY_CACHE)
        return ai.org_by_addr(ip)
    else:
        return "localhost"


@api.route('/')
def index():
    return render_template('index.html')


@api.route('/login' , methods=['GET'])
def login_get():
    return render_template('login.html')


@api.route('/login' , methods=['POST'])
def login_post():
    data = request.get_json()
    if not verify_login_data(data):
        abort(409)

    username = data.get('username','')
    password = data.get('password','')

    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)

    if not user.verify_password(password):
        abort(400)

    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    language = request.headers.get('Accept-Language').split(";")[0]
    ip = request.remote_addr
    provider = get_provider_from_ip(ip)
    browser = user_agent['user_agent']['family'] + " " + user_agent['user_agent']['major']
    os_client = user_agent['os']['family']
    os_client_version = user_agent['os']['major']
    country = "FR" # get country from IP or lat/long
    size_screen = data.get('size_screen')

    hash_global = get_hash_global(
        language,
        country,
        size_screen,
        os_client,
        provider,
        os_client_version,
        browser,
        user.phone
    )
    if hash_global == user.hash_global:
        return render_template('login_custom.html',
            username = username,
            language=language,
            country=country,
            size_screen=size_screen, 
            os=os_client,
            provider=provider,
            os_version=os_client_version,
            browser=browser
        )

    final_weight = get_final_weight(
        user,
        language,
        country,
        size_screen,
        os_client,
        provider,
        os_client_version,
        browser
    )
    if final_weight >= 60 :
        abort(403)
    if final_weight >= 30 :
        return "SMS validation required"

    user.language = language
    user.country = country
    user.size_screen = size_screen
    user.os = os_client
    user.provider = provider
    user.os_version = os_client_version
    user.browser = browser

    db.session.add(user)
    db.session.commit()

    return render_template('login_custom.html',
            username = username,
            language=language,
            country=country,
            size_screen=size_screen, 
            os=os_client,
            provider=provider,
            os_version=os_client_version,
            browser=browser
        )


@api.route('/login/custom' , methods=['POST'])
def login_custom_post():
    data = request.get_json()
    username= data.get('username')
    language = data.get('language')
    size_screen = data.get('size_screen')
    country = data.get('country')
    os_client = data.get('os')
    provider = data.get('provider')
    os_client_version = data.get('os_version')
    browser = data.get('browser')

    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)

    hash_global = get_hash_global(
        language,
        country,
        size_screen,
        os_client,
        provider,
        os_client_version,
        browser,
        user.phone
    )
    if hash_global == user.hash_global:
        return "success"

    final_weight = get_final_weight(
        user,
        language,
        country,
        size_screen,
        os_client,
        provider,
        os_client_version,
        browser
    )
    return str(final_weight)


@api.route('/register' , methods=['GET'])
def register_get():
    return render_template('register.html')


@api.route('/register' , methods=['POST'])
def register_post():
    data = request.get_json()
    if not verify_register_data(data):
        abort(400)
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    language = request.headers.get('Accept-Language').split(";")[0]
    ip = request.remote_addr
    provider = get_provider_from_ip(ip)
    browser = user_agent['user_agent']['family'] + " " + user_agent['user_agent']['major']
    os_client = user_agent['os']['family']
    os_client_version = user_agent['os']['major']
    country = "FR" # TODO : get country from IP or lat/long

    hash_global = get_hash_global(
        language,
        country,
        data.get('size_screen'),
        os_client,
        provider,
        os_client_version,
        browser,
        data.get('phone')
    )    

    user = User()
    user.username = data.get('username')
    user.set_password(data.get('password'))
    user.phone = data.get('phone')
    user.email = data.get('email')
    user.hash_global = hash_global
    user.language = language
    user.country = country
    user.size_screen = data.get('size_screen')
    user.os = os_client
    user.provider = provider
    user.os_version = os_client_version
    user.browser = browser

    # Server put in database
    db.session.add(user)
    db.session.commit()

    return "success"
