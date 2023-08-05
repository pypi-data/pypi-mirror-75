#-*- coding:utf-8 -*-

#movies列表
movies = ["The Holy Grail",1975,"Terry Jones & Terry Gillam",91,
            ["Graham Chapam",
                ["Michael Palin","John Cleese","Terry Gillam","Eric Idle","Terry Jones"]]]


'''
函数print_lol用于递归打印出列表中的嵌套的列表
'''
def print_lol(the_list):
    for each_item in the_list:
        if(isinstance(each_item,list)):
            print_lol(each_item)
        else:
            print(each_item)


#打印出movies列表中的数据
print_lol(movies)

