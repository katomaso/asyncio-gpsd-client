"""
Test on raw gpsd output.

To generate your testing data use `gpspipe -w -n 20`
"""
from gpsd_client_async import messages

def test_parse():
    with open("test/gpsd.log") as log:
        for line in log:
            print(messages.parse(line))


def test_parse_version():
    version_message = messages.parse('{"class":"VERSION","release":"3.24","rev":"3.24","proto_major":3,"proto_minor":15}')
    assert isinstance(version_message, messages.Version) 

def test_parse_devices():
    version_devices = messages.parse('{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/QWS.EG25.NMEA","driver":"NMEA0183","activated":"2025-12-17T12:10:32.016Z","flags":1,"native":0,"bps":9600,"parity":"N","stopbits":1,"cycle":1.00}]}')
    assert isinstance(version_devices, messages.Devices) 

def test_parse_watch():
    version_watch = messages.parse('{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}')
    assert isinstance(version_watch, messages.Watch) 

def test_parse_device():
    version_device = messages.parse('{"class":"DEVICE","path":"/dev/dtmux/0/ubl0","driver":"u-blox","activated":"2025-04-07T10:37:19.631Z","native":1,"bps":38400,"parity":"N","stopbits":1,"cycle":1.00,"mincycle":0.02}')
    assert isinstance(version_device, messages.Device) 

def test_parse_tpv_empty():
    version_tpv = messages.parse('{"class":"TPV","device":"/dev/QWS.EG25.NMEA","mode":1}')
    assert isinstance(version_tpv, messages.TPV) 

def test_parse_tpv():
    version_tpv = messages.parse('{"class":"TPV","device":"/dev/QWS.EG25.NMEA","mode":3,"time":"2025-12-17T12:10:33.000Z","ept":0.005,"lat":50.074039100,"lon":14.466591817,"altHAE":302.3000,"altMSL":257.3000,"alt":257.3000,"epv":13.800,"track":320.5000,"magtrack":319.2000,"magvar":1.3,"speed":0.000,"climb":0.000,"epc":27.60,"geoidSep":45.000,"eph":9.500,"sep":15.200}')
    assert isinstance(version_tpv, messages.TPV) 

def test_parse_sky():
    version_sky = messages.parse('{"class":"SKY","device":"/dev/dtmux/0/ubl0","gdop":10.58,"hdop":3.89,"pdop":8.91,"tdop":5.71,"vdop":8.02}')
    assert isinstance(version_sky, messages.Sky) 

def test_parse_sky_long():
    version_sky = messages.parse('{"class":"SKY","device":"/dev/QWS.EG25.NMEA","nSat":10,"uSat":0,"satellites":[{"PRN":1,"el":0.0,"az":0.0,"ss":0.0,"used":false,"gnssid":0,"svid":1},{"PRN":2,"el":0.0,"az":0.0,"ss":0.0,"used":false,"gnssid":0,"svid":2},{"PRN":3,"el":0.0,"az":0.0,"ss":0.0,"used":false,"gnssid":0,"svid":3},{"PRN":6,"el":16.0,"az":92.0,"ss":0.0,"used":false,"gnssid":0,"svid":6},{"PRN":10,"el":4.0,"az":278.0,"ss":0.0,"used":false,"gnssid":0,"svid":10},{"PRN":11,"el":3.0,"az":130.0,"ss":0.0,"used":false,"gnssid":0,"svid":11},{"PRN":12,"el":67.0,"az":258.0,"ss":0.0,"used":false,"gnssid":0,"svid":12},{"PRN":13,"el":0.0,"az":0.0,"ss":0.0,"used":false,"gnssid":0,"svid":13},{"PRN":14,"el":0.0,"az":0.0,"ss":0.0,"used":false,"gnssid":0,"svid":14},{"PRN":15,"el":8.0,"az":185.0,"ss":0.0,"used":false,"gnssid":0,"svid":15}]}')
    assert isinstance(version_sky, messages.Sky) 
