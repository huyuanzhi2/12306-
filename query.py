'''
查询两站之间的火车票信息

12306 api:
'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-09-02&leftTicketDTO.from_station=CSQ&leftTicketDTO.to_station=WHN&purpose_codes=ADULT'

'''
import sys
import requests
import json

# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()

# 城市名代码查询字典
# key：城市名 value：城市代码
from station import stations_dict
# 反转k，v形成新的字典
code_dict = {v: k for k, v in stations_dict.items()}
headers = { 
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cookie':'JSESSIONID=D49C62439EB50716094A141666EC3B6C; tk=wfA5EKQVrZeGRBcPCzK8Gvi2zoqZCv5OUr7Ns9PGgp5f-OLKy01110; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1943601418.24610.0000; BIGipServerpassport=770179338.50215.0000; fp_ver=4.5.0; RAIL_EXPIRATION=1503024514968; RAIL_DEVICEID=MdO_m-DlnJCor17yMpr_SplIZpM65GBIMuuqk-i2caV-ovk9i2BkivcANXNW2LHSzwoJBTmU_A8_hEIHMR8MU6Q1FjBNcdWDRjng4-L8JBfp5-Ffq91OaX1EUnM_n8hiI1SoaNd4enTOQcNLt973zDZOWg-l_Ssf; RAIL_OkLJUJ=FFA4Z04ub2RkOq5Dkr3AF5xb6Hi2CFY9; current_captcha_type=Z; _jc_save_fromStation=%u957F%u6C99%2CCSQ; _jc_save_toStation=%u6B66%u6C49%2CWHN; _jc_save_fromDate=2017-09-02; _jc_save_toDate=2017-08-15; _jc_save_wfdc_flag=dc',
            'Host':'kyfw.12306.cn',
            'If-Modified-Since':'0',
            'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            }

def get_query_url(text):
    '''
    返回调用api的url链接
    '''
    try:
        date = text[0] 
        from_station_name = text[1] 
        to_station_name = text[2]
        from_station=stations_dict[from_station_name]
        to_station = stations_dict[to_station_name]
    except:
        date,from_station,to_station='--','--','--' 
    #将城市名转换为城市代码
    
    # api url 构造
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
    #print(url)
    
    return url

def query_train_info(url):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''

    info_list = []
    try:
        r = requests.get(url,headers=headers,verify=False)
        r.encoding = 'utf-8'
        #print(r.text)
        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']
        #print(raw_trains)

        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'

            # 打印查询结果
            info = ('车次:{}\n出发站:{}  目的地:{}\n出发时间:{}  到达时间:{}  消耗时间:{}\n座位情况：\n一等座：「{}」  二等座：「{}」 软卧：「{}」 硬卧：「{}」 硬座：「{}」 无座：「{}」'.format(
                train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
                second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))

            info_list.append(info)

        return info_list
    except:
        return 'error'

if __name__ == '__main__':
    msg_content = sys.argv[1:4]
    infos = query_train_info(get_query_url(msg_content))
    if infos != 'error':
        for info in infos:
            print(info)
            print('='*40)
    else:
        print('输出有误')
