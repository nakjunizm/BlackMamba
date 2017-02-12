
import time
import datetime
import pytz
import numpy
import random
import sys
import argparse
from faker import Faker


faker = Faker()
log_lines = 20
f = open('./backend/access.log', 'a+')

otime = datetime.datetime.now()

response=["200","404","500","301"]
verb=["GET","POST","DELETE","PUT"]
resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]
ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

flag = True
while (flag):
    increment = datetime.timedelta(seconds=random.randint(30,300))
    otime += increment
    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%z')
    vrb = numpy.random.choice(verb, p=[0.6, 0.1, 0.1, 0.2])
    uri = random.choice(resources)
    if uri.find("apps") > 0:
        uri += repr(random.randint(1000, 10000))

    resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = numpy.random.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05] )()
    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s\n' % (ip,dt,tz,vrb,uri,resp,byt))

    log_lines -= 1
    flag = False if log_lines == 0 else True
