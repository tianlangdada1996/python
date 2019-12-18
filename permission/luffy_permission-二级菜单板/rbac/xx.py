from collections import OrderedDict

d = {
	1: {
		'title': '业务管理',
		'icon': 'fa-envelope-open',
		'weight': 80,
		'children': [{
			'title': '客户展示',
			'icon': 'fa-gavel fa-spin',
			'url': '/customer/list/'
		}]
	},
	2: {
		'title': '财务管理',
		'icon': 'fa-jpy',
		'weight': 70,
		'children': [{
			'title': '缴费展示',
			'icon': 'fa-bath fa-spin',
			'url': '/payment/list/'
		}, {
			'title': '纳税展示',
			'icon': 'fa-camera',
			'url': '/nashui/'
		}]
	}
}

d1_xx = OrderedDict()  # {}

# d1 = {
#     '1':{
#         'xx':70
#     },
#     '2':{
#         'xx':80
#     }
# }
#
# d1_sort = sorted(d,key=lambda x:d[x]['weight'],reverse=True)
# print(d1_sort)
#
# # dd1 = {}
# for i in d1_sort:
#     d1_xx[i] = d[i]
#
# print(d1_xx)



d2 = {
    1:'xx',
    2:'oo',
}













