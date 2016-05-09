# F - Jan, G - Feb, H - Mar, J - Apr, K - May, M - Jun
# N - Jul, Q - Aug, U - Sep, V - Oct, W - Nov, Z - Dec
#
import Quandl, os, itertools, sys
import logging, datetime
sys.path.append("..")
import pandas as pd
from memo import *

@memo                                    
def get_quandl_auth():
    fname = '%s/.quandl' % os.environ['HOME']
    if not os.path.isfile(fname):
        print 'Please create a %s file ' % fname
        exit()
    auth = open(fname).read()
    return auth

def web_download(contract,start,end):
    df = Quandl.get(contract,trim_start=start,trim_end=end,
                    returns="pandas",authtoken=get_quandl_auth())
    return df

def systemtoday():
    return datetime.datetime.today()

def download_data(downloader=web_download, today=systemtoday):

    years = range(1984,2022)
    months = ['F', 'G', 'H', 'J', 'K', 'M',
              'N', 'Q', 'U', 'V', 'W', 'Z']
    futcsv = pd.read_csv("../data/futures.csv")
    instruments = zip(futcsv.Symbol,futcsv.Market)

    start="1980-01-01"; end="2016-05-09"
    print today()
    for year in years:
        for month in months:
            for (sym,market) in instruments:
                contract = "%s/%s%s%d" % (market,sym,month,year)
                try:
                    print contract
                    df = downloader(contract,start,end)
                    print df.head()
                    print df.columns
                except Quandl.Quandl.DatasetNotFound:
                    print "No dataset"
                exit()

                
if __name__ == "__main__":
    
    f = '%(asctime)-15s: %(message)s'
    if len(sys.argv) == 3:
        logging.basicConfig(filename='%s/futures-%d.log' % (os.environ['TEMP'],int(sys.argv[1])),level=logging.DEBUG,format=f)        
        download_data(int(sys.argv[1]),int(sys.argv[2]))
    else:
        logging.basicConfig(filename='%s/futures.log' % os.environ['TEMP'],level=logging.DEBUG, format=f)
        download_data()
