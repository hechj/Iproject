import requests
import time
import execjs


def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())

    return head + fscode + tail


# 根据基金代码获取净值
def getWorth(fscode):
    content = requests.get(getUrl(fscode))
    jsContent = execjs.compile(content.text)

    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    # 单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    # 累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')

    netWorth = []
    ACWorth = []

    for dayWorth in netWorthTrend[::-1]:
        netWorth.append(dayWorth['y'])

    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])
    print(name, code)
    return netWorth, ACWorth


def getAllCode():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    content = requests.get(url)
    jsContent = execjs.compile(content.text)
    rawData = jsContent.eval('r')
    allCode = []
    for code in rawData:
        allCode.append(code[0])
    return allCode


allCode = getAllCode()

# netWorthFile = open('./netWorth.csv', 'w')
# ACWorthFile = open('./ACWorth.csv', 'w')
fundCodeFile = open('./fund.csv', 'w')
fundCodeFile.write("trade_code")

i = 0
for code in allCode:
    try:
        netWorth, ACWorth = getWorth(code)
    except:
        continue
    if len(netWorth) <= 0 or len(ACWorth) < 0:
        print(code + "'s' data is empty.")
        continue

    i = i + 1
    fundCodeFile.write("\n")
    fundCodeFile.write("-" + code + "-")

    """
    netWorthFile.write("\'" + code + "\',")
    netWorthFile.write(",".join(list(map(str, netWorth))))
    netWorthFile.write("\n")

    ACWorthFile.write("\'" + code + "\',")
    ACWorthFile.write(",".join(list(map(str, ACWorth))))
    ACWorthFile.write("\n")
    """
    print("write " + code + "'s data success.")
    if i >= 10:
        break

# netWorthFile.close()
# ACWorthFile.close()
fundCodeFile.close()
