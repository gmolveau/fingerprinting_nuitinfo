import geoip2.database
import os
import pygeoip
from flask import render_template, jsonify, request
from hashlib import sha256
from ua_parser import user_agent_parser
from . import api
from .. import db
from ..models.user import User


def hash_data(word):
    '''
    Take a string and return his sha256 hash
    '''
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

    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    language = request.headers.get('Accept-Language').split(";")[0]
    ip = request.remote_addr
    provider = get_provider_from_ip(ip)
    browser = user_agent['user_agent']['family'] + " " + user_agent['user_agent']['major']
    os_client = user_agent['os']['family']
    os_client_version = user_agent['os']['major']
    # {'username': 'test', 'password': 'test', 'phone': '601060791', 'email': 'a@a', 'size_screen': '800x1280', 'lat': 48.849919799999995, 'long': 2.6370411}
    all_information = data.get('phone','') + data.get('email','') + data.get('size_screen','') + str(data.get('lat','')) + str(data.get('long',''))
    country = "" # get country from IP or lat/long

    return "200"


@api.route('/login/custom' , methods=['GET'])
def login_custom_get():
    return render_template('login_custom.html')


@api.route('/login/custom' , methods=['POST'])
def login_custom_post():
    #print(os_version)
    print(str(language) + " " + str(os_client) + " " + str(os_client_version) + " " + str(navigateur) + " " + ip + " Country -> "+ country+" AS -> "+ asn)
    return "parsing et pourcentage"


@api.route('/register' , methods=['GET'])
def register_get():
    return render_template('register.html')


@api.route('/register' , methods=['POST'])
def register_post():
    data = request.get_json()

    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    language = request.headers.get('Accept-Language').split(";")[0]
    ip = request.remote_addr
    provider = get_provider_from_ip(ip)
    browser = user_agent['user_agent']['family'] + " " + user_agent['user_agent']['major']
    os_client = user_agent['os']['family']
    os_client_version = user_agent['os']['major']
    # {'username': 'test', 'password': 'test', 'phone': '601060791', 'email': 'a@a', 'size_screen': '800x1280', 'lat': 48.849919799999995, 'long': 2.6370411}
    all_information = data.get('phone','') + data.get('email','') + data.get('size_screen','') + str(data.get('lat','')) + str(data.get('long',''))
    country = "" # get country from IP or lat/long

    user = User()
    user.username = data.get('username','')
    user.password = data.get('password','')
    user.phone = data.get('phone','')
    user.email = data.get('email','')
    user.hash_global = hash_data(all_information)
    user.hash_language = hash_data(language)
    user.hash_gps = hash_data(country)
    user.hash_size_screen = hash_data(data.get('size_screen',''))
    user.hash_os = hash_data(os_client)
    user.hash_provider = hash_data(provider)
    user.hash_os_version = hash_data(os_client_version)
    user.hash_browser = hash_data(browser)

    # Server put in database
    db.session.add(user)
    db.session.commit()

    return "200"
