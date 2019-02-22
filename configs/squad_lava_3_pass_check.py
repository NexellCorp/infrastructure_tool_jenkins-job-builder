import pycurl
from StringIO import StringIO
from squad_lava_4_report_detail import report_detail_main
import json


pass_condition = {'"job_status"': '"Complete"', '"failure"': "null"}


def getBuffer(url) :
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return body


def resultParse(url):
    body = getBuffer(url)

    tmpHash = body[1:-1].split(',')
    is_job_status_complete = False
    is_failure_null = False
    testrunUrl = ""

    for _ in tmpHash:
        if pass_condition.keys()[0] in _ and _.split(':')[1] == pass_condition.values()[0]:  # job_status is Complete
            # print(_.split(':')[1])
            is_job_status_complete = True
        elif pass_condition.keys()[1] in _ and _.split(':')[1] == pass_condition.values()[1]:  # failure is Null
            # print(_.split(':')[1])
            is_failure_null = True
        elif '"testrun"' in _ :
            testrunUrl = "http" + _.split('http')[1][:-1]
            print("testruns : %s" % testrunUrl)
        else:
            pass

    if is_job_status_complete and is_failure_null :
        return pass_fail_check(testrunUrl + "tests_file/")
    else:
        return "LAVA Test Fail!"


def pass_fail_check(url) :
    body = getBuffer(url)

    tests_file_dict = json.loads(body)
    pass_cnt = 0
    fail_cnt = 0

    print("**********************************************************")
    for _ in list(tests_file_dict.keys()) :
        print("test %s : %s" % (_, tests_file_dict[_]))
        if tests_file_dict[_] == 'fail' :
            fail_cnt += 1
        elif tests_file_dict[_] == 'pass' :
            pass_cnt += 1
        else :
            pass

    print("pass : %d / fail : %d" % (pass_cnt, fail_cnt))

    if fail_cnt > 0 :
        return "LAVA Test Fail!"

    return "LAVA Test SUCCESS"


def pass_check_main(arg1, arg2):
    ret = resultParse(arg1)
    print (ret)
    report_detail_main(arg1, arg2)
