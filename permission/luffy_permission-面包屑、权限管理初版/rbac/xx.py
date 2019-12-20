# d = {1:{
# 	'permissions__id': 1,
# 	'permissions__menu_id': 1,
# 	'permissions__url': '/customer/list/',
# 	'permissions__parent_id': None,
# 	'permissions__title': '客户展示',
# 	'permissions__icon': 'fa-gavel fa-spin',
# 	'permissions__menu__title': '业务管理',
# 	'permissions__menu__weight': 80,
# 	'permissions__menu__icon': 'fa-envelope-open'
# }, 2:{
# 	'permissions__id': 2,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/customer/add/',
# 	'permissions__parent_id': 1,
# 	'permissions__title': '客户添加',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, 3:{
# 	'permissions__id': 3,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/customer/edit/(?P<cid>\\d+)/',
# 	'permissions__parent_id': 1,
# 	'permissions__title': '客户编辑',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, {
# 	'permissions__id': 4,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/customer/del/(?P<cid>\\d+)/',
# 	'permissions__parent_id': 1,
# 	'permissions__title': '客户删除',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, 5:{
# 	'permissions__id': 5,
# 	'permissions__menu_id': 2,
# 	'permissions__url': '/payment/list/',
# 	'permissions__parent_id': None,
# 	'permissions__title': '缴费展示',
# 	'permissions__icon': 'fa-bath fa-spin',
# 	'permissions__menu__title': '财务管理',
# 	'permissions__menu__weight': 70,
# 	'permissions__menu__icon': 'fa-jpy'
# }, {
# 	'permissions__id': 6,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/payment/add/',
# 	'permissions__parent_id': 5,
# 	'permissions__title': '缴费添加',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, {
# 	'permissions__id': 7,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/payment/edit/(?P<pid>\\d+)/',
# 	'permissions__parent_id': 5,
# 	'permissions__title': '缴费编辑',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, {
# 	'permissions__id': 8,
# 	'permissions__menu_id': None,
# 	'permissions__url': '/payment/del/(?P<pid>\\d+)/',
# 	'permissions__parent_id': 5,
# 	'permissions__title': '缴费删除',
# 	'permissions__icon': None,
# 	'permissions__menu__title': None,
# 	'permissions__menu__weight': None,
# 	'permissions__menu__icon': None
# }, {
# 	'permissions__id': 9,
# 	'permissions__menu_id': 2,
# 	'permissions__url': '/nashui/',
# 	'permissions__parent_id': None,
# 	'permissions__title': '纳税展示',
# 	'permissions__icon': 'fa-camera',
# 	'permissions__menu__title': '财务管理',
# 	'permissions__menu__weight': 70,
# 	'permissions__menu__icon': 'fa-jpy'
# }}



d1 = {1:'aa','bb':2}
#{"1": "aa", "bb": 2}

import json
a = json.dumps(d1)
print(json.loads(a))












