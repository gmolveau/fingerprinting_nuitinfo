from flask import render_template, jsonify, request
from . import api
from ua_parser import user_agent_parser
import geoip2.database
import os
import pygeoip
from hashlib import sha256


def hash_data(word):
    '''
    Take a string and return his sha256 hash
    '''
    return hashlib.sha256(word.encode('utf-8')).hexdigest()

@api.route('/')
def index():
    return render_template('login.html')


@api.route('/login' , methods=['POST'])
def home():
    """
    Les versions récupérées sont des versions "majeur"

    langue : language -> fr-FR,fr
    OS : os_client -> Mac OS X
    OS VERSION : os_client_version -> 10
    Navigateur : navigateur -> Chrome 70
    Ip : ip

    """
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    language = request.headers.get('Accept-Language').split(";")[0]
    ip = request.remote_addr

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    
    reader = geoip2.database.Reader(os.path.join(SITE_ROOT, '../../geo_ip_db/', "GeoLite2-City.mmdb" ))

    #reader = geoip2.database.Reader('../../geo_ip_db/GeoLite2-City_20181204/GeoLite2-City.mmdb')
    response = reader.city(ip)
    country = response.country.iso_code
    db_asn = os.path.join(SITE_ROOT, '../../geo_ip_db/', "GeoIPASNum.dat" )
    ai = pygeoip.GeoIP(db_asn, pygeoip.MEMORY_CACHE)
    asn = ai.org_by_addr(ip)

    navigateur = user_agent['user_agent']['family'] + " " + user_agent['user_agent']['major']

    os_client = user_agent['os']['family']

    os_client_version = user_agent['os']['major']


    #print(os_version)
    print(str(language) + " " + str(os_client) + " " + str(os_client_version) + " " + str(navigateur) + " " + ip + " Country -> "+ country+" AS -> "+ asn)

    return render_template('login.html')

