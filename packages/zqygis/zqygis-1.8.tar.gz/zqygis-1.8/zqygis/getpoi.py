import requests, random, json
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        利用高德geocoding服务解析地址获取位置坐标
        :param address:需要解析的地址
        :return:
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        geocoding = urllib.urlencode(geocoding)
        ret = urllib.urlopen("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lng = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lng, lat]
            else:
                return None
        else:
            return None


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def jiexiloc(s):
	#转坐标系
	lng, lat = s.split(',')
	lng, lat = gcj02_to_wgs84(float(lng), float(lat))
	lng = round(lng, 10)
	lat = round(lat, 10)
	return (str(lng), str(lat))

def requestone(url, lkey):
	url = url + '&key={}'.format(random.sample(lkey,1)[0])
	headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
	while 1:
		try:
			data = requests.get(url, timeout=1, headers=headers)
			data = data.text
			data = json.loads(data)
			if data['info'] == 'OK':
				break
			elif data['info'] == 'DAILY_QUERY_OVER_LIMIT':
				print('OVER_LIMIT')
				return 'OVER_LIMIT'
			else:
				print('poi解析错误')
				print(data['info'])
		except:
			print('网络不稳定')
	return data

def jiexidata(data):
	#解析json数据
	out = ''
	for poi in data['pois']:
		loc = jiexiloc(poi['location'])
		lng = loc[0]
		lat = loc[1]
		rating = poi['biz_ext']['rating']
		cost = poi['biz_ext']['cost']
		name = poi['name']
		address = poi.get('address', 'null')
		pname = poi['pname']
		cityname = poi['cityname']
		adname = poi['adname']
		type = poi['type']
		typecode = poi['typecode']
		list_output = [name, address, type, typecode, pname, cityname, adname, lng, lat, rating, cost]
		list_output = [str(x).replace(',',';') for x in list_output]
		out = out + '\t'.join(list_output) + '\n'
	return out

def write_columns(pathout):
	list_output = ['name', 'address', 'type', 'typecode', 'pname', 'cityname', 'adname', 'lng', 'lat', 'rating', 'cost']
	with open(pathout, 'w') as o:
		out = '\t'.join(list_output) + '\n'
		o.write(out)
		
def output(out, pathout):
	write_columns(pathout)
	with open(pathout, 'a') as o:
		o.write(out)

def check_last(data, page):
	count = data['count']
	if page * 20 >= int(count):
		return True
	else:
		return False

def getadocde(adcode, lkey):
	url = 'https://restapi.amap.com/v3/config/district?keywords=%s' % adcode
	data = requestone(url, lkey)
	l = data['districts'][0]['districts']
	ladcode = [x['adcode'] for x in l]
	return ladcode


def getpoi_adcode(adcode, lkey, keywords, pathout, out=False):
	s_output = ''
	page = 1
	while 1:
		url = 'https://restapi.amap.com/v3/place/text?keywords=%s&city=%s&page=%s' % (keywords, adcode, page)
		data = requestone(url, lkey)
		out2 = jiexidata(data)
		s_output += out2
		if check_last(data, page):
			break
		#exit()
		page += 1
	print('%s completed %s' % (adcode,keywords))
	if out:
		print(1)
		write_columns(pathout)
		output(s_output, pathout)
	return s_output

def getpoi_citycode(adcode, lkey, keywords, pathout, out=False):
	s_output = ''
	ladcode = getadocde(adcode, lkey)
	for adcode in ladcode:
		out2 = getpoi_adcode(adcode, lkey, keywords, pathout)
		s_output += out2
	if out:
		print(2)
		write_columns(pathout)
		output(s_output, pathout)
	return s_output

def getpoi_pcode(adcode, lkey, keywords, pathout, out=False):
	s_output = ''
	ladcode = getadocde(adcode, lkey)
	for adcode in ladcode:
		out2 = getpoi_citycode(adcode, lkey, keywords, pathout)
		s_output += out2
	if out:
		print(3)
		write_columns(pathout)
		output(s_output, pathout)
	return s_output


if __name__ == "__main__":
	adcode = '360000'
	keywords = '全季酒店'
	lkey = ['6d1a2b3523de345a6593c76eac6a4ff2']
	pathout = r"C:\Users\25223\Desktop\out.txt"
	#a = getpoi_pcode(adcode, lkey, keywords, pathout)
	getpoi_pcode(adcode, lkey, keywords, pathout, out=True)
	#with open(pathout, 'w') as o:
		#o.write(a)


