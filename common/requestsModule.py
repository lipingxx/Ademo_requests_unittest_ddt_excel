# coding:utf-8
'''
    封装requests方法
'''
import json
import requests

from Ademo_unittest_logging_email_test.common import  read_excel
from Ademo_unittest_logging_email_test.common.write_excel import  copy_excel,Write_excel

def send_requests(testdata):
    '''封装requests请求'''
    id = testdata['id']
    case_name = testdata['case_name']
    method = testdata["method"]
    url_base = testdata["url"]
    # 因为发现读取接口url时，最后带上了换行符，所以把右边的空格全删除
    url = url_base.rstrip()
    # params
    #try:
        # eval(expression,globals=None,locals=None):expression:传入的表达式;globals是可选参数，不设置时，则必须为dict对象，locals：不为None时，可以是任何map对象
        #params = eval(testdata["params"])
    #except:
        #params = None
    params = testdata['params']
    try:
        headers = eval(testdata["headers"])
        print("请求头部：%s" % headers)
    except:
        headers = None

    type = testdata["type"]
    #test_api = testdata['func_name']
    test_nub = testdata['id']

    print("测试用例场景：%s" % case_name)
    print("请求url： %s" % url)
    print("请求params：%s" % params)

    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}

    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata

    # 判断选择调用request的某个方法
    try:
        if method == "post":
            print("post请求body类型为：%s ,body内容为：%s" % (type, body))
            r = requests.post(url=url,data=params,headers={'content-type': 'application/json'})
            print(r.status_code)

        elif method == 'get':
            print("get请求!")  # body类型为：%s ,body内容为：%s" % (type, body))
            r = requests.get(url=url, data=params)

        elif method == 'patch':
            pass

        elif method == 'put':
            pass
        else:
            print('其他请求，结束！')
            return None

        print("页面返回信息：%s" % r.content.decode("utf-8"))

        # 接受返回数据
        res = {}
        res['id'] = testdata['id']
        res['rowNum'] = testdata['id'] + 1              # 第一行被字段占用，所以需要
        res["statuscode"] = str(r.status_code)          # 状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str

        if res["statuscode"] != "200":
            res["error"] = res['text']
        else:
            res["error"] = ""

        res["msg"] = ""

        # 进行判断
        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res["result"] = "fail"
        return res

    except Exception as msg:
        res["msg"] = str(msg)
    return res

def wirte_result(result, filename="result.xlsx"):
    # 返回结果的行数row_nub
    row_nub = result['rowNum']
    # 写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 9,  result['statuscode'])     # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 10, result['times'])          # 耗时
    wt.write(row_nub, 11, result['error'])          # 状态码非200时的返回信息
    wt.write(row_nub, 13, result['result'])
    wt.write(row_nub, 14, result['msg'])            # 抛异常


if __name__ == "__main__":
    data = read_excel.ApiDefine_change('F:\Python_project\Ademo_unittest_logging_email_test\dataExcel\出口合理性分析导出接口new.xlsx').dict_data()
    print(data)
    #s = requests.session()
    res = send_requests(data)
    copy_excel("出口合理性分析导出接口new.xlsx", "result.xlsx")
    wirte_result(res, filename="result.xlsx")
