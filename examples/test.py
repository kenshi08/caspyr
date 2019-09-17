from caspyr import Session, User, Region
from caspyr import CloudAccount, CloudAccountvSphere, CloudAccountNSXT
from caspyr import CloudZone, ImageMapping, FlavorMapping
from caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from caspyr import Project, Request, Deployment, Blueprint, Machine, DataCollector
import requests
import argparse
import json
import time
import os

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        required=True,
                        action='store'
    )
    args = parser.parse_args()
    return args

def get_datacollector(session):
    return DataCollector.list(session)[0]

def get_nsxt(session):
    return CloudAccountNSXT.list(session)[0]

def setup_org(session):
    dc = get_datacollector(session)
    i = CloudAccountNSXT.create(session,
                                name = 'nsxmgr-01a.corp.local',
                                fqdn = 'nsxmgr-01a.corp.local',
                                rdc = dc['id'],
                                username = 'admin',
                                password = 'VMware1!VMware1!'
                               )
    print(i.name)
    print(i.id)
    cloudaccounts = []
    cloudaccounts.append(i.id)
    vsphere = CloudAccountvSphere.create(session,
                                   name = 'Trading vSphere',
                                   fqdn = 'vcsa-01a.corp.local',
                                   rdc = dc['id'],
                                   username = 'administrator@corp.local',
                                   password = 'VMware1!',
                                   datacenter_moid = 'Datacenter:datacenter-21',
                                   nsx_cloud_account= cloudaccounts
                                  )

def main():
    args = getargs()
    session = Session.login(args.token)

    setup_org(session)

if __name__ == '__main__':
    main()