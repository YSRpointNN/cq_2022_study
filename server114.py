import socket
import time

SRESULTS = str()

PDLSERVER_LIST = {'10.66.0.1':'BN01',
'10.66.8.1':'BN02',
'10.66.16.1':'BN03',
'10.66.24.1':'BN04',
'10.66.32.1':'BN05',
'10.66.72.1':'BN10',
'10.66.80.1':'BN11',
'10.66.88.1':'BN12',
'10.66.96.1':'BN13',
'10.66.112.1':'BN15',
'10.66.120.1':'BN16',
'10.66.232.1':'BN18',
'10.66.208.1':'BN20',
'10.66.192.1':'BN23',
'10.66.168.1':'BN26',
'10.64.96.11':'F1-SMT-BL',
'10.64.64.1':'F2-SMT-BL',
'10.64.64.11':'F2-SMT-BL',
'10.64.0.1':'F2-F10-DL1',
'10.64.0.11':'F2-F10-DL1',
'10.64.8.1':'F2-F09-DL1',
'10.65.8.1':'F2-F09-OQC',
'10.65.32.1':'F1-F09-OQC',
'10.64.48.1':'F1-F13-DL1'}

def GetNowTime():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())

def SocketRequest(host):
    warntim = 0
    retry = True
    while retry:
        try:
            retry = False
            ROMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ROMserver.settimeout(5)
            ROMserver.connect((host, 6650))
        except ConnectionRefusedError:
            retry = True
            ROMserver.close()
            time.sleep(0.5)
            warntim += 1
            if warntim >= 20:
                retry = False
                return f'{GetNowTime()}:ERROR[1001]---PDLserver-side lost'
        except:
            ROMserver.close()
            retry = False
            return f'{GetNowTime()}:ERROR[1002]---Unknow connect fail'
    try:
        ROMserver.send(b'ready')
        sizeof = int(ROMserver.recv(1024).decode('ascii'))
        ROMserver.send(b'go')
        PDLdata_local = str()
        for i in range(0, (sizeof // 1024) + 1):
            buffer = ROMserver.recv(1024).decode('utf-8')
            PDLdata_local += buffer
        return PDLdata_local
    except socket.timeout:
        return f'{GetNowTime()}:ERROR[1003]---recv timeout'
    finally:
        ROMserver.close()

def email_send(html_txt):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    ##
    pass
    ##

#----------------------------------------start----------------------------------------#
html_egg = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style>
        span{font-family:"Microsoft YaHei",Arial;font-size:16px;}
        .title{background-color:#407a9f;color:#fff;text-align:center;font-size:25px;font-family:"Microsoft YaHei",Arial;
                width: auto;
                padding: 5px;}
        table{border-collapse:collapse;width: 100%;font-size: 13px;font-family: "Microsoft YaHei",Arial;}
        table td{border: gray 2px solid;
                width: 15%;
                background-color: #82de82;
                color: #fff;
                text-align:center;
            }
        table .line{width: 10%;background-color: #dec782;}
        table .normal{width: 70%;background-color: #ffffff;color: gray;text-align:left;}
        table .warnin{width: 70%;background-color: #ffffff;color: red;text-align:left;}
    </style>
    <title>Test</title>
</head>

<body>
    <div class="title"><h3>產綫Server自動巡檢(DELL)</h3></div>
    <br>
    <table border="1">
'''
for PDLip_txt in PDLSERVER_LIST:
    PDLstate_txt = SocketRequest(PDLip_txt)
    print(PDLstate_txt)
    if '----All system OK !' in PDLstate_txt:
        html_egg += f'''<tr>
            <td>{PDLip_txt}</td>
            <td class="line">{PDLSERVER_LIST[PDLip_txt]}</td>
            <td class="normal">正常</td>
        </tr>'''
    elif ':ERROR[' in PDLip_txt:
        html_egg += f'''<tr>
            <td>{PDLip_txt}</td>
            <td class="line">{PDLSERVER_LIST[PDLip_txt]}</td>
            <td class="warnin">{PDLstate_txt}</td>
        </tr>'''
    else:
        warn_buffer = PDLstate_txt.replace('\n','<br>')
        html_egg += f'''<tr>
            <td>{PDLip_txt}</td>
            <td class="line">{PDLSERVER_LIST[PDLip_txt]}</td>
            <td class="warnin">{warn_buffer}</td>
        </tr>'''
html_egg += '</table>'

html_egg += '''<span>以下服務器還需手動巡檢：<br>10.66.64.1<br>
        10.66.64.1<br>
        10.66.104.1<br>
        10.66.128.1<br>
        10.66.248.1<br>
        10.66.200.1<br>
        10.66.240.1<br>
        10.66.216.1<br>
        10.66.136.1<br>
        10.66.184.1<br>
        10.66.176.1<br>
        10.64.96.1<br>
        10.64.8.11<br>
        10.65.56.1<br>
        10.64.40.1<br>
        10.65.40.1<br>
        10.64.32.1<br>
        10.65.16.1<br>
    </span>

</body>
</html>'''
email_send(html_egg)
