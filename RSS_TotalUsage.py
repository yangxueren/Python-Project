import os

sum = 0
rss_list = []

str1 = os.popen('ps auc', 'r')
for i in str1:
    str2 = i.split()
    rss = str2[5]
    rss_list.append(rss)

for j in rss_list[1:-1]:
    sum += int(j)

print ("%s:%s" %("rss", sum))