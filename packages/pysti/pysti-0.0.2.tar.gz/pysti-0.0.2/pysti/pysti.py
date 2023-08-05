#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 00:02:41 2020

@author: joachim
"""
from typing import List, Dict
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
MODE = os.getenv('MODE')

if MODE == 'development' or MODE == 'testing': 
    headers = {'access_token':os.getenv('LOCAL_KEY')}
    url_target = 'http://localhost:8000'
else:
    headers = {'access_token':os.getenv('API_KEY')}
    url_target = 'https://rensti-api-backend.herokuapp.com'

print(f'running pysti in {MODE} mode. url target is {url_target}')

def request(target: str, payload = {}, method = 'get', headers = {}):
    """
    Parameters
    ----------
    target : str
        Endpoint to hit.
    payload : dict
        JSON object to post.

    Returns
    -------
    Request response object.
    """

    headers['Content-Type'] = 'text/html; charset=utf-8'
    r = requests.request(method = method, url = f'{url_target}/{target}', json = payload, headers = headers)
    return r

def create_source(tag: str, source_string: str, headers = {}):
    """
    Parameters
    ----------
    source_string : str
        the str representaton of a bibtex file.

    Returns
    -------
    Request reponse object.
    """
    
    payload = {'tag': tag, 'source': source_string}
    r = request('sources/', payload = payload, method = 'post', headers = headers)
    
    return r

def get_source(tag: str, headers = {}):
    """
    Parameters
    ----------
    tag : str
        tag of source to get.

    Returns
    -------
    Returns a dict representing the responsee object.
    """
    
    r = request(f'sources/{tag}', method = 'get', headers = headers)
    return json.loads(r.text)


def get_item(item: str, headers = {}) -> Dict[str, str]:
    """
    Parameters
    ----------
    item : str
        title of item to get from rensti api.
    headers : dict, optional
        Headers for passing api-keys. The default is {}.

    Returns
    -------
    Dict[str, str]
        Returns a dict representing the response object.
    """

    r = request(method = 'get', target = f'items/{item}', headers=headers)
    return json.loads(r.text)

def get_items(headers = {}) -> List[Dict[str, str]]:
    """
    Parameters
    ----------
    headers : TYPE, optional
        Headers for passing api-keys. The default is {}.

    Returns
    -------
    List[Dict[str, str]]
        List of dictionaries representing the item objects.
    """

    r = request(method = 'get', target = f'items/', headers=headers)
    return r.json()

def create_item(item: Dict[str, str], headers = {}):
    """
    Parameters
    ----------
    item : dict
        dict representing json object to add.
    headers : dict, optional
        Headers for passing api-keys. The default is {}.

    Returns
    -------
    Dict[str, str]
        Returns a dict representing the response object.
    """

    r = request(payload = item, method = 'post', target = 'items', headers = headers)
    return json.loads(r.text)

def update_item(item: Dict[str, str], item_to_update: str, headers = {}) -> Dict[str, str]:
    """
    Parameters
    ----------
    item : Dict[str, str]
        dict representing json object to add.
    item_to_update : str
        the item that gets updated with values from item
    headers : TYPE, optional
        Headers for passing api-keys. The default is {}.

    Creates a put request to rensti api which updates a given item entry (matched on title) to whatever body is passed. 

    Returns
    -------
    Dict[str, str]
        Returns a dict representing the updated item.
    """

    r = request(payload = item, method = 'put', target = f'items/{item_to_update}', headers = headers)
    return json.loads(r.text)

def get_sources(headers = {}): 
    """
    Parameters
    ----------
    headers : TYPE, optional
        Headers for passing api-keys. The default is {}.

    Returns
    -------
    Returns a list sof dicts representing the response objects.
    """

    r = request(method = 'get', target = 'sources', headers = headers)
    return json.loads(r.text)

def carride(departure_lat: float, departure_long: float, destination_lat: float, destination_long: float, headers = {}) -> Dict[str, str]:
    body = {'departure_lat': departure_lat, 'departure_long': departure_long, 'destination_lat': destination_lat, 'destination_long': destination_long}
    r = request(target = f'services/carride', payload=body, method='post', headers=headers)
    return json.loads(r.text)
