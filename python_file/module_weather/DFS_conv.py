import math
# LCC DFS 좌표변환을 위한 기초 자료
NX = 149            ## X축 격자점 수
NY = 253            ## Y축 격자점 수

Re = 6371.00877     ##  지구 반경 (km)
grid = 5.0          ##  격자 간격 (km)
slat1 = 30.0        ##  표준위도 1 / 투영 위도1(degree)
slat2 = 60.0        ##  표준위도 2 / 투영 위도2(degree)
olon = 126.0        ##  기준점 경도(degree)
olat = 38.0         ##  기준점 위도(degree)
xo = 210 / grid     ##  기준점 X좌표(GRID)
yo = 675 / grid     ##  기준점 Y좌표(GRID)
first = 0

# LCC DFS 좌표변환 ( code : "toXY"(위경도->좌표, v1:위도, v2:경도), "toLL"(좌표->위경도,v1:x, v2:y) )



if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI


    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1

#위경도 > 좌표 변환
def mapToGrid(lat, lon, code = 0 ):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

# 좌표 > 위경도 변환
def gridToMap(x, y, code = 1):
    x = x - 1
    y = y - 1
    xn = x - xo
    yn = ro - y + yo
    ra = math.sqrt(xn * xn + yn * yn)
    if sn < 0.0 :
        ra = -ra
    alat = math.pow((re * sf / ra), (1.0 / sn))
    alat = 2.0 * math.atan(alat) - PI * 0.5
    if math.fabs(xn) <= 0.0 :
        theta = 0.0
    else :
        if math.fabs(yn) <= 0.0 :
            theta = PI * 0.5
            if xn < 0.0 :
                theta = -theta
        else :
            theta = math.atan2(xn, yn)
    alon = theta / sn + olon
    lat = alat * RADDEG
    lon = alon * RADDEG

    return lat, lon

print(mapToGrid(37.579871128849334, 126.98935225645432))
print(mapToGrid(35.101148844565955, 129.02478725562108))
print(mapToGrid(33.500946412305076, 126.54663058817043))
### result :
#(60, 127)
#(97, 74)
#(53, 38)

print(gridToMap(60, 127))
print(gridToMap(97, 74))
print(gridToMap(53, 38))
### result
# 37.579871128849334, 126.98935225645432
# 35.101148844565955, 129.02478725562108
# 33.500946412305076, 126.54663058817043

# https://gist.github.com/fronteer-kr/14d7f779d52a21ac2f16?permalink_comment_id=2785533
# github url : https://gist.github.com/fronteer-kr/14d7f779d52a21ac2f16
# 소스출처 : http://www.kma.go.kr/weather/forecast/digital_forecast.jsp  내부에 있음

# (사용 예)
# var rs = dfs_xy_conv("toLL","60","127");
# console.log(rs.lat, rs.lng);