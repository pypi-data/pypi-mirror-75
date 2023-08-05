class Yml:
    restMap = {
        'zone':
            {
                #aimax list zone -F aaa 获取zonelist
                'reqUrl': '/api/job/zones',
                'resp': 'zones',  # response json的key
                'respcolumndesc': ("name", "createTimeStamp", "jobType"),
                'respcolumns': ("name", "createTimeStamp", "jobType"),

                # "%s/api/job/zones/%s?token=%s",
                #aimax get zone -F aaa  根据zonename获取zoneinfo
                'getUrl': '/api/job/zones',
                'getUrldesc': ("Please input zonename: "),

                #aimax add zone -F aaa  新增zone
                'addUrl': '/api/job/zones',
                'addarg': ("name", "jobType", "desc", "quotas", "message", "success", "totalSize"),
                # 'addargdef':(None,"ML","",{#NONE表示需要输入的
                #     "MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
                #     "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
                #     "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
                #     "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},"","true","0"),
                # 'addargdesc':("Please input zone name: ",
                #            "Please select JobType  0 ML 1 HPC",
                #            "Please input desc name: ",
                #            "Please input zone quotas: ","message","success","totalSize"
                #            ),
                # @RequestBody ZoneInfo
                'bodyjson': 'Please input ZoneInfo json (demo: {"name":"","jobType":"ML","desc":"","quotas":{"MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},"JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},"CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},"GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},"message":"","success":true,"totalSize":0}):',

                # aimax del zone -F aaa 删除zone
                # %s/api/job/zones/%s?token=%s
                'delUrl': '/api/job/zones',
                'delUrldesc': ("Please input zonename: "),
                'delconfirm': "The zone {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
            },

        'image':  # aimax list image -F aaa   #5
            {
                # 获取imagelist
                'reqUrl': '/api/image/images',
                'reqarg': ('loginName', 'page', 'publicPage', 'page_size', 'q'),
                'reqargdef': ('auth_username', '0', '1', '10', ''),
                # "%s/api/image/images?token=%s&q=%s&page=%s&pageSize=%s&publicPage=%s&loginName=%s"
                'resp': 'publicImages',  # response json的key
                'respcolumndesc': ("name", "creationTime", "tagsCount"),
                'respcolumns': ("name", "creationTime", "tagsCount"),
            },
        'imageforjob':  # aimax list imageforjob -F aaa
            {
                # 根据job获取适配的镜像
                # "%s?token=%s&page=%s&pageSize=%s&type=%s&frames=%s&visual=%s&jupyter=%s&deploy=%s&ssh=%s&vnc=%s"
                'reqUrl': '/api/image/imagesForjob',
                'reqarg': ('page', 'pageSize', 'type', 'frames', 'visual', 'jupyter', 'deploy', 'ssh', 'vnc'),  # ,
                'reqargdef': ('1', '10', None, 'caffe', "null", "null", "null", "false", "false"),
                'reqargdesc': ('1', '10', 'Please input type(0 某个用户,1 public仓库镜像,2 分享镜像): ',
                               'Please input frames(type:list demo1 [tensorflow-gpu:python],[caffe]): ',
                               # TODO此处后台有bug 模糊查询不可用
                               "null", "null", "null", "false", "false"),

                'resp': 'imagesForjob',  # response json的key
                'respcolumndesc': ("imageName", "系统", "标签"),
                'respcolumns': ("imageName", "dist", "tagName"),
            },
        'disclose':  # 公开镜像仅管理员 aimax add disclose -F aaa
            {
                # "%s/api/image/images/disclose?token=%s"
                'addUrl': '/api/image/images/disclose',
                # #body ImageShareInfo
                # 'body':{"totalSize":0,"imageName":"nginx","tagName":["latest"],"shareOfTag":[],
                #            "repositoryName":"ray4","message":"","success":"true"},
                # 'bodyarg':("repositoryName","imageName","tagName"),
                # 'bodydesc':('Please input repositoryName(demo:ray4): ',
                #      'Please input imageName(demo:nginx): ',
                #      'Please input tagName(demo:latest,stable-alpine): '),
                # 'bodytype':("str","str","array"),

                # @RequestBody ImageShareInfo
                'bodyjson': 'Please input ImageShareInfo json (demo: {"totalSize":0,"imageName":"nginx","tagName":["latest"],"shareOfTag":[],"repositoryName":"ray4","message":"","success":"true"}):',
            },

        'repositoriesByprojectId':  # 根据用户获取镜像 aimax list repositoriesByprojectId -F aaa
            {
                # "%s/api/image/images/%s/repository?token=%s&q=%s&page=%s&pageSize=%s"
                'reqUrl': '/api/image/images',
                'reqUrldesc': ("Please input username: "),
                'reqUrlappend': 'repository',
                'reqarg': ('loginName', 'page', 'publicPage', 'page_size', 'q'),
                'reqargdef': ('auth_username', '1', '1', '10', ''),

                'resp': 'commonImages',  # response json的key
                'respcolumndesc': ("name", "creationTime", "tagsCount"),
                'respcolumns': ("name", "creationTime", "tagsCount"),
            },

        'syncImage':  # 同步镜像 aimax add syncImage -F aaa
            {
                # %s/api/image/images/sync?token=%s&loginName=%s
                'addUrl': '/api/image/images/sync',
                'addarg': ('loginName'),
                'addargdef': ('auth_username'),

                # 'addarg':("repositoryName","imageName","tagName","message","success","totalSize"),
                # 'addargdef':('user_ray4',"nginx",["latest"],"","true",0),
                # 'addargdesc':("Please input sync Name: "),
                # body ImageShareInfo
                # 'body':{"totalSize":0,"imageName":"","tagName":[],"shareOfTag":[],
                #         "repositoryName":"","message":"","success":"true"},
                # 'bodyarg':("repositoryName","imageName","tagName"),
                # 'bodydesc':('Please input repositoryName(demo:user_ray4): ',
                #             'Please input imageName(demo:nginx): ',
                #             'Please input tagName(demo:latest,stable-alpine): '),
                # 'bodytype':("str","str","array"),
                # @RequestBody  ImageShareInfo
                'bodyjson': 'Please input ImageShareInfo json (demo: {"totalSize":0,"imageName":"nginx","tagName":["latest"],"shareOfTag":[],"repositoryName":"user_ray4","message":"","success":"true"}):',

            },

        'shareImage-bk':  # 分享镜像  aimax add shareImage -F aaa    #10
            {
                # "%s/api/image/images/share?token=%s",
                'addUrl': '/api/image/images/share',
                # body ImageShareInfo
                # 'body':{"totalSize":0,"imageName":"","tagName":[],"owner":"",
                #         "shareOfTag":[{"shareObjs":[{"shareRange":"group","shareTo":[]},
                #                       {"shareRange":"person","shareTo":["ray3"]},
                #                       {"shareRange":"all","shareTo":[]}],"tagName":"stable"}],
                #         "repositoryName":"","message":"","success":"true"},
                # 'bodyarg':("repositoryName","imageName","owner"#,"shareOfTag"
                #              ),
                # 'bodydesc':('Please input repositoryName(demo:ray4): ',
                #             'Please input imageName(demo:nginx): ',
                #             'Please input owner(demo:ray4): ',
                #             #'Please input shareOfTag(demo:latest,stable-alpine): '
                #             ),
                # 'bodytype':("str","str","str"),

                # @RequestBody  ImageShareInfo
                'bodyjson': 'Please input ImageShareInfo json (demo: {"totalSize":0,"imageName":"nginx","tagName":["stable"],"owner":"ray4","shareOfTag":[],"repositoryName":"ray4","message":"","success":"true"}):',

            },

        'shareImage':  # 分享镜像  aimax add shareImage -F aaa    #10
            {
                # "%s/api/image/images/share?token=%s",
                'addUrl': '/api/image/images/share',
                # body ImageShareInfo
                'bodyjson': 'Please input ImageShareInfo json (demo: {"totalSize":0,"imageName":"","tagName":[],"owner":"ray4","shareOfTag":[{"shareObjs":[{"shareRange":"group","shareTo":[]},{"shareRange":"person","shareTo":["ray3"]},{"shareRange":"all","shareTo":[]}],"tagName":"stable"}],"repositoryName":"ray4","message":"","success":"true"}):'
            },

        'shareObj':  # 获取共享对象 aimax list shareObj -F aaa  # 33
            {
                # 获取imagelist
                # %s/api/image/images/share/shareObj?token=%s&id=%s"
                'reqUrl': '/api/image/images/share/shareObj',
                'reqarg': ('id'),
                'reqargdef': (None),
                'reqargdesc': ("Please input id: "),

                'resp': 'shareOfTag',  # response json的key
                'respcolumndesc': ("tagName", "shareObjs"),
                'respcolumns': ("tagName", "shareObjs"),
            },

        'getShareImage':  # 查看某用户的分享镜像列表 aimax get getShareImage -F aaa # username: ray5
            {
                # 获取imagelist
                # "%s/api/image/images/share/%s?token=%s&page=%s",
                'getUrl': '/api/image/images/share',
                'getUrldesc': ("Please input username name: "),
                # 'reqUrlappend':'username',
                'getarg': ('page', 'page_size'),
                'getargdef': ('1', '10'),
                'getargdesc': ("", ""),

                # 'resp': 'shareInfos',  # response json的key
                # 'respcolumndesc': ("owner", "imageName", "repositoryName", "tagName"),
                # 'respcolumns': ("owner", "imageName", "repositoryName", "tagName"),
            },

        'cancelShare':  # 取消分享镜像 aimax del cancelShare -F aaa  #tagId
            {
                # "%s/api/image/images/share/cancelShare?token=%s&tagId=%s",
                'delUrl': '/api/image/images/share/cancelShare',
                # 'delUrldesc':("Please input imagename: "),
                'delarg': ('tagId'),
                'delargdef': (None),
                'delargdesc': ("Please input tagId: "),

                'delconfirm': "The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
            },

        'getImageByName':  # 根据名称 获取镜像 aimax get getImageByName -F aaa
            {
                # "%s/api/image/images/%s/tags?token=%s&isPublic=%s&repositoryName=%s&loginName=%s"
                # 获取imagelist
                'getUrl': '/api/image/images',
                'getUrldesc': ("Please input imageName : "),
                'getUrlappend': 'tags',
                'getarg': ('isPublic', 'repositoryName', 'loginName'),
                'getargdef': (None, None, 'auth_username'),
                'getargdesc': ("Please input isPublic(demo: 1 true 0 false) : ", "Please input repositoryName : ", ""),

                # 'resp': 'images',  # response json的key
                # 'respcolumndesc': ("name", "os", "size", "tagId"),
                # 'respcolumns': ("name", "os", "size", "tagId"),
            },

        'getImagesByProjectId':  # 根据项目id获取镜像 aimax list getImagesByProjectId -F aaa    #15
            {
                # "%s/api/image/images/%s/repository?token=%s&q=%s&page=%s&pageSize=%s"
                # 获取imagelist
                'reqUrl': '/api/image/images',
                'reqUrldesc': ("Please input username : "),
                'reqUrlappend': 'repository',
                'reqarg': ('q', 'page', 'pageSize'),
                'reqargdef': ('', '1', '10'),
                'reqargdesc': ("Please input isPublic : ", "Please input repositoryName : ", ""),

                'resp': 'commonImages',  # response json的key
                'respcolumndesc': ("projectId", "tagsCount", "name", "updateTime"),
                'respcolumns': ("projectId", "tagsCount", "name", "updateTime"),
            },

        'doNewTags':  # 打标签 aimax add doNewTags -F aaa
            {
                # ""%s/api/image/images/%s/tags?token=%s&tagName=%s&oldTag=%s&isPublic=%s&repositoryName=%s"",
                'addUrl': '/api/image/images',
                'addUrldesc': ("Please input imageName : "),
                'addUrlappend': 'tags',

                'addarg': ("tagName", "oldTag", "isPublic", "repositoryName"),
                'addargdef': (None, None, None, None),
                'addargdesc': ("Please input tagName: ", "Please input oldTag: ", "Please input isPublic: ",
                               "Please input repositoryName: "),

            },

        'uploadTarImage':  # 文件上传具体实现方法（单文件上传） aimax upload uploadTarImage -F aaa
            {
                # "%s/api/image/images/upload/tarfile?token=%s&imageName=%s&tagName=%s&isPublic=%s"
                'uploadUrl': '/api/image/images/upload/tarfile',

                'uploadarg': ("imageName", "tagName", "isPublic"),
                'uploadargdef': (None, None, None),
                'uploadargdesc': ("Please input imageName: ", "Please input tagName: ", "Please input isPublic: "),
                'uploadfilepath': ("Please input uploadfilepath (demo:/home/leihaibo/下载/TFServing.tar.gz): "),
                'uploadfilename': ("Please input uploadfilename : "),

            },

        'uploadDockfileImage':  # 上传dokcerfile    aimax upload uploadDockfileImage -F aaa
            {
                # %s/api/image/images/upload/dockerfile?token=%s&imageName=%s&tagName=%s&isPublic=%s
                'uploadUrl': '/api/image/images/upload/dockerfile',

                'uploadarg': ("imageName", "tagName", "isPublic"),
                'uploadargdef': (None, None, None),
                'uploadargdesc': ("Please input imageName: ", "Please input tagName: ", "Please input isPublic: "),
                'uploadfilepath': ("Please input uploadfilepath (demo:/home/leihaibo/下载/Dockerfile): "),
                'uploadfilename': ("Please input uploadfilename : "),
            },

        'deleteImage':  # 删除镜像 aimax del deleteImage -F aaa
            {
                # %s/api/image/images/%s/tags?token=%s&tagName=%s&isPublic=%s
                'delUrl': '/api/image/images',
                'delUrldesc': ("Please input imageName: "),
                'delUrlappend': ("tags"),
                'delarg': ('tagName', "isPublic"),
                'delargdef': (None, None),
                'delargdesc': ("Please input tagName: ", "Please input isPublic: "),
                'delconfirm': "The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"

            },

        'isContainerMaking':  # aimax get isContainerMaking -F aaa      #20
            {
                # %s/api/image/making/%s?token=%s
                'getUrl': '/api/image/making',
                'getUrldesc': ("Please input cid: "),
                'respcolumndesc': ("data", "count", "user", "imageShareInfo"),
                'respcolumns': ("data", "count", "user", "imageShareInfo"),
            },

        # storge=======================================================

        'createVolumes':  # aimax add createVolumes -F aaa
            {
                # %s/api/storage/volumes?token=%s
                'addUrl': '/api/storage/volumes',

                'addarg': ("count", "dataDisk", "volumeName", "volumeType"),
                'addargdef': (None, [], None, None),
                'addargdesc': ("Please input count: ", "Please input dataDisk: ", "Please input volumeName: ",
                               "Please input volumeType: "),

            },

        #########TODO 暂不支持 GLUSTER 接口返回无数据  另外此方法 要再调用listAllUsers
        'getVolumeInfo':  # 获取卷信息 aimax list getVolumeInfo -F aaa
            {
                # %s/api/storage/volumes/%s?token=%s   volumeName
                'reqUrl': '/api/storage/volumes',
                'reqUrldesc': ("Please input volumeName: "),

                'resp': 'publicImages',  # response json的key
                'respcolumndesc': ("name", "creationTime", "tagsCount"),
                'respcolumns': ("name", "creationTime", "tagsCount"),
            },

        'listVolumes': {  # aimax list listVolumes -F aaa
            # %s/api/storage/volumes?token=%s
            'reqUrl': '/api/storage/volumes',

            'resp': 'data',  # response json的key
            'respcolumndesc': ("name", "creationTime", "tagsCount"),
            'respcolumns': ("name", "creationTime", "tagsCount"),

        },

        'listDirs':  # 获取共享对象 aimax list listDirs -F aaa
            {
                # 获取imagelist
                # %s/api/storage/volumes/%s/dirs/%s?token=%s&path=%s
                'reqUrl': '/api/storage/volumes/@1@/dirs/@2@',
                'reqUrlReplaceAttr': ("Please input volumeName: ", 'Please input userFolder:'),
                'reqUrlReplace': ("@1@", '@2@'),
                'reqarg': ('path'),
                'reqargdef': (None),
                'reqargdesc': ("Please input path : "),

                'resp': 'shareOfTag',  # response json的key
                'respcolumndesc': ("tagName", "shareObjs"),
                'respcolumns': ("tagName", "shareObjs"),
            },

        'listNFSVolumes':  # 获取NFS卷 aimax put listNFSVolumes -F aaa
            {  # 25
                # %s/api/storage/nfsvolumes?token=%s
                'putUrl': '/api/storage/nfsvolumes',
                'putarg': ('listNFSVolumes'),
                'putargdef': ('listNFSVolumes_node_fun'),

                'resp': ('data'),  # response json的key
                'respcolumndesc': (
                    "address", "description", "attribute", "option", "shareDir", "mnt", "action", "external",
                    "volumeName",
                    'type', 'totalSpace', 'id', 'status', 'usablespace'),
                'respcolumns': (
                    "address", "description", "attribute", "option", "shareDir", "mnt", "action", "external",
                    "volumeName",
                    'type', 'totalSpace', 'id', 'status', 'usablespace'),
            },
        'listNFSVolumes_node_fun': {  # 获取  listNFSVolumes
            # "%s/api/node/nodes?token=%s&pageNum=%s&pageSize=%s
            # &nodeFlag=%s&keyWord=%s&gpucount=%s&cpucount=%s&latest=%s&status=%s&timer=%s
            # 获取imagelist
            'putUrl': '/api/node/nodes',
            'putarg': ('pageNum', 'pageSize'),
            # ,'nodeFlag','keyWord','gpucount','cpucount','latest','status','timer'),
            'putargdef': ('1', '10'),
            # "%s/api/image/images?token=%s&q=%s&page=%s&pageSize=%s&publicPage=%s&loginName=%s"
            'resp': ('obj', 'results'),  # response json的key
            'respcolumndesc': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),
            'respcolumns': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),
        },

        'getJobFileLocation':  # aimax get getJobFileLocation -F aaabbb注意用户有鉴权如果认证不过会403
            {
                # %s/api/storage/volumes/%s/dirs/%s/jobfilepath?token=%s&entryFile=%s&lib=%s
                'getUrl': '/api/storage/volumes/@1@/dirs/@2@/jobfilepath',
                'getUrlReplaceAttr': ("Please input volumeName: ", 'Please input userFolder:'),
                'getUrlReplace': ("@1@", '@2@'),

                'getarg': ('entryFile', 'lib'),
                'getargdef': (None, None),
                'getargdesc': ("Please input entryFile: ", "Please input lib: "),
            },

        'getShareData': {  # aimax get getShareData -F aaabbb注意用户有鉴权如果认证不过会403

            # %s/api/storage/volumes/%s/dirs/%s/share?token=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/share',
            'getUrlReplaceAttr': ("Please input volumeName: ", 'Please input userFolder:'),
            'getUrlReplace': ("@1@", '@2@'),
        },

        'getShareObjs': {  # aimax get getShareObjs -F aaabbb注意用户有鉴权如果认证不过会403

            # %s/api/storage/volumes/%s/dirs/%s/shareObj?token=%s&id=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/shareObj',
            'getUrlReplaceAttr': ("Please input volumeName: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),

            'getarg': ('id'),
            'getargdef': (None),
            'getargdesc': ("Please input id: "),
        },

        'getShareDataOpInfo': {  # aimax get getShareDataOpInfo -F aaa         #30
            # %s/api/storage/volumes/%s/dirs/shareDataOpInfo?token=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/shareDataOpInfo',
            'getUrlReplaceAttr': ("Please input volumeName: "),
            'getUrlReplace': ("@1@"),

        },

        'getDecompressInfo': {  # aimax get getDecompressInfo -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/decompressInfo?token=%s&path=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/decompressInfo',
            'getUrlReplaceAttr': ("Please input volumeName: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),
            'getarg': ('path'),
            'getargdef': (None),
            'getargdesc': ("Please input path: "),
        },

        'cancelDecompress': {  # aimax get cancelDecompress -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/cancelDecompress?token=%s&path=%s&fileName=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/cancelDecompress',
            'getUrlReplaceAttr': ("Please input volumeName: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),
            'getarg': ('path', 'fileName'),
            'getargdef': (None, None),
            'getargdesc': ("Please input path: ", "Please input fileName: "),
        },

        'getMyShareData': {  # aimax get getMyShareData -F
            # %s/api/storage/volumes/%s/dirs/%s/myShare?token=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/myShare',
            'getUrlReplaceAttr': ("Please input volumes: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),
        },

        'copyShareData': {  # aimax get copyShareData -F
            # %s/api/storage/volumes/%s/dirs/%s/copyShare
            # ?token=%s&destPathStr=%s&ownerVolume=%s&owner=%s&srcPathStr=%s&fileName=%s&isDir=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/copyShare',
            'getUrlReplaceAttr': ("Please input volumes: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),

            'getarg': ('destPathStr', 'ownerVolume', 'owner', 'srcPathStr', 'fileName', 'isDir'),
            'getargdef': (None, None, None, None, None, None),
            'getargdesc': ("Please input destPathStr: ", "Please input ownerVolume: ", "Please input owner: ",
                           "Please input srcPathStr: ", "Please input fileName: ", "Please input isDir: "),
        },

        'getFileInfo': {  # aimax get getFileInfo -F
            # %s/api/storage/volumes/%s/dirs/%s/detail?token=%s&path=%s&fileName=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/detail',
            'getUrlReplaceAttr': ("Please input volumes: ", 'Please input dirs:'),
            'getUrlReplace': ("@1@", '@2@'),

            'getarg': ('path', 'fileName'),
            'getargdef': (None, None),
            'getargdesc': ("Please input path: ", "Please input fileName: "),
        },

        'getPrivateVol': {  # aimax get getPrivateVol -F bbb
            # %s/api/storage/volumes/%s/user?token=%s&username=%s
            'getUrl': '/api/storage/volumes/@1@/user',
            'getUrlReplaceAttr': ("Please input volumes: "),
            'getUrlReplace': ("@1@"),

            'getarg': ('username'),
            'getargdef': (None),
            'getargdesc': ("Please input username: "),

        },

        'deleteDirs': {  # aimax del deleteDirs -F bbb
            # %s/api/storage/volumes/%s/dirs/%s?token=%s
            'delUrl': '/api/storage/volumes/@1@/dirs/@2@',
            'delUrlReplaceAttr': ("Please input volumeName: ", 'Please input dirs:'),
            'delUrlReplace': ("@1@", '@2@'),
            'delconfirm': "The volumes dirs  {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n",

            # 'delbody':([{"fileName":"1","id":0,"share":0}]),
            # @RequestBody List<FileDelInfo>
            'bodyjson': 'Please input List<FileDelInfo> json (demo: [{"fileName":"1","id":0,"share":0}]):',

        },

        'tagDeletedForHomeDir': {  # aimax del tagDeletedForHomeDir -F aaa
            # %s/api/storage/volumes/dirs/%s/delete?token=%s
            'delUrl': '/api/storage/volumes/dirs/@1@/delete',
            'delUrlReplaceAttr': ('Please input dirs:'),
            'delUrlReplace': ("@1@"),
            'delconfirm': "The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n",
            # body User
            # 'delbody':({"count":0,"id":123456,"message":"","success":'true',"totalSize":0}),
            # 'bodyjson':'Please input List<FileDelInfo> json (demo: [{"fileName":"1","id":0,"share":0}])'
            # @RequestBody User
            'bodyjson': 'Please input User json (demo: {"count":0,"message":"","success":true,"totalSize":0,"username":"username123","volumeName":""}):'

        },

        'createNFSVolumes': {  # aimax post createNFSVolumes -F aaa
            # %s/api/storage/nfsvolumes?token=%s
            'addUrl': '/api/storage/nfsvolumes',

            # @RequestBody StorageInfo
            # 'body':({"external":'false',"volumeName":"asdasdas"}),
            'bodyjson': 'Please input StorageInfo json (demo: {"external":"false","volumeName":"asdasdas"}):'

            # Integer id;String volumeName;String address;String type;     //gluster,nfs,local
            # boolean external; //0代表内部数据  1代表外部数据String mnt;      // 節點掛載點
            # String shareDir; //共享目錄String action;   //mount  /start   /ok     /delete  /deleted    下一步需要執行的動作
            # String status;   //Created/Mounting/Started/Deleting/Deleted     當前狀態String usablespace;
            # String totalSpace;String attribute;String option; String description;

        },

        'createFolder': {  # aimax post createFolder -F aaa             #40
            # %s/api/storage/volumes/%s/dirs?token=%s
            'addUrl': '/api/storage/volumes/@1@/dirs',
            'addUrlReplaceAttr': ('Please input volumes:'),
            'addUrlReplace': ("@1@"),
            # @RequestBody FolderInfo
            # 'body':({"attr":"attr","fileName":"filename","path":"path"}),
            'bodyjson': 'Please input FolderInfo json (demo: {"attr":"attr","fileName":"filename","path":"path"}):'

        },

        'uploadvolumes':  # 上传dokcerfile    aimax upload uploadvolumes -F aaa
            {
                # %s/zuul/s/api/storage/volumes/%s/dirs/%s
                # ?token=%s&path=%s&fileName=%s&sameUpload=%s&fileSize=%s&sliceCurrent=%s&uuid=%s
                'uploadUrl': '/api/storage/volumes/@1@/dirs/@2@',
                'uploadUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
                'uploadUrlReplace': ("@1@", "@2@"),
                # 'uploadUrlReplacedef':("134nfs","common"),
                'uploadarg': ("path", "fileName", "sameUpload", "fileSize", "sliceCurrent", "uuid"),
                'uploadargdef': ('', 'Dockerfile', 'false', 'file_Size', 0, ''),
                'uploadargdesc': ("Please input path: ", "Please input fileName: ", "Please input sameUpload: ",
                                  "Please input fileSize: ", "Please input sliceCurrent: ", "Please input uuid: "),
                'uploadfilepath': ("Please input uploadfilepath (demo:/home/leihaibo/下载/Dockerfile): "),
                'uploadfilename': ("Please input uploadfilename : "),

            },

        'downloadvolumes': {  # TODO 目前前台使用 FTP 直接获取 不走api 此接口 aimax download downloadvolumes -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/download?token=%s&path=%s&fileName=%s

            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/download',  # public/dirs/common
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试

            'getarg': ('path', 'fileName'),
            'getargdef': ('', 'Dockerfile'),
            'getargdesc': ("Please input path: ", "Please input fileName: "),

        },

        'downloadBigFile': {  # aimax download downloadBigFile -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/download?token=%s&path=%s&beginIndex=%s&endIndex=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/download',  # public/dirs/common
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试

            'getarg': ('path', 'beginIndex', 'endIndex'),
            'getargdef': (None, None, None),
            'getargdesc': ("Please input path: ", "Please input beginIndex: ", "Please input endIndex: "),
        },

        'zipFolder': {  # aimax download zipFolder -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/zip?token=%s&path=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/zip',
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
            'getarg': ('path'),
            'getargdef': (None),
            'getargdesc': ("Please input path: "),
        },

        'unzipFolder':  # 获取NFS卷 aimax put unzipFolder -F aaa
            {
                # %s/api/storage/volumes/%s/dirs/%s/unzip?token=%s&path=%s&fileName=%s
                'putUrl': '/api/storage/volumes/@1@/dirs/@2@/unzip',
                'putUrlReplaceAttr': ('Please input volumes(demo:134nfs):', 'Please input dirs(demo:common):'),
                'putUrlReplace': ("@1@", "@2@"),
                # 'putUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试

                'putarg': ('path', 'fileName', 'unzipFolder_node_fun'),
                #'putargdef': ('common','src.tar.gz','unzipFolder_node_fun'),  # path=common&fileName=src.tar.gz
                'putargdef': (None,None,'unzipFolder_node_fun'),
                # &type=public
                'putargdesc': ("Please input path: ", "Please input fileName: "),

                # 'resp': ('obj','results'),  # response json的key
                # 'respcolumndesc': (
                #     "address", "description", "attribute", "option", "shareDir", "mnt", "action", "external",
                #     "volumeName",
                #     'type', 'totalSpace', 'id', 'status', 'usablespace'),
                # 'respcolumns': (
                #     "address", "description", "attribute", "option", "shareDir", "mnt", "action", "external",
                #     "volumeName",
                #     'type', 'totalSpace', 'id', 'status', 'usablespace'),
            },
        'unzipFolder_node_fun': {  # 获取   aimax put listNFSVolumes -F aaa
            # "%s/api/node/nodes?token=%s&pageNum=%s&pageSize=%s
            # &nodeFlag=%s&keyWord=%s&gpucount=%s&cpucount=%s&latest=%s&status=%s&timer=%s
            # 获取imagelist
            'putUrl': '/api/node/nodes',
            'putarg': ('pageNum', 'pageSize'),
            # ,'nodeFlag','keyWord','gpucount','cpucount','latest','status','timer'),
            'putargdef': ('1', '10'),
            # "%s/api/image/images?token=%s&q=%s&page=%s&pageSize=%s&publicPage=%s&loginName=%s"
            'resp': ('obj', 'results'),  # response json的key
            'respcolumndesc': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),
            'respcolumns': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),
        },

        'progress': {  # TODO 不用实现了 之前用于查询下载的的进度 目前该webclient实现 aimax get progress -F aaa
            # "%s/api/storage/volumes/%s/dirs/%s/progress?token=%s&path=%s&fileName=%s"
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/progress',
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
            'getarg': ('path', 'fileName'),
            'getargdef': (None, None),
            'getargdesc': ("Please input path: ", "Please input filename: "),
        },

        'copyData': {  # aimax get copyData -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/copy?token=%s&srcPathStr=%s&fileName=%s&destPathStr=%s&isDir=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/copy',
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
            'getarg': ('srcPathStr', 'fileName', 'destPathStr', 'isDir'),
            'getargdef': (None, None, None, None),
            # 'getargdef':('','Dockerfile','','false'),
            'getargdesc': ("Please input path: ", "Please input filename: "
                           , "Please input destPathStr: ", "Please input isDir (type boolean): "),

        },

        'moveData': {  # aimax get moveData -F aaa
            # %s/api/storage/volumes/%s/dirs/%s/move
            # ?token=%s&srcPathStr=%s&fileName=%s&destPathStr=%s&isDir=%s&id=%s&share=%s
            'getUrl': '/api/storage/volumes/@1@/dirs/@2@/move',
            'getUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
            'getarg': ('srcPathStr', 'fileName', 'destPathStr', 'isDir', 'id', 'share'),
            'getargdef': (None, None, None, 'false', 0, 0),
            'getargdesc': ("Please input path: ", "Please input filename: "
                           , "Please input destPathStr: ", "Please input isDir (type boolean): "
                           , "Please input id: ", "Please input share: "),
        },

        'listBricks': {  # gluster TODO 转块 暂不实现#50

        },
        'expandeVolume': {  # gluster TODO 转块 暂不实现

        },

        'shareData': {  # aimax post shareData -F ray5
            # %s/api/storage/volumes/%s/dirs/%s/share?token=%s
            'addUrl': '/api/storage/volumes/@1@/dirs/@2@/share',
            'addUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'addUrlReplace': ("@1@", "@2@"),
            # 'addUrlReplacedef':('134nfs','ray5'),
            # @RequestBody FileShareInfo
            # 'body':({"dir":'false',"fileName":"Dockerfile","id":0,"imgUrl":"",'owner':'ray5',"shareObjs":[{'shareRange':'group',"shareTo":[]}, {'shareRange':'person',"shareTo":["ray3"]},{'shareRange':'all',"shareTo":[]}],"volumeName":"134nfs"}),
            'bodyjson': 'Please input FileShareInfo json (demo: {"dir":"false","fileName":"Dockerfile","id":0,"imgUrl":"","owner":"ray5","shareObjs":[{"shareRange":"group","shareTo":[]}, {"shareRange":"person","shareTo":["ray3"]},{"shareRange":"all","shareTo":[]}],"volumeName":"134nfs"}):'
        },

        'cancleShareData':  # 取消分享 aimax del cancleShareData -F ray5  #tagId
            {
                # "%s/api/storage/volumes/%s/dirs/%s/cancleShare?token=%s&id=%s",
                'delUrl': '/api/storage/volumes/@1@/dirs/@2@/cancleShare',
                'delUrlReplaceAttr': ("Please input volumeName: ", 'Please input dirs:'),
                'delUrlReplace': ("@1@", '@2@'),
                # 'delUrlReplacedef':("134nfs",'common'),
                'delarg': ('id'),
                'delargdef': (None),
                'delargdesc': ("Please input id: "),
                'delconfirm': "The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
            },

        'rename': {  # aimax put rename -F ray5
            # %s/api/storage/volumes/%s/dirs/%s/rename?token=%s

            'putUrl': '/api/storage/volumes/@1@/dirs/@2@/rename',
            'putUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
            'putUrlReplace': ("@1@", "@2@"),
            # 'putUrlReplacedef':('134nfs','ray5'),#用于预置替换参数 一般用于测试
            #'putbody': ({"oldFileName": "Dockerfile", "newFileName": "Dockerfile1", "path": "","share": "0", "id": "0", "type": "private", }),
            #@RequestBody FileRenameInfo
            'bodyjson': 'Please input FileRenameInfo json (demo: {"oldFileName": "Dockerfile", "newFileName": "Dockerfile1", "path": "","share": "0", "id": "0", "type": "private"}):',

            'resp': ('data'),  # response json的key
            # 'respcolumndesc':("address","description","attribute","option","shareDir","mnt","action","external","volumeName", 'type', 'totalSpace', 'id', 'status', 'usablespace'),
            # 'respcolumns':("address","description","attribute","option","shareDir","mnt","action","external","volumeName", 'type', 'totalSpace', 'id', 'status', 'usablespace'),
        },

        'setFilePermission':  # job 时调用 aimax put setFilePermission -F aaa
            {
                # %s/api/storage/volumes/%s/dirs/%s/chmod?token=%s
                'putUrl': '/api/storage/volumes/@1@/dirs/@2@/chmod',
                'putUrlReplaceAttr': ('Please input volumes:', 'Please input dirs:'),
                'putUrlReplace': ("@1@", "@2@"),
                # 'putUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
                # 'putargdesc':("Please input path: ","Please input fileName: "),
                #'putbody': ({"path": "path", "attr": "attr", "path": "", "fileName": "fileName"}),

                #@RequestBody FileRenameInfo
                'bodyjson': 'Please input FolderInfo json (demo: {"path": "path", "attr": "attr", "path": "", "fileName": "fileName"} ):',

                'resp': ('data'),  # response json的key
            },

        'createUserFolder': {  # aimax post createUserFolder -F aaa
            'addUrl': '/api/storage/volumes/dirs/homedir',
            # @RequestBody UserQuota
            # 'body':({"id":0,'userId':0,'cpu':0,'gpu':0,'internalMemory':'','dataStorage':'','taskNumber':'','isDefault':0,'':'','username':'','volumeName':'','gputype':''}),

            'bodyjson': 'Please input UserQuota json (demo: {"id":0,"userId":0,"cpu":0,"gpu":0,"internalMemory":"","dataStorage":"","taskNumber":"","isDefault":0,"":"","username":"","volumeName":"","gputype":""}):'

        },

        'updateVolumeQuota': {  # aimax put updateVolumeQuota -F aaa
            # %s/api/storage/volumes/%s/quota?token=%s
            'putUrl': '/api/storage/volumes/@1@/quota',
            'putUrlReplaceAttr': ('Please input volumes:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试

            # @RequestBody UserQuota
            # 'putbody':({"id":0,'userId':0,'cpu':0,'gpu':0,'internalMemory':'','dataStorage':'','taskNumber':'','isDefault':0,'':'','username':'','volumeName':'','gputype':''}),
            'bodyjson': 'Please input UserQuota json (demo: {"id":0,"userId":0,"cpu":0,"gpu":0,"internalMemory":"","dataStorage":"","taskNumber":"","isDefault":0,"":"","username":"","volumeName":"","gputype":""}):',

            'resp': ('data'),  # response json的key

        },

        # 'tagDeletedForHomeDir':{# aimax del tagDeletedForHomeDir -F aaa
        #     #%s/api/storage/volumes/dirs/%s/delete?token=%s
        #     'delUrl':'/api/storage/volumes/dirs/@1@/delete',
        #     'delUrlReplaceAttr':('Please input dirs:'),
        #     'delUrlReplace':("@1@"),
        #     'delbody':({"count":0,"message":"","success":'true',"totalSize":0,"username":"username"}),#User
        #
        #     'delconfirm':"The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
        #
        # },

        # job

        'createJob': {  # aimax post job -F aaa
            # %s/api/job/jobs?token=%s
            'addUrl': '/api/job/jobs',
            # @RequestBody JobInfoList
            # 'body':({"attr":"attr","fileName":"filename","path":"path"}),
            'bodyjson': 'Please input JobInfoList json (demo: {"attr":"attr","fileName":"filename","path":"path"}):',

        },

        'createDeployment': {  # aimax post createDeployment -F aaa             #60
            # %s/api/job/deployments?token=%s
            'addUrl': '/api/job/deployments',
            # @RequestBody JobInfo
            # 'body':({"attr":"attr","fileName":"filename","path":"path"}),
            'bodyjson': 'Please input JobInfo json (demo: {"attr":"attr","fileName":"filename","path":"path"}):',

        },

        'listjob': {  # aimax list listjob -F aaa
            # %s/api/job/jobs?token=%s&
            # owner=%s&zoneName=%s&jobName=%s&image=%s&status=%s&state=%s
            # &startFrom=%s&startTo=%s&endFrom=%s&endTo=%s&pageSize=%s
            # &pageNum=%s&history=%s&page=%s&filter=%s&visual=%s
            # owner=ray4&zoneName=&image=&status=[%22Running%22]&state=&startFrom=&startTo=&endFrom=&endTo=&appType=job&pageSize=10&pageNum=1&jobName=
            'reqUrl': '/api/job/jobs',
            'reqarg': ('owner', 'zoneName', 'jobName', 'image', 'status', 'state', 'startFrom', 'startTo', 'endFrom',
                       'endTo', 'pageSize', 'pageNum', 'history', 'page', 'filter', 'visual'),
            'reqargdef': ('', '', '', '', '', '', '', '', '',
                          '', '100', '1', 'true', 'true', 'true', 'false'),
            'reqargdesc': ("Please input path : "),
            'resp': 'jobs',  # response json的key
            'respcolumndesc': ("jobName", "owner", "zoneName"),
            'respcolumns': ("jobName", "owner", "zoneName"),
        },

        'listDeployment': {  # 获取模型部署列表 aimax list listDeployment -F ray4
            # %s/api/job/deployments?token=%s&
            # owner=%s&zoneName=%s&jobName=%s&image=%s&status=%s&state=%s&appType=%s
            # &startFrom=%s&startTo=%s&endFrom=%s&endTo=%s&pageSize=%s
            # &pageNum=%s&%s&page=%s&filter=%s&visual=%s
            # owner=ray4&zoneName=&image=&status=[%22Running%22]&state=&startFrom=&startTo=&endFrom=&endTo=&appType=job&pageSize=10&pageNum=1&jobName=
            'reqUrl': '/api/job/jobs',
            'reqarg': ('owner', 'zoneName', 'jobName', 'image', 'status', 'state', 'appType',
                       'startFrom', 'startTo', 'endFrom', 'endTo', ''
                                                                   'pageSize', 'pageNum', 'page', 'filter', 'visual'),
            'reqargdef': (None, '', '', '', '', '', None,
                          '', '', '', '',
                          '100', '1', 'false', 'false', 'false'),
            'reqargdesc': ("Please input owner : ", 'zoneName', 'jobName', 'image', 'status', 'state',
                           "Please input appType (demo: job/visual/model/interactive): "),
            'resp': 'jobs',  # response json的key
            'respcolumndesc': ("jobName", "owner", "zoneName"),
            'respcolumns': ("jobName", "owner", "zoneName"),
        },

        'jobinfo': {  # aimax get jobinfo -F aaa   1 job18441 zone1
            # %s/api/job/jobs/%s/%s?token=%s&zoneName=%s
            'getUrl': '/api/job/jobs/@1@/@2@',
            'getUrlReplaceAttr': ('Please input uid  :', 'Please input jobName:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
            'getarg': ('zoneName'),
            'getargdef': (None),
            'getargdesc': ("Please input zoneName: "),
        },

        'getgpuList': {  # 创建任务前 获取 gpu类型列表 aimax list getgpuList -F aaa
            # %s/api/job/jobs/gputype?token=%s
            'reqUrl': '/api/job/jobs/gputype',
            # 'resp': 'gputypes',  # response json的key
            # 'respcolumndesc':("jobName","owner","zoneName"),
            # 'respcolumns':("jobName","owner","zoneName"),
        },

        'getErrorInfo': {  # aimax get getErrorInfo -F user
            # %s/api/job/jobs/%s/%s/error?token=%s
            'getUrl': '/api/job/jobs/@1@/@2@/error',
            'getUrlReplaceAttr': ('Please input uid  :', 'Please input jobName:'),
            'getUrlReplace': ("@1@", "@2@"),
            # 'getUrlReplacedef':('134nfs','common'),#用于预置替换参数 一般用于测试
        },

        'getErrorList': {  # aimax list getErrorList -F aaa
            # %s/api/job/jobs/%s/%s/errorList?token=%s
            'reqUrl': '/api/job/jobs/@1@/@2@/errorList',
            'reqUrlReplaceAttr': ('Please input uid  :', 'Please input jobName:'),
            'reqUrlReplace': ("@1@", "@2@"),
            # 'reqUrlReplacedef':('2739d614-462e-40c9-9e1b-e4f30dc7d07c','tensorflowserving75689'),#用于预置替换参数 一般用于测试

            # 'resp': 'jobErrors',  # response json的key
            # 'respcolumndesc': ("createTime", "errorReason", "errorType", 'errorMessage'),
            # 'respcolumns': ("createTime", "errorReason", "errorType", 'errorMessage'),

        },
        'getPredictResult': {  # aimax post getPredictResult -F aaa
            # %s/api/job/models/%s/predict?token=%s
            'addUrl': '/api/job/models/@1@/predict',
            'addUrlReplaceAttr': ('Please input jobName:'),
            'addUrlReplace': ("@1@"),  # tensorflowserving44205
            # @RequestBody ModelInputInfo
            # 'body':({"inputVal":"","kubeServiceIp":"10.200.46.168","kubeServicePort":"25675",'modelName': "/",'signatureN':''}),
            'bodyjson': 'Please input ModelInputInfo json (demo: {"inputVal":"","kubeServiceIp":"10.200.46.168","kubeServicePort":"25675","modelName": "/","signatureN":""}):',

        },
        'getInputParameterSample': {  # 模型部署时 测试 aimax get getInputParameterSample -F aaa
            # %s/api/job/models/inputParameterSample?token=%s&kubeServiceIp=%s&kubeServicePort=%s&modelName=%s
            # kubeServiceIp=10.200.67.77&kubeServicePort=25089&modelName=
            'getUrl': '/api/job/models/inputParameterSample',
            'getarg': ('kubeServiceIp', 'kubeServicePort', 'modelName'),
            'getargdef': (None, None, ''),
            'getargdesc': (
                "Please input kubeServiceIp: (demo:10.200.67.77)", "Please input kubeServicePort:(demo 25089) "),
        },
        'generateImageFromContainer': {  # aimax post generateImageFromContainer -F aaa
            # %s/api/job/containerToImage?token=%s
            'addUrl': '/api/job/containerToImage',
            # @RequestBody SnapshotInfo
            # 'body':({"jobName":"","repositoryName":"","imageName":"",'tagName': "",'zoneName':'','owner':'','uid':''}),
            'bodyjson': 'Please input SnapshotInfo json (demo: {"jobName":"","repositoryName":"","imageName":"","tagName": "","zoneName":"","owner":"","uid":""}):',

        },
        'getJobSaveImgInfo': {  # aimax get getJobSaveImgInfo -F aaa #70
            # %s/api/job/event/saveImage?token=%s&owner=%s&zoneName=%s&appType=%s
            'getUrl': '/api/job/event/saveImage',
            'getarg': ('owner', 'zoneName', 'appType'),
            'getargdef': (None, None, None),
            'getargdesc': ("Please input owner:", "Please input zoneName:", "Please input appType:(demo: job/visual/model/interactive)"),

        },
        'getJobLog': {  # aimax get getJobLog -F aaa
            # %s/api/job/jobs/%s/log?token=%s&zoneName=%s&offset=%d&maxFetchedLineNum=%d&size=%d
            'getUrl': '/api/job/jobs/@1@/log',
            'getUrlReplaceAttr': ('Please input jobName  :'),
            'getUrlReplace': ("@1@"),
            'getarg': ('zoneName', 'offset', 'maxFetchedLineNum', 'size'),
            'getargdef': (None, None, None, None),
            'getargdesc': ("Please input zoneName:", "Please input offset:",
                           "Please input maxFetchedLineNum:", "Please input size:"),
        },
        'getNodeTaintStatus': {  # aimax get getNodeTaintStatus -F aaa
            # %s/api/job/nodes/taint/status?token=%s
            'getUrl': '/api/job/nodes/taint/status',
        },
        'listPods': {  # aimax get listPods -F aaa TODO 测试用的接口
            # %s/api/job/pods?token=%s&nodeName=%s
            'getUrl': '/api/job/pods',
            'getarg': ('nodeName'),
            'getargdef': (None),
            'getargdesc': ("Please input nodeName: "),

            'resp': ('pods'),  # response json的key
            # 'respcolumndesc':("data","count","user","imageShareInfo"),
            # 'respcolumns':("data","count","user","imageShareInfo"),
        },
        'getNodeAllocatable': {  # aimax get getNodeAllocatable -F aaa TODO 未找到controller的实现
            # %s/api/job/node/%s?token=%s
            'getUrl': '/api/job/node',
            'getUrldesc': ("Please input imageName: "),

        },

        'removeJob': {  # aimax del removeJob -F aaa
            # %s/api/job/jobs/%s?token=%s&zoneName=%s
            'delUrl': '/api/job/jobs/@1@',
            'delUrlReplaceAttr': ('Please input uid:'),
            'delUrlReplace': ("@1@"),
            'delarg': ('zoneName'),
            'delargdef': (None),
            'delargdesc': ("Please input zoneName: "),
            # 'delbody':({"count":0,"message":"","success":'true',"totalSize":0,"username":"username"}),#User
            'delconfirm': "The job id {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
        },

        'removeDeploymentAndSVC': {  # aimax del removeDeploymentAndSVC -F aaa
            # %s/api/job/deployments/%s?token=%s&zoneName=%s
            'delUrl': '/api/job/deployments/@1@',
            'delUrlReplaceAttr': ('Please input uid:'),
            'delUrlReplace': ("@1@"),
            'delarg': ('zoneName'),
            'delargdef': (None),
            'delargdesc': ("Please input zoneName: "),
            # 'delbody':({"count":0,"message":"","success":'true',"totalSize":0,"username":"username"}),#User
            'delconfirm': "The deployments id {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
        },

        'pause': {  # aimax put pause -F aaa
            # %s/api/job/jobs/%s/pause?token=%s&zoneName=%s
            'putUrl': '/api/job/jobs/@1@/pause',
            'putUrlReplaceAttr': ('Please input uid:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('zoneName'),
            'putargdef': (None),
            'putargdesc': ('Please input zoneName:'),

            # @RequestBody ZoneInfo
            # 'putbody': (
            #     # {"jobType":"ML","message":"",
            #     #         "quotas":{"MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
            #     #            "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
            #     #            "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
            #     #            "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},
            #     #         "success":'true',"totalSize":0},
            #     {"jobType": "ML", "message": "", "quotas": {}, "success": 'true', "totalSize": 0}
            # ),

            #@RequestBody ZoneInfo
            'bodyjson': 'Please input ZoneInfo json (demo: {"name":"","jobType":"ML","desc":"","quotas":{},"message":"","success":true,"totalSize":0}):',

        },

        'resume': {  # aimax put resume -F aaa
            # %s/api/job/jobs/%s/resume?token=%s&zoneName=%s
            'putUrl': '/api/job/jobs/@1@/resume',
            'putUrlReplaceAttr': ('Please input uid:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('zoneName'),
            'putargdef': (None),
            'putargdesc': ('Please input zoneName:'),

            # @RequestBody ZoneInfo
            # 'putbody': (
            #     # {"jobType":"ML","message":"",
            #     #         "quotas":{"MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
            #     #            "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
            #     #            "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
            #     #            "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},
            #     #         "success":'true',"totalSize":0},
            #     {"jobType": "ML", "message": "", "quotas": {}, "success": 'true', "totalSize": 0}
            # ),
            #@RequestBody ZoneInfo
            'bodyjson': 'Please input ZoneInfo json (demo: {"name":"","jobType":"ML","desc":"","quotas":{},"message":"","success":true,"totalSize":0}):',

        },

        'pauseDeployment': {  # aimax put pauseDeployment -F aaa
            # %s/api/job/deployments/%s/pause?token=%s&zoneName=%s
            'putUrl': '/api/job/deployments/@1@/pause',
            'putUrlReplaceAttr': ('Please input uid:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('zoneName'),
            'putargdef': (None),
            'putargdesc': ('Please input zoneName:'),

            # @RequestBody ZoneInfo
            # 'putbody': (
            #     # {"jobType":"ML","message":"",
            #     #         "quotas":{"MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
            #     #            "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
            #     #            "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
            #     #            "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},
            #     #         "success":'true',"totalSize":0},
            #     {"jobType": "ML", "message": "", "quotas": {}, "success": 'true', "totalSize": 0}
            # ),
            #@RequestBody ZoneInfo
            'bodyjson': 'Please input ZoneInfo json (demo: {"name":"","jobType":"ML","desc":"","quotas":{},"message":"","success":true,"totalSize":0}):',

        },

        'resumeDeployment': {  # aimax put resumeDeployment -F aaa    #80
            # %s/api/job/deployments/%s/resume?token=%s&zoneName=%s
            'putUrl': '/api/job/deployments/@1@/resume',
            'putUrlReplaceAttr': ('Please input uid:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('zoneName'),
            'putargdef': (None),
            'putargdesc': ('Please input zoneName:'),

            # @RequestBody ZoneInfo
            # 'putbody': (
            #     # {"jobType":"ML","message":"",
            #     #         "quotas":{"MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
            #     #            "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
            #     #            "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
            #     #            "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}},
            #     #         "success":'true',"totalSize":0},
            #     {"jobType": "ML", "message": "", "quotas": {}, "success": 'true', "totalSize": 0}
            # ),
            #@RequestBody ZoneInfo
            'bodyjson': 'Please input ZoneInfo json (demo: {"name":"","jobType":"ML","desc":"","quotas":{},"message":"","success":true,"totalSize":0}):',

        },

        'unschedule': {  # aimax put unschedule -F aaa
            # %s/api/job/nodes/%s/unschedule?token=%s&nodeIp=%s
            'putUrl': '/api/job/nodes/@1@/unschedule',
            'putUrlReplaceAttr': ('Please input nodeName:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('nodeIp'),
            'putargdef': (None),
            'putargdesc': ('Please input nodeIp:'),

            # @RequestBody null
            'putbody': (),

        },

        'schedule': {  # aimax put schedule -F aaa
            # %s/api/job/nodes/%s/schedule?token=%s&nodeIp=%s"
            'putUrl': '/api/job/nodes/@1@/schedule',
            'putUrlReplaceAttr': ('Please input nodeName:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('nodeIp'),
            'putargdef': (None),
            'putargdesc': ('Please input nodeIp:'),

            # @RequestBody null
            'putbody': (),
        },
        'unschedule': {  # aimax put unschedule -F aaa
            # %s/api/job/nodes/%s/unschedule?token=%s&nodeIp=%s"
            'putUrl': '/api/job/nodes/@1@/unschedule',
            'putUrlReplaceAttr': ('Please input nodeName:'),
            'putUrlReplace': ("@1@"),
            # 'putUrlReplacedef':('134nfs1'),#用于预置替换参数 一般用于测试
            'putarg': ('nodeIp'),
            'putargdef': (None),
            'putargdesc': ('Please input nodeIp:'),

            # @RequestBody null
            'putbody': (),
        },

        'createTemplate': {  # aimax post createTemplate -F aaa
            # %s/api/job/templates?token=%s
            'addUrl': '/api/job/templates',
            # @RequestBody TemplateInfo
            # 'body':({}),
            'bodyjson': 'Please input TemplateInfo json (demo: {}):',

        },

        'getTemplate': {  # aimax get getTemplate -F ray4  template35478
            # %s/api/job/templates/%s?token=%s
            'getUrl': '/api/job/templates',
            'getUrldesc': ("Please input templateName: "),
        },

        'delTemplate': {  # aimax del delTemplate -F ray4 #软删除 只是改了状态位0变1
            # %s/api/job/templates/%s?token=%s
            'delUrl': '/api/job/templates',
            'delUrldesc': ("Please input templateName:"),
            # 'delbody':({"count":0,"message":"","success":'true',"totalSize":0,"username":"username"}),#User
            'delconfirm': "The deployments id {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"
        },

        'updateTemplate': {  # aimax put updateTemplate -F aaa
            # %s/api/job/templates/%s?token=%s
            'putUrl': '/api/job/templates',
            'putUrldesc': ('Please input templateName:'),
            # @RequestBody TemplateInfo
            #'putbody': ({}),  #
            'bodyjson': 'Please input TemplateInfo json (demo: {}):',

        },

        'getTemplateList': {  # aimax list getTemplateList -F ray4
            # %s/api/job/templates?appType=%s&token=%s
            'reqUrl': '/api/job/templates',
            # 'getUrlReplaceAttr':('Please input appType:'),
            # 'getUrlReplace':("@1@"),
            'reqarg': ('appType'),
            'reqargdef': (None),
            'reqargdesc': ("Please input appType(demo: job/visual/model/interactive):"),

            'resp': ('data'),  # response json的key
            'respcolumndesc': ("templateName", "appType", "imageTag", "createTime"),
            'respcolumns': ("templateName", "appType", "imageTag", "createTime"),

        },

        'getVisualInfoList': {  #根据用户和任务名获取可视化任务 aimax list getVisualInfoList -F ray4
            # %s/api/job/visuals?token=%s&owner=%s&jobName=%s&pageNum=%s&pageSize=%s

            'reqUrl': '/api/job/visuals',
            'reqarg': ('owner', 'jobName', 'pageNum', 'pageSize'),
            'reqargdef': (None, None, 1, 100),
            'reqargdesc': ("Please input owner: ", "Please input jobName: ",
                           "Please input pageNum: ", "Please input pageSize: "),

            'resp': ('data'),  # response json的key
            'respcolumndesc': ("templateName", "appType", "imageTag", "createTime"),
            'respcolumns': ("templateName", "appType", "imageTag", "createTime"),
        },

        'visualForTensorflow': {  # aimax post getVisualInfo -F ray4        #100
            # %s/api/job/visualForTensorflow?token=%s
            'addUrl': '/api/job/visualForTensorflow',
            'addUrlReplaceAttr': ('Please input jobName:'),
            'addUrlReplace': ("@1@"),  # tensorflowserving44205
            # @RequestBody VisualInfo
            # 'body':({}),
            'bodyjson': 'Please input VisualInfo json (demo: {}):',

        },

        'visualForCaffe': {  # aimax post visualForCaffe -F ray4
            # %s/api/job/visualForCaffe?token=%s

            'addUrl': '/api/job/visualForCaffe',
            'addUrlReplaceAttr': ('Please input jobName:'),
            'addUrlReplace': ("@1@"),  # tensorflowserving44205
            # @RequestBody VisualInfo
            # 'body':({}),
            'bodyjson': 'Please input VisualInfo json (demo: {}):',
        },

        'removeVisual': {  # aimax del removeVisual -F ray4
            # %s/api/job/visual/%s?token=%s
            'delUrl': '/api/job/visual',
            'delUrldesc': ("Please input visual_id:"),
            # 'delbody':({"count":0,"message":"","success":'true',"totalSize":0,"username":"username"}),#User
            'delconfirm': "The visual id {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"

        },

        'getCaffeEntity': {  # aimax get getCaffeEntity -F ray4
            # %s/api/job/visual/%s?token=%s
            'getUrl': '/api/job/visual',
            'getUrldesc': ("Please input visual_id: "),
        },

        # monitor
        'getNodeDockers': {  # aimax get getNodeDockers -F aaa
            # %s/api/monitor/node/dockers?token=%s&hostname=%s
            'getUrl': '/api/monitor/node/dockers',
            'getarg': ('hostname'),
            'getargdef': (None),
            'getargdesc': ("Please input hostname: (demo:n001)"),
            'getargfun': ('zab'),
        },

        'getNodeHistory': {  # aimax get getNodeHistory -F aaa
            # %s/api/monitor/node/history?token=%s&hostname=%s&keys=%s&limit=%s
            'getUrl': '/api/monitor/node/history',
            'getarg': ('hostname', 'keys', 'limit'),
            'getargdef': (None, None, None),
            'getargdesc': (
                "Please input hostname: (demo:n001 )",
                "Please input keys(memhistory/gpuhistory/cpuhistory/nethistory): ",
                "Please input limit: (demo:20)",),
            'getargfun': ('zab', '', ''),

        },

        'getNodeInfo': {  # aimax get getNodeInfo -F aaa
            # %s/api/monitor/node/info?token=%s&hostname=%s
            'getUrl': '/api/monitor/node/info',
            'getarg': ('hostname'),
            'getargdef': (None),
            'getargdesc': ("Please input hostname: (demo:n001 )"),
            'getargfun': ('zab'),
        },

        'getNodeItem': {  # aimax get getNodeItem -F aaa
            # %s/api/monitor/node/item?token=%s&hostname=%s&keys=%s
            'getUrl': '/api/monitor/node/item',
            'getarg': ('hostname', 'keys'),
            'getargdef': (None, None),
            'getargdesc': ("Please input hostname: (demo:n001 )",
                           "Please input keys(sysDockers/dockerLogs/amax.allDockerhealth/amax.dockerhealth/amax.isOnline/nodesQuota): "),
            'getargfun': ('zab', ''),
        },

        'getClusterHistory': {  # aimax get getClusterHistory -F aaa  TODO未找到相关调用
            # %s/api/monitor/cluster/history?token=%s&keys=%s&limit=%s
            'getUrl': '/api/monitor/cluster/history',
            'getarg': ('keys', 'limit'),
            'getargdef': (None, None),
            'getargdesc': ("Please input keys: ", "Please input limit: "),
            # 'getargfun':('zab',''),
        },

        'getClusterHealth': {  # aimax get getClusterHealth -F aaa
            # %s/api/monitor/cluster/health?token=%s
            'getUrl': '/api/monitor/cluster/health',
        },

        'getClusterItem': {  # aimax get getClusterItem -F aaa      #110
            # %s/api/monitor/cluster/item?token=%s&keys=%s
            # http://api-gateway/s/api/monitor/cluster/item?token=%s&keys=%s
            'getUrl': '/api/monitor/cluster/item',
            'getarg': ('keys'),
            'getargdef': (None),
            'getargdesc': ("Please input keys(clusterInfo/dashboardClusterInfo): "),
            # 'getargfun':('zab',''),
        },

        'getJobHistory': {  # aimax get getJobHistory -F aaa
            # %s/api/monitor/job/history?token=%s&jobName=%s&nameSpace=%s&startTime=%s&endTime=%s
            'getUrl': '/api/monitor/job/history',
            'getarg': ('jobName', 'nameSpace', 'startTime', 'endTime'),
            'getargdef': (None, None, None, None),
            'getargdesc': ("Please input jobName:",
                           "Please input nameSpace:",
                           "Please input startTime:",
                           "Please input endTime:",)

            # 'getargfun':('zab',''),
        },

        'getJobInfo': {  # aimax get getJobInfo -F aaa
            # %s/api/monitor/job/info?token=%s&jobName=%s&nameSpace=%s
            'getUrl': '/api/monitor/job/info',
            'getarg': ('jobName', 'nameSpace'),
            'getargdef': (None, None),
            'getargdesc': ("Please input jobName:",
                           "Please input nameSpace:")
        },

        'getJobSummery': {  # aimax get getJobSummery -F aaa
            # %s/api/monitor/job/summery?token=%s&jobName=%s&nameSpace=%s
            'getUrl': '/api/monitor/job/summery',
            'getarg': ('jobName', 'nameSpace'),
            'getargdef': (None, None),
            'getargdesc': ("Please input jobName:",
                           "Please input nameSpace:")
        },

        'getNodeDashboard': {  # aimax get getNodeDashboard -F aaa
            # %s/api/monitor/node/dashboard?token=%s&hostname=%s&keys=%s
            'getUrl': '/api/monitor/node/dashboard',
            'getarg': ('hostname', 'keys'),
            'getargdef': (None, None),
            'getargdesc': ("Please input hostname:",
                           "Please input keys(dockerInfo/history/nodesInfo/allNodesInfo):"),
            # 'getargfun':('zab',''),
        },

        'getNamespaceDashboard': {  # aimax get getNamespaceDashboard -F aaa
            # %s/api/monitor/namespace/dashboard?token=%s&nameSpace=%s&keys=%s
            'getUrl': '/api/monitor/namespace/dashboard',
            'getarg': ('nameSpace', 'keys'),
            'getargdef': (None, None),
            'getargdesc': ("Please input nameSpace:",
                           "Please input keys(dockerInfo/history/namespaceInfo/namespaceDataset):"),
        },

        'getReportTnterval': {  # aimax get getReportTnterval -F aaa
            # %s/api/monitor/report/interval?token=%s&type=%s&startTime=%s&endTime=%s&entities=%s
            'getUrl': '/api/monitor/report/interval',
            'getarg': ('type', 'startTime', 'endTime', 'entities'),
            'getargdef': (None, None, None, None),
            'getargdesc': ("Please input type:",
                           "Please input startTime:",
                           "Please input endTime:",
                           "Please input entities:"),
            # 'getargfun':('zab',''),
        },
        'getReportHistory': {  # aimax get getReportHistory -F aaa
            # %s/api/monitor/report/history?token=%s&type=%s&startTime=%s&endTime=%s&entities=%s
            'getUrl': '/api/monitor/report/history',
            'getarg': ('type', 'startTime', 'endTime', 'entities'),
            'getargdef': (None, None, None, None),
            'getargdesc': ("Please input type:",
                           "Please input startTime:",
                           "Please input endTime:",
                           "Please input entities:"),
        },

        # user
        'listAllUsers': {  # aimax get listAllUsers
            # "%s/api/auth/user?token=%s&pageNum=%s&pageSize=%s&q=%s&groupId=%s
        },

        # node
        'node': {  # 获取节点列表 aimax list node -F aaa
            # "%s/api/node/nodes?token=%s&pageNum=%s&pageSize=%s
            # &nodeFlag=%s&keyWord=%s&gpucount=%s&cpucount=%s&latest=%s&status=%s&timer=%s
            # 获取imagelist
            'reqUrl': '/api/node/nodes',
            'reqarg': ('pageNum', 'pageSize'),
            # ,'nodeFlag','keyWord','gpucount','cpucount','latest','status','timer'),
            'reqargdef': ('1', '10'),
            # "%s/api/image/images?token=%s&q=%s&page=%s&pageSize=%s&publicPage=%s&loginName=%s"
            'resp': ('obj', 'results'),  # response json的key
            'respcolumndesc': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),
            'respcolumns': ("nodeName", "ip", "cpucount", "memory", "gpucount", "disksize", "nodeFlag", "power"),

        },

    }
