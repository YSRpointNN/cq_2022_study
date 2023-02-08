import socket
import time
import re
import os

SOCKET_TIMEOUT = 300
SYS_COMPONENT = ('Fans', 'Intrusion', 'Memory', 'Power Supplies', 'Power Management', 'Processors',
              'Temperatures', 'Voltages', 'Hardware Log', 'Batteries')


def GetSystemStatus():
    sys_status_txt_local = os.popen('omreport chassis').read()
    sys_status_dict_local = dict()
    for i in SYS_COMPONENT:
        sys_status_dict_localbuf = re.findall(f'(.*?): {i}\n', sys_status_txt_local)[0]
        sys_status_dict_local[i] = sys_status_dict_localbuf.strip(' ')
    return sys_status_dict_local

def GetFansStatus():
    fans_status_txt_local = os.popen('omreport chassis fans').read()
    fans_status_list = re.findall('Status *: (.*?)\nProbe Name *: System Board FAN (\d) RPM\nReading *: (\d*) RPM', fans_status_txt_local)
    fans_status = str()
    for singfan_status in fans_status_list:
        fans_status += f'槽位: {singfan_status[1]}; 状态: {singfan_status[0]}; 转速: {singfan_status[2]}RPM\n'
    return '\n机箱风扇状态:\n' + fans_status

def GetIntrusionStatus():
    intr_status_txt_local = os.popen('omreport chassis intrusion').read()
    return '\n机箱侵入状态:\n'+intr_status_txt_local

def GetMemoryStatus():
    memory_status_txt_local = os.popen('omreport chassis memory').read()
    me_arr = re.findall('Fail Over State *: (.*?)\nMemory Operating Mode Configuration : (.*?)\n.*Installed Capacity *: (\d*) .*Slots Available *: (\d*)\nSlots Used *: (\d*)\n', memory_status_txt_local, re.S)[0]
    memory_status_list = re.findall('Status *: (.*?)\nConnector Name *: (.*?)\nType *: (.*?)\nSize *:(.*?)\n', memory_status_txt_local)
    memory_status_array = '内存阵列属性:\n'
    memory_status_array += f'故障转移状态: {me_arr[0]}\n内存配置模式: {me_arr[1]}\n已安装容量: {me_arr[2]}MB\n可用插槽数: {me_arr[3]}\n已用插槽数: {me_arr[4]}\n'
    memory_status = '内存信息:\n'
    for singmemory_status in memory_status_list:
        memory_status += f'槽位: {singmemory_status[1]}; 状态: {singmemory_status[0]}; 类型: {singmemory_status[2]}; 容量: {singmemory_status[3]}\n'
    return memory_status_array + memory_status

def GetPowersupStatus():
    powersup_status_txt_local = os.popen('omreport chassis pwrsupplies').read()
    powersup_status_list = re.findall('Status *: (\w+)\nLocation *: (.*?) Status\nType *: (\w+).*?Online Status *: (.*?)\n', powersup_status_txt_local, re.S)
    powersup_status_local = str()
    for powersup_status in powersup_status_list:
        powersup_status_local += f'电源{powersup_status[1]}: {powersup_status[0]}; 类型:{powersup_status[2]}; 工作状态:{powersup_status[3]}\n'
    return '\n电源信息:\n' + powersup_status_local

def GetPowermenStatus():
    powermen_status_txt_local = os.popen('omreport chassis pwrmanagement').read()
    return '\n电源功耗:\n' + powermen_status_txt_local

def GetProcessorsStatus():
    processors_status_txt_local = os.popen('omreport chassis processors').read()
    processors_status_list = re.findall('Status *: (\w+)\nConnector Name *: (\w+)\nProcessor Brand *: (.*)\n.*\nCurrent Speed *: (.+)\nState *:(.+)\nCore Count *: (.+)', processors_status_txt_local)
    processors_status_local = str()
    for processors_status in processors_status_list:
        buf = processors_status
        processors_status_local += f'{buf[1]}: {buf[0]}; 状态:{buf[4]}; 速度:{buf[3]}; 核心数:{buf[5]};\n型号: {buf[2]}\n'
    return '\nCPU信息:\n' + processors_status_local

def GetTemperaturesStatus():
    temperatures_status_txt_local = os.popen('omreport chassis temps').read()
    temperatures_status_list = re.findall('Index *: (\d)\nStatus *: (\w+)\n.*\nReading *: (.*?)\n', temperatures_status_txt_local)
    temperatures_status_local = str()
    for temperatures_status in temperatures_status_list:
        temperatures_status_local += f'主板环境温度传感器{temperatures_status[0]}:{temperatures_status[1]}; 读数:{temperatures_status[2]}\n'
    return '\n温度状态:\n' + temperatures_status_local

def GetVoltagesStatus():
    voltages_status_txt_local = os.popen('omreport chassis volts').read()
    return '\n板载电压信息:\n' + voltages_status_txt_local

def GetBatteriesStatus():
    batteries_status_txt_local = os.popen('omreport chassis batteries').read()
    return '\n板载CMOS电池状态:\n' + batteries_status_txt_local

def GetCtlBatteryInfo():
    battery_status_local = str()
    controller_card_txt = os.popen('omreport storage controller').read()
    controller_card_list = re.findall('Name * : (.*?)\n', controller_card_txt)
    for i in range(0, len(controller_card_list)):
        battery_status_txt = os.popen(f'omreport storage battery controller={i}').read()
        if 'No Batteries found' in battery_status_txt:
            return False
        battery_status_list = re.findall('ID *: (\d*)\nStatus *: (.*)\nName.*\nState *: (.*)\n.*\n.*\nLearn State *: (.*)\n', battery_status_txt)[0]
        if battery_status_list[1] == 'Ok' and battery_status_list[2] == 'Ready':
            pass
        else:
            battery_status_local += f'阵列卡{controller_card_list[i]}电池异常\n'
            battery_status_local += f'电池状态: {battery_status_list[1]}, {battery_status_list[2]}; 记忆状态: {battery_status_list[3]}'
    return battery_status_local

def GetStorageInfo():
    vdisk_status_local = str()
    storage_vdisk_status_txt = os.popen('omreport storage vdisk').read()
    repat = re.compile('ID *: (\d*)\nStatus *: (.*?)\nName * : (.*?)\nState *: (.*?)\n.*?Layout *: (.*?)\nSize *: (.*?)\n.*?Bus Protocol *: (.*?)\nMedia *: (.*?)\n.*?Stripe Element Size  *: (.*?)\n', re.S)
    controller_card_list = re.findall('Controller PERC (.*?)\n', storage_vdisk_status_txt)
    for controller_card_name in controller_card_list:
        vdisk_status_local += f'阵列卡{controller_card_name}虚拟磁盘:\n'
        start_pos = storage_vdisk_status_txt.find('Controller PERC ' + controller_card_name)
        controller_card_status_list = repat.findall(storage_vdisk_status_txt, start_pos, len(storage_vdisk_status_txt)//len(controller_card_list) + start_pos)
        for controller_card_status in controller_card_status_list:
            if controller_card_status[1] == 'Ok' and controller_card_status[3] == 'Ready':
                vdisk_status_local += f'虚拟盘 {controller_card_status[0]}: OK\n'
            else:
                vdisk_status_local += '虚拟磁盘异常\n'
                i = controller_card_status
                buffer = f'虚拟盘 {i[0]}: {i[1]}; 名称: {i[2]}; 状态: {i[3]}; 阵列类型: {i[4]}; 总容量: {i[5]}; 协议: {i[6]}; 磁盘类型: {i[7]}; 条带元素大小: {i[8]}\n'
                vdisk_status_local += buffer

    pdisk_status_local = str()
    for i in range(0, len(controller_card_list)):
        storage_pdisk_status_txt = os.popen(f'omreport storage pdisk controller={i}').read()
        controller_card_name = re.findall('Controller PERC (.*?)\n', storage_pdisk_status_txt)[0]
        pdisk_status_list = re.findall('ID *: (.*?)\nStatus *: (.*?)\n.*\nState *: (.*?)\n', storage_pdisk_status_txt)
        for sing_pdisk_status in pdisk_status_list:
            if sing_pdisk_status[1] == 'Ok' and sing_pdisk_status[2] == 'Online':
                pass
            else:
                pdisk_status_local += f'阵列卡{controller_card_name}物理磁盘异常\n'
                pdisk_status_local += f'盘位 {sing_pdisk_status[0]}: {sing_pdisk_status[1]}; 状态: {sing_pdisk_status[2]}\n'
    return vdisk_status_local, pdisk_status_local

def GetEnclosureInfo():
    enclosure_status_local = str()
    enclosure_status_txt = os.popen('omreport storage enclosure').read()
    enclosure_status_list = re.findall('ID *: (.*)\nStatus *: (.*)\nName *: (.*)\nState *: (.*)\n', enclosure_status_txt)
    for sing_enclosure_status in enclosure_status_list:
        if sing_enclosure_status[1] == 'Ok' and sing_enclosure_status[3] == 'Ready':
            pass
        else:
            enclosure_status_local += '机柜异常\n'
            enclosure_status_local += f'机柜{sing_enclosure_status[0]}: {sing_enclosure_status[1]}; 名称: {sing_enclosure_status[2]}; 状态: {sing_enclosure_status[3]}\n'
            if len(enclosure_status_list) >= 2:
                enclosure_com_temps_txt = os.popen(f'omreport storage enclosure controller=1 enclosure={sing_enclosure_status[0]} info=temps').read()
                enclosure_com_temps_list = re.findall('ID *: (.*)\nStatus *: (.*)\nName.*\nState *: (.*)\nReading *: (\d*) C\n', enclosure_com_temps_txt)
                for i in enclosure_com_temps_list:
                    if i[1] == 'Ok' and i[2] == 'Ready':
                        pass
                    else:
                        enclosure_status_local += f'机柜{sing_enclosure_status[2]}--'
                        enclosure_status_local += f'温度传感器 {i[0]}: {i[1]}; 状态: {i[2]}; 读数: {i[3]}°C\n'

                enclosure_com_fans_txt = os.popen(f'omreport storage enclosure controller=1 enclosure={sing_enclosure_status[0]} info=fans').read()
                enclosure_com_fans_list = re.findall('ID *: (.*)\nStatus *: (.*)\nName.*\nState *: (.*)\nPart.*\nSpeed *(.*)\n', enclosure_com_fans_txt)
                for i in enclosure_com_fans_list:
                    if i[1] == 'Ok' and i[2] == 'Ready':
                        pass
                    else:
                        enclosure_status_local += f'机柜{sing_enclosure_status[2]}--'
                        enclosure_status_local += f'风扇{i[0]}: {i[1]}; 状态: {i[2]}; 转速: {i[3]}\n'

                enclosure_com_power_txt = os.popen(f'omreport storage enclosure controller=1 enclosure={sing_enclosure_status[0]} info=pwrsupplies').read()
                enclosure_com_power_list = re.findall('ID *: (.*)\nStatus *: (.*)\nName.*\nState *: (.*)\n', enclosure_com_power_txt)
                for i in enclosure_com_power_list:
                    if i[1] == 'Ok' and i[2] == 'Ready':
                        pass
                    else:
                        enclosure_status_local += f'机柜{sing_enclosure_status[2]}--'
                        enclosure_status_local += f'电源{i[0]}: {i[1]}; 状态: {i[2]}\n'

                enclosure_com_emms_txt = os.popen(f'omreport storage enclosure controller=1 enclosure={sing_enclosure_status[0]} info=emms').read()
                enclosure_com_emms_list = re.findall('ID *: (.*)\nStatus *: (.*)\nName.*\nState *: (.*)\n', enclosure_com_emms_txt)
                for i in enclosure_com_emms_list:
                    if i[1] == 'Ok' and i[2] == 'Ready':
                        pass
                    else:
                        enclosure_status_local += f'机柜{sing_enclosure_status[2]}--'
                        enclosure_status_local += f'EMMS{i[0]}: {i[1]}; 状态: {i[2]}\n'
    return enclosure_status_local

def GetLocalAddress() -> str:
    alladdr_info = socket.getaddrinfo(socket.gethostname(), None)
    for addr_info in alladdr_info:
        addr = re.findall('^10.6\d.\d+.1*$',addr_info[4][0])
        if addr:
            return addr[0]

def SocketResponse(report:str):
    nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
    local_ip = GetLocalAddress()
    if not local_ip:
        with open(f'ProgramLogs.txt', 'a') as warnlog:
                warnlog.write(f'{nowtime}:ERROR[1005]---get ip fail\n')
        return 0
    try:
        PDLserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PDLserver.bind((local_ip, 6650))
        PDLserver.settimeout(SOCKET_TIMEOUT)
        PDLserver.listen(3)
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        PDLsock, PDLaddr = PDLserver.accept()
    except socket.timeout:
        with open(f'ProgramLogs.txt', 'a') as warnlog:
                warnlog.write(f'{nowtime}:ERROR[1006]---timeout no connection\n')
    except:
        with open(f'ProgramLogs.txt', 'a') as warnlog:
                warnlog.write(f'{nowtime}:ERROR[1007]---Unknow\n')
    else:
        first_req = PDLsock.recv(1024)
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        if first_req.decode('ascii') == 'ready':
            sizeof = len(report)
            PDLsock.send(str(sizeof).encode('ascii'))
            PDLsock.recv(1024)
            last_index = 0
            for curr_index in range(1024, sizeof + 1024, 1024):
                senddata = report[last_index:curr_index]
                last_index = curr_index
                PDLsock.send(senddata.encode('utf-8'))
        else:
            PDLsock.close()
            PDLserver.close()
            with open(f'ProgramLogs.txt', 'a') as warnlog:
                warnlog.write(f'{nowtime}:ERROR[1008]---the first is unexpected\n')
        PDLsock.close()
    finally:
        PDLserver.close()

def InsLogsWrite(writein:str):
    logname = time.strftime('%Y%m%d%H%M', time.localtime())
    logtime = time.strftime('%Y/%m/%d-%H:%M', time.localtime())
    with open(f'InsLogs/{logname}.txt', 'w', encoding='utf-8') as inslog:
                inslog.write(f'[{logtime}]:{writein}\n')
    path =f'{os.getcwd()}/InsLogs'
    file_list = os.listdir(path)
    while len(file_list) > 149:
        os.remove(f'{path}/{file_list[0]}')
        file_list = os.listdir(path)

#--------------------------------------------start--------------------------------------------#
REPORT = str()
warning_list = list()
sys_status_dict = GetSystemStatus()                             # 系统机箱判断
for sys_component_name in SYS_COMPONENT:
    if sys_status_dict[sys_component_name] == 'Ok':
        pass
    else:
        if sys_component_name == 'Fans':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetFansStatus())
        elif sys_component_name == 'Intrusion':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetIntrusionStatus())
        elif sys_component_name == 'Memory':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetMemoryStatus())
        elif sys_component_name =='Power Supplies':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetPowersupStatus())
        elif sys_component_name == 'Power Management':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetPowermenStatus())
        elif sys_component_name == 'Processors':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetProcessorsStatus())
        elif sys_component_name == 'Temperatures':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetTemperaturesStatus())
        elif sys_component_name == 'Voltages':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetVoltagesStatus())
        elif sys_component_name == 'Hardware Log':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + '\n硬件日志异常\n')
        elif sys_component_name == 'Batteries':
            warning_list.append(f'系统机箱异常--{sys_component_name}: {sys_status_dict[sys_component_name]}' + GetBatteriesStatus())

battery_status = GetCtlBatteryInfo()                            # 阵列卡电池单项
if battery_status:
    warning_list.append(battery_status)

vdisk_status, pdisk_status= GetStorageInfo()                    # 磁盘
if '异常' in vdisk_status:
    warning_list.append(vdisk_status)
if '异常' in pdisk_status:
    warning_list.append(pdisk_status)

enclosure_status = GetEnclosureInfo()                           # 机柜(MD1200)
if enclosure_status:
    warning_list.append(enclosure_status)

if warning_list:
    for i in warning_list:
        REPORT += i
else:
    REPORT = '-----All system OK !'

SocketResponse(REPORT)
InsLogsWrite(REPORT)
#---end
