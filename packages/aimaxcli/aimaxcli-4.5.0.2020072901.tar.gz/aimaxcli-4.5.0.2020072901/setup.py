#!/usr/bin/env python
from setuptools import setup, find_packages
PROJECT = 'aimaxcli'

# Change docs/sphinx/conf.py too!
VERSION = '4.5.0.2020072901'



try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='AIMax python commands client',
    long_description=long_description,

    author='Gavin Li',
    author_email='gavin_li@amaxgs.com',

    #url='https://github.com/openstack/cliff',
    #download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff','requests'],
    #requests json
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    entry_points={
        #'console_scripts': [
        #    'cliffdemo = cliffdemo.main:main' 'as = aimaxcmd.main:main'
        #],
        'console_scripts': [
            'aimax= aimaxcmd.main:main'
        ],
        'aimax.client': [
            # 'simple = cliffdemo.simple:Simple',
            # 'two_part = cliffdemo.simple:Simple',
            # 'error = cliffdemo.simple:Error',
            # 'list files = cliffdemo.list:Files',
            # 'files = cliffdemo.list:Files',
            # 'file = cliffdemo.show:File',
            # 'show file = cliffdemo.show:File',
            # 'unicode = cliffdemo.encoding:Encoding',
            # 'hooked = cliffdemo.hook:Hooked',
            'connect = aimaxcmd.cmds_base:Connect',#
            # 'linked = cliffdemo.hook:Linked',
            'disconnect = aimaxcmd.cmds_base:Disconnect',#
            'node list = aimaxcmd.cmds_node:NodeList',#
            'node info = aimaxcmd.cmds_node:NodeInfo',#
            'node overview = aimaxcmd.cmds_node:NodeOverview',
            'node poweron = aimaxcmd.cmds_node:PowerOn',
            'node poweroff = aimaxcmd.cmds_node:PowerOff',
            'node reset = aimaxcmd.cmds_node:PowerReset',
            'node tag = aimaxcmd.cmds_node:NodeTag',
            'node delete = aimaxcmd.cmds_node:NodeDelete',
            'node add = aimaxcmd.cmds_node:NodeAdd',
            'group list = aimaxcmd.cmds_user:GroupList',
            'group info = aimaxcmd.cmds_user:GroupInfo',
            'group add = aimaxcmd.cmds_user:GroupAdd',
            'group delete = aimaxcmd.cmds_user:GroupDelete',
            'user list = aimaxcmd.cmds_user:UserList',
            'user info = aimaxcmd.cmds_user:UserInfo',
            #'user add = aimaxcmd.cmds_user:UserAdd',
            'user quotas = aimaxcmd.com_list:CommonAdd',
            'user add = aimaxcmd.com_list:CommonAdd',#增加用户
            'user getgpuList =aimaxcmd.com_list:CommonList',#创建用户前 获取 gpu类型列表

            #'zone list = aimaxcmd.cmds_zone:NodeList',#
            #'zone info = aimaxcmd.cmds_node:NodeInfo',#
            'zone list =aimaxcmd.com_list:CommonList',
            'zone get =aimaxcmd.com_list:CommonShow',
            'zone add =aimaxcmd.com_list:CommonAdd',
            'zone del =aimaxcmd.com_list:CommonDelete',
            'zone getgpuList =aimaxcmd.com_list:CommonList',#创建用户前 获取 gpu类型列表

            'image list =aimaxcmd.com_list:CommonList',#获取镜像列表
            'image addHarborUser =aimaxcmd.com_list:CommonAdd',#增加harbor用户
            'image forjob =aimaxcmd.com_list:CommonList',#根据job获取适配的镜像
            'image repositoriesByprojectId =aimaxcmd.com_list:CommonList',# 根据用户获取镜像
            'image syncImage =aimaxcmd.com_list:CommonAdd',#同步镜像
            'image disclose =aimaxcmd.com_list:CommonAdd',#公开镜像
            'image share =aimaxcmd.com_list:CommonAdd',# 分享镜像
            'image shareObj =aimaxcmd.com_list:CommonList',# 获取共享对象
            'image getshare =aimaxcmd.com_list:CommonShow',# 查看某用户的分享镜像列表
            'image cancel =aimaxcmd.com_list:CommonDelete',# 取消分享镜像
            'image getImageByName =aimaxcmd.com_list:CommonShow',# 根据名称获取镜像
            'image getImagesByProjectId =aimaxcmd.com_list:CommonList',# 根据项目id获取镜像
            'image doNewTags =aimaxcmd.com_list:CommonAdd',# 打标签
            'image uploadTar =aimaxcmd.com_list:CommonUpload',# 文件上传具体实现方法（单文件上传）
            'image uploadDockfile =aimaxcmd.com_list:CommonUpload',#上传dokcerfile
            'image delete =aimaxcmd.com_list:CommonDelete',#删除镜像
            'image isContainerMaking =aimaxcmd.com_list:CommonShow',#isContainerMaking
            'storage createVolumes =aimaxcmd.com_list:CommonAdd',
            'storage createNFSVolumes =aimaxcmd.com_list:CommonAdd',#创建NFS卷
            'storage createFolder =aimaxcmd.com_list:CommonAdd',#创建文件夹
            'storage getVolumeInfo =aimaxcmd.com_list:CommonList',#获取卷信息
            'storage listVolumes =aimaxcmd.com_list:CommonList',
            'storage listDirs =aimaxcmd.com_list:CommonList',#获取共享对象
            'storage listNFSVolumes =aimaxcmd.com_list:CommonPut',#获取NFS卷
            'storage getJobFileLocation =aimaxcmd.com_list:CommonShow',#获取
            'storage getShareData =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getShareObjs =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getShareDataOpInfo =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getDecompressInfo =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage cancelDecompress =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getMyShareData =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage copyShareData =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getFileInfo =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage getPrivateVol =aimaxcmd.com_list:CommonShow',#获取共享数据
            'storage deleteDirs =aimaxcmd.com_list:CommonDelete',#
            'storage tagDeletedForHomeDir =aimaxcmd.com_list:CommonDelete',#
            'storage uploadvolumes =aimaxcmd.com_list:CommonUpload',#更新卷
            'storage downloadvolumes =aimaxcmd.com_list:CommonDownload',#下载 目前前台使用 FTP 直接获取 不走api
            'storage downloadBigFile =aimaxcmd.com_list:CommonDownload',#下载
            'storage zipFolder =aimaxcmd.com_list:CommonDownload',#下载
            'storage unzipFolder =aimaxcmd.com_list:CommonPut',#下载
            'storage progress =aimaxcmd.com_list:CommonShow',#查询下载的的进度
            'storage copyData =aimaxcmd.com_list:CommonShow',#复制
            'storage moveData =aimaxcmd.com_list:CommonShow',#移动
            'storage shareData =aimaxcmd.com_list:CommonAdd',#分享数据
            'storage cancleShareData =aimaxcmd.com_list:CommonDelete',#取消分享
            'storage rename =aimaxcmd.com_list:CommonPut',#重命名
            'storage chmodFile =aimaxcmd.com_list:CommonPut',#设置权限
            'storage createUserFolder =aimaxcmd.com_list:CommonAdd',#创建用户文件夹
            'storage updateVolumeQuota =aimaxcmd.com_list:CommonPut',#更新卷用量
            # 'listBricks': # gluster TODO 转块 暂不实现
            # 'expandeVolume': # gluster TODO 转块 暂不实现
            #'storage tagDeletedForHomeDir =aimaxcmd.com_list:CommonDelete',#删除目录
            'job createJob =aimaxcmd.com_list:CommonAdd',
            'job createDeployment =aimaxcmd.com_list:CommonAdd',
            'job list =aimaxcmd.com_list:CommonList',
            'job listDeployment =aimaxcmd.com_list:CommonList',# 获取模型部署列表
            'job info =aimaxcmd.com_list:CommonShow',#获取任务信息
            'job getgpuList =aimaxcmd.com_list:CommonList',#创建任务前 获取 gpu类型列表
            'job getErrorInfo =aimaxcmd.com_list:CommonShow',#获取任务错误信息
            'job getErrorList =aimaxcmd.com_list:CommonList',#获取任务错误信息列表
            'job getPredictResult =aimaxcmd.com_list:CommonAdd',#获取结果
            'job getInputParameterSample =aimaxcmd.com_list:CommonShow',#模型部署时 测试
            'job generateImageFromContainer =aimaxcmd.com_list:CommonAdd',#获取结果
            'job getJobSaveImgInfo =aimaxcmd.com_list:CommonShow',#获取任务镜像信息
            'job getJobLog =aimaxcmd.com_list:CommonShow',#获取任务信息
            'job getNodeTaintStatus =aimaxcmd.com_list:CommonShow',#
            'job listPods =aimaxcmd.com_list:CommonShow',#测试用的接口
            'job getNodeAllocatable =aimaxcmd.com_list:CommonShow',#未找到controller的实现
            'job removeJob =aimaxcmd.com_list:CommonDelete',#移除任务
            'job removeDeploymentAndSVC =aimaxcmd.com_list:CommonDelete',#移除任务
            'job pause =aimaxcmd.com_list:CommonPut',#挂起任务
            'job resume =aimaxcmd.com_list:CommonPut',#重新开始任务
            'job pauseDeployment =aimaxcmd.com_list:CommonPut',#挂起部署任务
            'job resumeDeployment =aimaxcmd.com_list:CommonPut',#重新开始部署任务
            'job unschedule =aimaxcmd.com_list:CommonPut',#取消定时任务
            'job schedule =aimaxcmd.com_list:CommonPut',#定时任务
            'job createTemplate =aimaxcmd.com_list:CommonAdd',#创建模板
            'job getTemplate =aimaxcmd.com_list:CommonShow',#获取模板
            'job getCaffeEntity =aimaxcmd.com_list:CommonShow',#获取caffe
            'job delTemplate =aimaxcmd.com_list:CommonDelete',#删除模板 软删除 只是改了状态位0变1
            'job updateTemplate =aimaxcmd.com_list:CommonPut',#更新模板
            'job getTemplateList =aimaxcmd.com_list:CommonList',#获取模板列表
            'job getVisualInfoList =aimaxcmd.com_list:CommonList',#根据用户和任务名获取可视化任务
            'job visualForTensorflow =aimaxcmd.com_list:CommonShow',#visualForTensorflow
            'job visualForCaffe =aimaxcmd.com_list:CommonShow',#visualForCaffe
            'job removeVisual =aimaxcmd.com_list:CommonDelete',#删除visual
            'monitor getNodeDockers =aimaxcmd.com_list:CommonShow',#获取节点的docker
            'monitor getNodeHistory =aimaxcmd.com_list:CommonShow',#获取节点历史
            'monitor getNodeInfo =aimaxcmd.com_list:CommonShow',#获取节点信息
            'monitor getNodeItem =aimaxcmd.com_list:CommonShow',#获取节点信息item
            'monitor getClusterHistory =aimaxcmd.com_list:CommonShow',#获取监控历史
            'monitor getClusterHealth =aimaxcmd.com_list:CommonShow',#获取集群健康
            'monitor getClusterItem =aimaxcmd.com_list:CommonShow',#获取集群健康
            'monitor getJobHistory =aimaxcmd.com_list:CommonShow',#获取任务历史
            'monitor getJobInfo =aimaxcmd.com_list:CommonShow',#获取任务信息
            'monitor getJobSummery =aimaxcmd.com_list:CommonShow',#获取任务summery
            'monitor getNodeDashboard =aimaxcmd.com_list:CommonShow',#获取任务仪表
            'monitor getNamespaceDashboard =aimaxcmd.com_list:CommonShow',#获取命名空间仪表
            'monitor getReportTnterval =aimaxcmd.com_list:CommonShow',#获取报告
            'monitor getReportHistory =aimaxcmd.com_list:CommonShow',#获取报告
            'list = aimaxcmd.com:CommonList',#get 17
            'put = aimaxcmd.com:CommonPut',#put 13
            'add = aimaxcmd.com:CommonAdd',#post 6
            #'creat = aimaxcmd.com:CommonAdd',#post
            'post = aimaxcmd.com:CommonAdd',# 11
            'del = aimaxcmd.com:CommonDelete',#del 11
            'get = aimaxcmd.com:CommonShow',#get 40
            'upload = aimaxcmd.com:CommonUpload',#post 3
            'download = aimaxcmd.com:CommonDownload',#get 3
            #'cmdimage list = aimaxcmd.cmds_image:CommonList',#

            'json = aimaxcmd.com:CommonDownload',#get 3
        ],

        'cliff.demo.hooked': [
            'sample-hook = cliffdemo.hook:Hook',
        ],
    },

    zip_safe=False,
)
