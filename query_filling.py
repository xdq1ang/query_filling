from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json,random
from selenium.webdriver import ActionChains

def get_track(distance):      # distance为传入的总距离
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance*4/5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 1

    while current < distance:
        if current < mid:
            # 加速度为2
            a = random.uniform(0, 2)
        else:
            # 加速度为-2
            a = random.uniform(-1, -2)
        v0 = v
        # 当前速度
        v = v0 + a*t
        # 移动距离
        move = v0*t+1/2*a*t*t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track

def move_to_gap(driver, slider, tracks):     # slider是要移动的滑块, tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()

#we need a special finction to help circulate here
def opeDiv(i,driver,obj,selNum=None,weights=None):
    lst=list(obj.keys())#获取可以填写的项目
    #step1
    div=driver.find_element(By.ID,"div"+str(i))
    #step2
    typeDiv=div.get_attribute("type")
    #step3
    if typeDiv=="1":
        # 文本输入框
        #operate as the text input-send_keys(content)
        node=driver.find_element(By.XPATH,'//input[@id="q%s"]'%str(i))
        for i in lst:
            if i in div.text:
                node.send_keys(obj[i])
                break
            else:
                continue
        return
    elif typeDiv=="3":
        # 单选题
        choice = [1, 2, 3, 4, 5]
        weight= weights[str(i)]
        oneC=random.choices(choice, weights=weight)[0]
        node=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/div[%s]/span/a'%(str(i),str(oneC)))
        node.click()
    elif typeDiv=="4":
        #operate as the checkbox input-click()
        node1=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/div[%d]/span/a'%(str(i),random.randint(1,4)))
        node2=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/div[%d]/span/a'%(str(i),random.randint(1,4)))
        #上面两个节点是以四个多选项为例进行的，并且选择的选项是随机的
        node1.click()
        node2.click()
    elif typeDiv=="6":
        # 选项
        choice = [1, 2, 3, 4, 5]
        # 权重
        weight= weights[str(i)]
        num=selNum*2+1
        weight_id=1
        for it in range(3,num+1,2):
            oneC=random.choices(choice, weights=weight[str(weight_id)])[0]
            node=driver.find_element(By.XPATH,'//*[@id="div%s"]/div[2]/table/tbody/tr[%d]/td[2]/ul/li[%d]/a'%(str(i),it,oneC))
            node.click()
            weight_id+=1

    else:
        return

def write(link,driver,obj,weights):
    #通过问卷url获取并打开
    driver.get(link)
    #try filling the query, if not accessible, fill in by hand
    page1=range(1,7)
    selNum1=0
    page2=range(7,8)
    selNum2=8
    page3=range(8,9)
    selNum3=13
    page4=range(9,10)
    selNum4=10    
    pages=[page1, page2, page3, page4]
    selNums=[selNum1,selNum2,selNum3,selNum4]

    p=0
    for page in pages:
        for i in page:   
            opeDiv(i,driver,obj,selNums[p],weights)
        try:
            # 存在下一页，获取下一页按钮
            driver.find_element(By.XPATH,'//*[@id="divNext"]/a').click()
            p+=1
        except:
            # 不存在下一页
            # 用于用甄别有效性
            driver.find_element(By.XPATH,"//*[@id='div10']/div[2]/div[1]/span/a").click()
            driver.find_element(By.XPATH,"//*[@id='ctlNext']").click()

            
    try:#尝试点击验证，这个不耽误时间，停留0.1秒就够了
        time.sleep(5)#必要的间歇时间，没有的话可能找不到节点
        element = driver.find_element(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]')
        element.click()#点击确认验证
        yanz = driver.find_element(By.XPATH,'//*[@id="SM_BTN_1"]/div[1]/div[4]')
        yanz.click()#点击验证按钮
        print("end time:%d"%time.localtime(time.time())[5])
        print("已点击验证按钮!")#time.localtime(time.time())[5]#到这一步只需要2秒钟
    except:
        pass
    
    time.sleep(6)
    #下面需要一个判断是否填写成功的方法，当然前台运行浏览器时可以直观看到
    feedback=driver.find_element(By.XPATH,'//*[@id="divdsc"]')
    print(feedback.text)


def onTime():#下面设置一个定时填写的函数
    #现在需要设置问卷填写的时间，到时间以后再获取链接进行填写即跳出循环
    hour=int(input("hour:"))
    minute=int(input("minute:"))
    second=int(input("second:"))
    while True:
        time_tuple=time.localtime(time.time())#3、4、5分别代表时分秒
        if time_tuple[3]==hour and time_tuple[4]>=minute and time_tuple[5]>=second:
            break#数据类型是整型
        else:
            #print(time_tuple[3:6])
            time.sleep(0.01)
            continue
    return True

#预加载浏览器，加快提交速度
def openChrome():
    option = webdriver.ChromeOptions()
    #可以补充一个后台运行的插件，这样会更快，同样后面需要另一个插件判定是否填写成功
    #option.add_argument("headless")
    #加速优化
    option.add_argument("--disable-images")
    option.add_argument("--disable-javascript")
    #优化页面加载策略
    option.page_load_strategy='eager'   #这一项可能会出现问题，大多数是网络问题，更换网络即可
    #绕过问卷星的防selenium设置
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return driver
    
#function main()
if __name__=="__main__":
    obj=json.load(open("questions.json","r",encoding="utf-8"))#读取json文件获取要填写的信息
    weights=json.load(open("weights.json","r",encoding="utf-8"))
    times=30
    for each in range(times):
        #防止系统原因出现问卷没有及时开放
        driver=openChrome()#预加载浏览器
        # link=input("THE LINK OF THE QUERY:\n")#嵌入链接
        link="https://www.wjx.cn/vm/eOMHAci.aspx"
        # if onTime():
        # print("start time:%d"%time.localtime(time.time())[5])
        time.sleep(0.01)
        write(link,driver,obj,weights)

