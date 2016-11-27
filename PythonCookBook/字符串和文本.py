#本章的重点放在有关文本操作的常见问题。

#2.1  针对任意多的分割符拆分字符串
#字符串对象的split()方法只能处理非常简单的情况，而且不支持多个分割符，对分隔符周围出现的空格也无能为力。
#这时可以使用re.split()方法。
line ='asdf fijk;  afed, fjek,asdk,    foo'
import re
a = re.split(r'[;,\s]\s*',line)

print(a)        #['asdf', 'fijk', 'afed', 'fjek', 'asdk', 'foo']

#当使用到了捕获组，需要小心正则表达式模式中捕获组(capture group)是否包含在括号中。
#如果用到捕获组，那么匹配的文本也会包含在最终的的结果中

fields = re.split(r'(;|,|\s)\s*',line)
print(fields)       #['asdf', ' ', 'fijk', ';', 'afed', ',', 'fjek', ',', 'asdk', ',', 'foo']

#如果不想在结果中看到分割符，但仍想使用括号对正则表达式模式进行分组，请确保使用的是非捕获组，以(?:...)的形式指定。
fields = re.split(r'(?:;|,|\s)\s*',line)
print(fields)       #['asdf', 'fijk', 'afed', 'fjek', 'asdk', 'foo']

#2.2在文本字符串的开头或者结尾处做文本匹配
#我们需要在字符串的开头或者结尾处按照指定的文本模式做检查，例如检查文本扩展名、URL协议类型等
filename = 'spam.txt'
filename.endswith('.txt')        #True

#如果需要同时针对多个选项做检查，只需要给startswith()和endswith()提供包含可能选项的元组即可。
filename.endswith(('.txt','.py'))       #True

#2.3利用shell 通配符做字符串匹配
#当在工作UNIX shell 下时，我们想使用常见的通配符模式（即，*.py/Dat[0-]*.csv等）对文本做匹配
from fnmatch import fnmatch
from fnmatch import fnmatchcase

print(fnmatch('foo.txt','*.txt'))       #True
print(fnmatch('foo.txt','?oo*.txt'))       #True

print(fnmatch('Dat45.csv','Dat[0-9]*.csv'))     #True

#一般来说，fnmatch()函数模式所采用的大小写区分规则和底层文件系统相同（根据操作系统的不同而有所不同）。
#而fnmatchcase()，它完全根据我们提供的大小方式来匹配

#2.4 文本模式的匹配和查找
#如果想要匹配的只是简单地文字，可以使用基本的字符串方法，如果更为复杂，需要使用正则表达式和re模块

text1 = '11/27/2012'
text2 = 'Nov 27,2012'
import re 

#Somple matching:\d+ means match oone or more digits
if re.match(r'\d+/\d+/\d+',text1):
    print('yes')
else:
    print('no')
#yes
if re.match(r'\d+/\d+/\d+',text2):
    print('yes')
else:
    print('no')
#no

#如果打算针对同一种模式做多次匹配，那么通常会先将正则表达式模式预编译成一个对象模式
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')
#yes
if datepat.match(text2):
    print('yes')
else:
    print('no')
    #no

#match()方法总是尝试在字符串的靠头找到匹配项。如果针对整个文本搜索出所有的匹配项，那么就应该使用findall()方法。
#当定义正则表达式时，我们常常会将部分模式用括号包起来的模式引进捕获组。
#捕获组通常能简化后续对匹配文本进行处理，因为每个组的内容都可以单独提取出来。

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/127/2012')
print(m)
#<_sre.SRE_Match object; span=(0, 11), match='11/127/2012'>
print(m.group(0))
#11/127/2012
print(m.group(1))
#11
print(m.group(2))
#127
print(m.group(3))
#2012
print(m.groups())
#('11', '127', '2012')

#findall()方法搜索整个文本并找出所有匹配项然后将他们以列表的形式返回。

#2.5查找和替换文本
#对于简单的文本模式，使用str.replace()即可
#针对更为复杂的模式，可以使用re模块的sub()函数和方法。
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
a = re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text)
print(a)
#Today is 2012-11-27. PyCon starts 2013-3-13.
#sub()函数的第一个参数是匹配模式，第二个参数是要替换上的模式。类似“\3”这样的反斜线加数字的符号代表着模式中捕获组的数量。

#2.6以不区分大小写的方式对文本做查找和替换

#要进行不区分大小写的文本操作，我们需要使用re模块并对各种操作都要加上re.IGNORECASE标记。
text = 'UPPER PYTHON,lower python ,Mixed Python'

a = re.findall('python',text,flags = re.IGNORECASE)
print(a)
#['PYTHON', 'python', 'Python']
a = re.sub('python','snake',text,flags = re.IGNORECASE)
print(a)
#UPPER snake,lower snake ,Mixed snake

#上面这个例子揭示出了一种局限，那就是带替换的文本与匹配的文本大小写并不吻合。
#如果要修正这个问题，需要用到一个支撑函数(support function),示例如下：

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

a = re.sub('python',matchcase('snake'),text,flags = re.IGNORECASE)
print(a)
#UPPER SNAKE,lower snake ,Mixed Snake

#2.7定义实现最短匹配的正则表达式

# *操作符在正则表达式中采取的时贪心策略，所以匹配过程是基于找出最长的可能匹配来进行的。要实现最短匹配，只要在模式中的*操作符后加上?修饰符就可以
text = 'Computre says "no." Phone says "yes"'
str_pat = re.compile(r'\"(.*?)\"')
a = str_pat.findall(text)
print(a)        #['no.', 'yes']

str_pat = re.compile(r'\"(.*)\"')
a = str_pat.findall(text)
print(a)        #['no." Phone says "yes']

#2.8编写多行模式的正则表达式
#我们打算用正则表达式对一段文本块做匹配，但是希望在进行匹配时能够跨越多行。
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/*this is a comment */'
text2 = '/*this is a \n multiline comment */'
a = comment.findall(text1)
print(a)        #['this is a comment ']
a = comment.findall(text2)
print(a)        #[]

#句点(.)可以匹配任意字符，但是不能匹配换行符。
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
a = comment.findall(text2)
print(a)        #['this is a \n multiline comment ']
#在这个模式中，(?:.|\n)指定了一个非捕获组（即，这个组只做匹配但不捕获结果，也不会分配组号）。

#2.9将Unicode文本统一表示为规范形式。
#在Unicode 中，有些特定的字符可以表示成多种合法的代码点序列。






