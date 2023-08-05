class Yml:
    restMap = {
                'zone':
                    {
                        #获取zonelist
                        'reqUrl':'/api/job/zones',
                        'resp':'zones',#response json的key
                        'respcolumndesc':("name","createTimeStamp","jobType"),
                        'respcolumns':("name","createTimeStamp","jobType"),



                        #新增zone   aimax add zone -F aaa
                        'addUrl':'/api/job/zones',
                        'addarg':("name","jobType","desc","quotas","message","success","totalSize"),
                        'addargdef':(None,"ML","",{#NONE表示需要输入的
                            "MEM":{"amount":1.0,"resourceType":"MEM","unit":"GB","usedAmount":0.0},
                            "JOBS":{"amount":20.0,"resourceType":"JOBS","usedAmount":0.0},
                            "CPU":{"amount":1.0,"resourceType":"CPU","usedAmount":0.0},
                            "GPU":{"amount":0.0,"resourceType":"GPU","usedAmount":0.0}
                        },"","true","0"),
                        'adddesc':("Please input zone name: ",
                                   "Please select JobType  0 ML 1 HPC",
                                   "Please input desc name: ",
                                   "Please input zone quotas: ","message","success","totalSize"
                                   ),


                        #删除zone %s/api/job/zones/%s?token=%s
                        'delUrl':'/api/job/zones',
                        'delUrldesc':("Please input zonename: "),
                        'delconfirm':"The zone {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"

                    },

                'image':
                    {
                        #获取imagelist
                        'reqUrl':'/api/image/images',
                        'reqarg':('loginName','page','publicPage','page_size','q'),
                        'reqargdef':('auth_username','0','1','10',''),
                        #"%s/api/image/images?token=%s&q=%s&page=%s&pageSize=%s&publicPage=%s&loginName=%s"
                        'resp':'publicImages',#response json的key
                        'respcolumndesc':("name","creationTime","tagsCount"),
                        'respcolumns':("name","creationTime","tagsCount"),
                    },
                'imageforjob':
                    {
                        #根据job获取适配的镜像
                        #"%s?token=%s&page=%s&pageSize=%s&type=%s&frames=%s&visual=%s&jupyter=%s&deploy=%s&ssh=%s&vnc=%s"
                        'reqUrl':'/api/image/imagesForjob',
                        'reqarg':('page','pageSize','type','frames','visual','jupyter','deploy','ssh','vnc'),#,
                        'reqargdef':('1','10','1','[tensorflow-gpu:python]',"null","null","null","false","false"),
                        'resp':'imagesForjob',#response json的key
                        'respcolumndesc':("imageName","系统","标签"),
                        'respcolumns':("imageName","dist","tagName"),
                    },
                'disclose':#aimax add disclose -F aaa
                    {
                        #"%s/api/image/images/disclose?token=%s"
                        'addUrl':'/api/image/images/disclose',
                        #{"imageName":"cuda","message":"","success":true,"tagName":["asdasdasdasd"],"totalSize":0}
                        'addarg':("repositoryName","imageName",
                                   "tagName","message","success","totalSize"),
                        'addargdef':("ray4","cuda",
                                      ["10.0-cudnn7-devel-ubuntu18.04"],"","true",0),
                        'adddesc':(),
                    },

                'repositoriesByprojectId':#g根据用户获取镜像 list
                    {
                        #"%s/api/image/images/%s/repository?token=%s&q=%s&page=%s&pageSize=%s"
                        'reqUrl':'/api/image/images',
                        'reqUrldesc':("Please input project name: "),
                        'reqUrlappend':'repository',
                        'reqarg':('loginName','page','publicPage','page_size','q'),
                        'reqargdef':('auth_username','1','1','10',''),

                        'resp':'commonImages',#response json的key
                        'respcolumndesc':("name","creationTime","tagsCount"),
                        'respcolumns':("name","creationTime","tagsCount"),

                    },


                'syncImage':#同步镜像 aimax add syncImage -F aaa
                    {
                        #%s/api/image/images/sync?token=%s&loginName=%s
                        'addUrl':'/api/image/images/sync',
                        'addarg':('loginName'),
                        'addargdef':(None),
                        'addargdesc':("Please input sync Name: "
                                      ),
                        'addarg':("repositoryName","imageName",
                                   "tagName","message","success","totalSize"),
                        'addargdef':('user_ray4',"nginx",
                                      ["latest"],"","true",0),
                    },

                'shareImage':#分享镜像  aimax add shareImage -F aaa
                    {
                        #"%s/api/image/images/share?token=%s",
                        'addUrl':'/api/image/images/share',
                        'addargdesc':("Please input sync Name: "),
                        'addarg':("imageName","message","owner","repositoryName","shareOfTag","success","totalSize"),
                        'addargdef':('nginx',"",'ray5', "ray5",
                                      [{"shareObjs":[{"shareRange":"group","shareTo":[]},
                                                     {"shareRange":"person","shareTo":["ray3"]},
                                                     {"shareRange":"all","shareTo":[]}],"tagName":"latest"}],"true",0),
                    },



                'shareObj':#获取共享对象 aimax list shareObj -F aaa  # 33
                    {
                        #获取imagelist
                        #%s/api/image/images/share/shareObj?token=%s&id=%s"
                        'reqUrl':'/api/image/images/share/shareObj',
                        'reqarg':('id'),
                        'reqargdef':(None),
                        'reqargdesc':("Please input id: "),

                        'resp':'shareOfTag',#response json的key
                        'respcolumndesc':("tagName","shareObjs"),
                        'respcolumns':("tagName","shareObjs"),
                    },

                'getShareImage':#查看某用户的分享镜像列表 aimax list getShareImage -F aaa # username: ray5
                    {
                        #获取imagelist
                        #"%s/api/image/images/share/%s?token=%s&page=%s",
                        'reqUrl':'/api/image/images/share',
                        'reqUrldesc':("Please input username name: "),
                        #'reqUrlappend':'username',
                        'reqarg':('page','page_size'),
                        'reqargdef':('1','10'),
                        'reqargdesc':("","",""),

                        'resp':'shareInfos',#response json的key
                        'respcolumndesc':("owner","imageName","repositoryName","tagName"),
                        'respcolumns':("owner","imageName","repositoryName","tagName"),

                    },

                'cancelShare':#取消分享镜像 aimax del cancelShare -F aaa  #tagId
                    {
                        #"%s/api/image/images/share/cancelShare?token=%s&tagId=%s",
                        'delUrl':'/api/image/images/share/cancelShare',
                        #'delUrldesc':("Please input imagename: "),
                        'delarg':('tagId'),
                        'delargdef':(None),
                        'delargdesc':("Please input tagId: "),

                        'delconfirm':"The image tagId {} will be removed , are you sure?\n 'Y': Continue, 'Others': Cancel\n"

                    },

                'getImageByName':#根据名称 获取镜像 aimax list getImageByName -F aaa
                    {
                        #"%s/api/image/images/%s/tags?token=%s&isPublic=%s&repositoryName=%s&loginName=%s"
                        #获取imagelist
                        'reqUrl':'/api/image/images',
                        'reqUrldesc':("Please input imageName : "),
                        'reqUrlappend':'tags',
                        'reqarg':('isPublic','repositoryName','loginName'),
                        'reqargdef':(None,None,'auth_username'),
                        'reqargdesc':("Please input isPublic : ","Please input repositoryName : ",""),

                        'resp':'images',#response json的key
                        'respcolumndesc':("name","os","size","tagId"),
                        'respcolumns':("name","os","size","tagId"),


                    },

                'getImagesByProjectId':#根据项目id获取镜像 aimax list getImagesByProjectId -F aaa
                    {
                        #"%s/api/image/images/%s/repository?token=%s&q=%s&page=%s&pageSize=%s"
                        #获取imagelist
                        'reqUrl':'/api/image/images',
                        'reqUrldesc':("Please input username : "),
                        'reqUrlappend':'repository',
                        'reqarg':('q','page','pageSize'),
                        'reqargdef':('','1','10'),
                        'reqargdesc':("Please input isPublic : ","Please input repositoryName : ",""),

                        'resp':'commonImages',#response json的key
                        'respcolumndesc':("projectId","tagsCount","name","updateTime"),
                        'respcolumns':("projectId","tagsCount","name","updateTime"),
                    },

                'doNewTags':#打标签 aimax add doNewTags -F aaa
                    {
                        #""%s/api/image/images/%s/tags?token=%s&tagName=%s&oldTag=%s&isPublic=%s&repositoryName=%s"",

                        #"%s/api/image/images/share?token=%s",
                        
                        'addUrl':'/api/image/images',
                        'addUrldesc':("Please input imageName : "),
                        'addUrlappend':'tags',

                        'addarg':("tagName","oldTag","isPublic","repositoryName"),
                        'addargdef':(None,None,None,None),
                        'adddesc':("Please input tagName: ","Please input oldTag: ","Please input isPublic: ","Please input repositoryName: "),


                    },







    }
