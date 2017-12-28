### Appium-Rogue 移动端自动化框架python版本

#### 工具简介：
目前采用python+appium+allure作为这次移动端自动化框架支撑，目的为了减少团队的学习成本以及后期的维护压力，1期所有功能均已经开发完毕。

#### 框架功能：
这套框架整体设计结构和我之前的java版本差不多，只需要运行程序即可启动对应appium server以及自动化测试用例，前提需要在机器上配置好appium的运行环境。页面元素locator以及设备相关信息单独写到配置文件里面，测试时启动命令传这2个文件即可执行工具。1期功能已经包含所有基础框架功能。

#### 详细介绍：
上次和豪哥review之后，已经加入默认配置文件，目的在于方便写case时单用例调试。python版本截图这块参考的豪哥说的override unittest.case.TestCase里面 run这个方法(其实也就多了2行代码)。因此大家在写case的时候不是以往的继承unittest.TestCase，而是我这边自定义的一个类:AppiumTestCase

- 所有的page元素定位以及case 用例集按照项目(sqb, crm)以及页面(LoginPage, HomePage等等)进行归类。
- 配置文件分2种
1. 设备配置文件，主要是存放运行 用例时指定设备相关信息以及appium server相关信息。
> 例如xiaomi.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<config mobileName="samsungS5" mobileType="android">
    <appium>
        <host>127.0.0.1</host>
        <port>4725</port>
        <implicitlyWait>5</implicitlyWait>

        <capabilities>
            <deviceName>Xiaomi</deviceName> <!--要测试的设备名称,如：iphone6s, MI4 -->
            <automationName>appium</automationName> <!--自动化测试平台名称appium -->
            <platformName>Android</platformName> <!--要测试的设备平台名称,如 Android,iOS -->
            <udid>YSBIAEGQ99EA9HW4</udid> <!-- 待测设备的udid -->
            <platformVersion>5.0.2</platformVersion> <!-- 待测设备的版本 -->
            <appPackage>com.wosai.cashbar</appPackage> <!--要测试的App Package名称,如: com.ecovacs -->
            <appActivity>.core.guide.WelcomeActivity</appActivity> <!--要测试的App Activity名称,如:.EcoLogin -->
        </capabilities>
    </appium>

    <global>
        <timeout>30</timeout>
        <wait>3</wait>
        <screenrecord>true</screenrecord>
    </global>
</config>
```

2. 元素定位配置文件，例如sqb分2个配置文件(Android, iOS)
> 例如sqb_android.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<map>
    <!--locator of page map info -->
    <page pageName="LoginPage">
        <locator type="id" timeout="15" location="com.wosai.cashbar:id/frag_guide_page_img">img_guide_page</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/frag_guide_page_button">btn_guide_start</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/login_phone">text_username</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/login_password">text_password</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/login_button">btn_login</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/login_error_message">text_error_msg</locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/frag_login_forget_password">tv_forget_password
        </locator>
        <locator type="id" timeout="3" location="com.wosai.cashbar:id/login_place_holder_text">tv_login_place_holder
        </locator>
    </page>
    <page pageName="HomePage">
        <locator type="text" timeout="10" location="收钱吧">tv_cash_logo</locator>
        <locator type="text" timeout="5" location="收款">tv_cash</locator>
        <locator type="text" timeout="3" location="账本">tv_account_book</locator>
        <locator type="text" timeout="3" location="报表">tv_report</locator>
        <locator type="text" timeout="3" location="首页">tv_home</locator>
        <locator type="text" timeout="3" location="服务中心">tv_service</locator>
        <locator type="text" timeout="3" location="我">tv_personal</locator>
    </page>
</map>
```
- 另外全局的测试数据文件，默认读取data.json。

#### 如何写case
- 如何定义元素？
1. 页面元素定义按照页面来划分，也就是说loign_page.py这个下面放的是登录页面所有元素的定义以及该页面上所涉及的常规方法
2. 使用装饰器@locator来定义元素
> 例如登录页面的输入用户名的元素定义可以通过下面的代码来简单定义

```
class HomePage:
@locator()
    def tv_cash_logo(self):
        pass
```
> 上面的这段意思是从配置文件sqb_android.xml读取HomePage.tv_cash_logo这段元素定义，返回的是一个Locator对象(包含type, timeout, location这3个属性)
- 如何写case
1. 写case也是按照页面来划分，比如test_login_page.py存放的是涉及登录页面的所有case
2. 测试用例的类需要继承我上面说的AppiumTestCase，这样才能断言失败后自动截图
3. 所有的元素操作，比如点击，输入等等，不是像我们常规理解的是对MobileElement进行操作，需要换一个理解方式，这边对元素的操作都是对一个Locator对象进行操作，我这边会把selenium对元素的操作方法重新封装一遍(在action.py这个下面)。
> 例如对登录页面下的输入用户名控件进行输入操作

```
action.input_text(self.login_page.text_username(), self.data.testLogin.username, True)
```

```
def input_text(self, locator, value, clear_first=False):
    """
    输入文本内容
    :param locator: locator 
    :param value: 输入内容
    :param clear_first: 是否先清除
    :return: 
    """
    if clear_first:
        self._find_element(locator).clear()
        self._find_element(locator).send_keys(value)
```
#### 其他
1期所有功能均已经开发完毕，根据豪哥上次的APP测试团队技术路线要求，2期会加入以下功能(因为接下来业务审核2期以及app团队理财项目影响，这块2期完成时间待定)：
1. 引入opencv进行图像识别，以及对比功能
2. monkey test
3. 遍历测试(java版本自动遍历已开发完，待长时间健壮性测试)
4. 解决BSC触发能力
5. 推送消息认证(本周五的时候已经开发完这个小工具，具体的需求已和灿伟沟通过，待下周调试)
