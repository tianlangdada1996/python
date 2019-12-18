
from rbac import models
from django.conf import settings



def init_permission(request,uname):
    """
    权限注入函数,

    :param request: request对象
    :param uname:   用户名称
    :return:
    """
    # 往session中注入权限
    permission_list = models.Role.objects.filter(userinfo__username=uname).values(
        'permissions__id',
        'permissions__menu_id',
        'permissions__url',
        'permissions__parent_id',
        'permissions__title',
        'permissions__icon',
        'permissions__menu__title',
        'permissions__menu__weight',
        'permissions__menu__icon',

    ).distinct()

    print(permission_list)
    # menu_list = []  # [{permission__url:'/xx/list/'}]
    menu_dict = {}
    '''
        {
            2:{
                'title':'财务管理',
                'icon':''
                'children':[
                    {'title':'缴费展示','url':'/payment/list/','icon':''},
                    {'title':'纳税展示','url':'/nashui/list/','icon':''},
                ]
                
            },
            一级菜单id:{
                'title':'业务管理',
                'icon':''
                'children':[
                    {'title':'客户展示','url':'/payment/list/','icon':''},
                    
                ]
                
            }
        
        }
    
    
    < QuerySet[{
            'permissions__id': 1,
            'permissions__menu_id': 1,
            'permissions__url': '/customer/list/',
            'permissions__title': '客户展示',
            'permissions__icon': 'fa-gavel fa-spin',
            'permissions__menu__title': '业务管理',
            'permissions__menu__icon': 'fa-envelope-open'
        }, {
            'permissions__id': 2,
            'permissions__menu_id': None,
            'permissions__url': '/customer/add/',
            'permissions__title': '客户添加',
            'permissions__icon': None,
            'permissions__menu__title': None,
            'permissions__menu__icon': None
        }
    '''
    for permission in permission_list:

        if permission['permissions__menu_id']:
            if menu_dict.get(permission['permissions__menu_id']):
                menu_dict[permission['permissions__menu_id']]['children'].append(
                    {
                        'title': permission['permissions__title'],
                        'icon': permission['permissions__icon'],
                        'url': permission['permissions__url'],
                        'id': permission['permissions__id'],
                    }
                )
            else:
                menu_dict[permission['permissions__menu_id']] = {
                    'title':permission['permissions__menu__title'],
                    'icon':permission['permissions__menu__icon'],
                    'weight':permission['permissions__menu__weight'],
                    'children':[
                        {
                            'title':permission['permissions__title'],
                            'icon':permission['permissions__icon'],
                            'url':permission['permissions__url'],
                            'id': permission['permissions__id'],
                         }
                    ]

                }



    # print(menu_dict)



    # # 校验用户是否有某个功能的权限,中间件中用的
    request.session[settings.PERMISSION_KEY] = list(permission_list)
    #
    # # 生成左侧菜单用的
    request.session[settings.MENU_KEY] = menu_dict




