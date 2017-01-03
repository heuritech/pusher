#!/usr/bin/python3

from prometheus_client import CollectorRegistry, Gauge, Counter, pushadd_to_gateway
from prometheus_client.parser import text_string_to_metric_families
from operator import itemgetter
import argparse
import requests

def prometheus_get(addr_gateway, name_metrics, job, data=None):
    addr = addr_gateway + "/metrics"
    if "http://" not in addr:
        addr = "http://" + addr
    if data == None:
        data=requests.get(addr).content.decode()
    if data != None:
        for family in text_string_to_metric_families(data):
            for sample in family.samples:
                if sample[0] == name_metrics and job in sample[1]["job"]:
                    return sample[2], data
    else:
        print("Error with getting %s" % addr)
    return 0, data

def prometheus_push(addr_gateway, name_job, registry):
    pushadd_to_gateway(addr_gateway, job=name_job, registry=registry)

def prometheus_add(name_metric, dict_labels, registry=None, value=None):
    if registry == None:
        registry = CollectorRegistry()
    keys = dict_labels.keys()
    if len(keys) > 0:
        g = Gauge(name_metric, name_metric, dict_labels.keys(), registry=registry)
        if value is not None:
            g.set(value)
        else:
            g.labels(**dict_labels).set_to_current_time()
    else:
        g = Gauge(name_metric, name_metric, registry=registry)
        if value is not None:
            g.set(value)
        else:
            g.set_to_current_time()
    return registry

def main():
    parser = argparse.ArgumentParser(description='Send a crawling notification')
    parser.add_argument('--addr-gateway', '-a', type=str,
                        help='addr push gateway', required=True)
    parser.add_argument('--name-metric', '-n', type=str,
                        help='name metrics', required=True)
    parser.add_argument('--name-job', '-N', type=str,
                        help='name metrics', required=True)
    parser.add_argument('--source', '-s', default=None, type=str)
    parser.add_argument('--block', '-b', default=None, type=str)
    parser.add_argument('--family', '-f', default=None, type=str)
    parser.add_argument('--add', '-A', default=None, type=int)
    parser.add_argument('--set', '-S', default=None, type=int)
    
    args = parser.parse_args()
    dict_labels = {
        "source": args.source,
        "block": args.block,
        "family": args.family
    }
    dict_labels = {k: v for k, v in dict_labels.items() if v}
    value = args.set
    if args.add is not None:
        value , _ = prometheus_get(args.addr_gateway, args.name_metric, args.name_job)
        value += args.add
    registry=prometheus_add(args.name_metric, dict_labels, value=value)
    prometheus_push(args.addr_gateway, args.name_job, registry)

if __name__ == "__main__":
    main()