

# 这个采用 python + unittest + requests/ui + test*.py + logging + report + email 自动化测试
# case:                         测试场景test*.py
# case_excel：                  excel\api接口测试场景
# common：
        -> create_find_report.py 创建找最新测试报告集合
        -> requestModule.py：    request方法封装
        -> logger.py：           log方法的封装
        -> read_excel.py：       读取excel接口测试数据
        -> write_excel.py：      copy接口测试数据至report文件夹下，并将测试的结果（状态码、信息）写入excel文件
        -> sendEmail.py：        邮件发送测试报告（.html）模块封装
        -> write_excel.py：      将测试结果吸入copy的excel文件
        -> zipFile.py：          压缩文件模块封装
        -> HTMLRunner*.py：      html报告文件


# config：
        -> config.ini：          存放excel测试数据路径；存放邮箱的配置信息；
        -> readConfig.py：       读取配置文件
        -> confyaml.yaml：       yaml格式的配置文件
        -> readYaml.py：         读取.yaml文件的内容
        -> writeToYaml.py：      向.yaml文件写入信息

# dataExcel：                    存放接口测试数据
# report：                       存放报告、测试结果信息，每次执行都会生成最新的测试报告集。
# log：                          存放log日志文件

# run_main_basic.py：            最基本，无封装。加载、执行测试用例，发送邮件
# run_main_testPack.py：         test*.py；封装，加载case的测试场景,
# run_main_excel.py：            ddt；封装，加载case_excel的接口测试场景
# run_main_threads.py：          引入BeautifulReport，并多线程执行测试用例

【20180806】
    1、多线程模式                 见run_main_threads.py

【20180808】
    1、增加yaml文件以及读取模块    ok
