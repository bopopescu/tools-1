#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: ingestion_client.py
# Author: xiaoh
# Mail: xiaoh@about.me 
# Created Time:  2016-02-01 15:10:05
#############################################

import click, requests, json
import uuid, random, os, sys
from plumbum.cmd import wc

@click.group()
def cli():
    pass

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def create(host, port, user, auth_token, db, table, version):
    """
        Create ingestion service for upload data
    """
    _get_request(host, port, user, auth_token, db, table, version, "create")

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def start(host, port, user, auth_token, db, table, version):
    """
        Start ingestion service for upload data
    """
    _get_request(host, port, user, auth_token, db, table, version, "start")

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def stop(host, port, user, auth_token, db, table, version):
    """
        Stop ingestion service
    """
    _get_request(host, port, user, auth_token, db, table, version, "stop")

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def restart(host, port, user, auth_token, db, table, version):
    """
        Restart ingestion service
    """
    _get_request(host, port, user, auth_token, db, table, version, "restart")

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def status(host, port, user, auth_token, db, table, version):
    """
        Get status of ingestion service
    """
    _get_request(host, port, user, auth_token, db, table, version, "status")

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def token(host, port, user, auth_token, version):
    """
        Modify user token
    """
    _set_token(host, port, user, auth_token, version)

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('--times', default=1, help='Times for upload data')
@click.option('-l', '--lines', default=1, help='Lines of upload data per time')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def post(host, port, user, auth_token, db, table, times, lines, version):
    """
        Post random data to server(Production Environment)
    """
    _post(host, port, user, auth_token, db, table, times, lines, version)

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', required=True, help='Port of data center')
@click.option('-l', '--lines', default=1, help='Lines of upload data per time')
def ingestion(host, port, lines):
    """
        post random data directly to ingestion server
    """
    url = "http://%s:%s" % (host, port)
    data = _get_random_data(lines)
    post_data = []
    for body in data:
        post_data.append({"body":json.dumps(body)})
    r = requests.post(url, data=json.dumps(post_data))
    click.echo(r.status_code)
    click.echo(r.content)
    if r.ok:
        click.echo(r.text)

@cli.command()
@click.option('-h', '--host', required=True, help='Host of data center')
@click.option('-p', '--port', default=8000, help='Port of data center [default:8000]')
@click.option('-u', '--user', required=True, help='User of data center')
@click.option('-a', '--auth_token', required=True, help='Token of user')
@click.option('-d', '--db', required=True, help='Database name')
@click.option('-t', '--table', required=True, help='Table name')
@click.option('-f', '--filename', required=True, help='File path saving json data')
@click.option('-l', '--lines', default=1, type=click.IntRange(1, 100), help='Lines of upload data per time')
@click.option('-v', '--version', default='v1', help='RestAPI version Default:[v1]')
def postfile(host, port, user, auth_token, db, table, filename, lines, version):
    """
        post data reading from file to server
    """
    if not os.path.isfile(filename):
        click.echo('[ERROR] Filename not exist')
        return

    headers = {'X-USERNAME':user, 'X-AUTH-TOKEN':auth_token}
    url = "http://%s:%s/%s/%s/%s" % (host, port, version, db, table)

    total_lines = wc['-l', filename]().split()[0]
    over_lines = 0
    post_data = []
    for data in open(filename):
        js = json.loads(data)
        js['tags']= js['tags'][0] if len(js['tags']) else ''
        post_data.append(js)
        if len(post_data) == lines:
            over_lines = over_lines + lines
            r = requests.post(url, data=json.dumps(post_data), headers=headers)
            if r.status_code != 200:
                click.echo("Invalid response from server")
                return
            click.echo('Post %s/%s lines data to ingestion Server' % (over_lines, total_lines))
            post_data = []

    if len(post_data) > 0:
        over_lines = over_lines + len(post_data)
        requests.post(url, data=json.dumps(post_data), headers=headers)
        click.echo('Post %s/%s lines data to ingestion Server' % (over_lines,total_lines))

    click.echo("All data post to ingestion server")


def _post(host, port, user, auth_token, db, table, times, lines, version):
    headers = {'X-USERNAME':user, 'X-AUTH-TOKEN':auth_token}
    url = "http://%s:%s/%s/%s/%s" % (host, port, version, db, table)
    r = None
    for time in xrange(times):
        data = _get_random_data(lines)
        r = requests.post(url, data=json.dumps(data), headers=headers)

        if times % max(1,times/5) == 0:
            print r.text

def _get_random_data(lines):
    data = []
    for i in xrange(lines):
        data.append({'name':uuid.uuid1().get_hex()[2:8], 'age':random.randint(0,200)})
    return data

def _set_token(host, port, user, auth_token, version):
    headers = {'content-type':'application/json'}
    data = {'username':user, 'token':auth_token}
    url = "http://%s:%s/%s/api/token" % (host, port, version)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print "Response Status:%s" % r.status_code
    if r.ok:
        print r.json()

def _get_request(host, port, user, auth_token, db, table, version, action):
    headers = {"X-USERNAME":user, "X-AUTH-TOKEN":auth_token}
    url = "http://%s:%s/%s/api/%s/%s/%s" % (host, port, version, db, table, action)
    r = requests.get(url, headers=headers)
    print "Response Status:%s" % r.status_code
    if r.ok:
        print r.json()

if __name__ == "__main__":
    cli()

