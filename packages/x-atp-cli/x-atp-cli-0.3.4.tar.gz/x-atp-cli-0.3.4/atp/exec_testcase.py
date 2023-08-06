import platform
from x_sweetest import Autotest


def run_test_frame(plan_name, desired_caps):
    # 测试用例集文件里的Sheet表单名称
    sheet_name = '*'
    # 通过X-Sweetest执行自动化测试
    server_url = ''
    sweet = Autotest(plan_name, sheet_name, desired_caps, server_url)
    sweet.plan()
    # 创建并写入测试详情文件
    details_file = open('details/details.txt', 'w', encoding='utf-8')
    details_file.write(str(sweet.report_data))
    details_file.close()


def exec_testcase(test_name, test_type):
    if test_type.lower() == 'api':
        # API测试配置参数
        desired_caps = {'platformName': 'api'}
    else:
        sys_name = platform.system()
        if sys_name == 'Linux':
            # Linux平台下web测试配置参数
            desired_caps = {'platformName': 'Desktop', 'browserName': 'Chrome', 'headless': True}
        else:
            # 非linux平台下web测试配置参数
            desired_caps = {'platformName': 'Desktop', 'browserName': 'Chrome'}
    # 执行测试框架X-Sweetest
    try:
        run_test_frame(plan_name=test_name, desired_caps=desired_caps)
    except Exception as exc:
        return exc
    return True


if __name__ == '__main__':
    exec_testcase(test_name='baidu', test_type='api')
