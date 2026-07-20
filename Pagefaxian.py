import time
from appium.webdriver.common.appiumby import AppiumBy
from BasePage import BasePage

class Pagefaxian(BasePage):
    # 页面元素定位
    def kefu(self):
        return self.find_by_accessibility('智能客服')

    def youhuiquan(self):
        return self.find_by_accessibility('优惠券')

    def gengduo(self):
        xpath='//android.widget.LinearLayout[@resource-id="com.xiaomi.jr:id/flutter_container"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[@content-desc="发现"]/android.view.View[3]'
        return self.find_by_xpath(xpath)

    def jiedaiedu(self):
        xpath='//android.view.View[contains(@content-desc,"最高200000")]'
        return self.find_by_xpath(xpath)

    def zongzichan(self):
        xpath='//android.view.View[contains(@content-desc,"我的总资产")]'
        return self.find_by_xpath(xpath)

    def wodebaozhang(self):
        xpath='//android.view.View[contains(@content-desc,"官方碎屏保")]'
        return self.find_by_xpath(xpath)

    def fulihongbao(self):
        xpath='//android.view.View[contains(@content-desc,"福利红包")]'
        return self.find_by_xpath(xpath)

    def tianxingjieqian(self):
        xpath='(//android.view.View[contains(@content-desc,"优选持牌机构")])[1]'
        return self.find_by_xpath(xpath)

    def huankuanguanjia(self):
        xpath='//android.view.View[contains(@content-desc,"还款管家")]'
        return self.find_by_xpath(xpath)

    def xinyongka(self):
        return self.find_by_accessibility('信用卡')

    def meiriqiandao(self):
        xpath='//android.view.View[contains(@content-desc,"每日签到")]'
        return self.find_by_xpath(xpath)

    def daezhouzhuan(self):
        xpath='//android.view.View[contains(@content-desc,"大额周转")]'
        return self.find_by_xpath(xpath)

    def huafeichongzhi(self):
        return self.find_by_accessibility('话费充值')

    def wodekefu(self):
        return self.find_by_accessibility('我的客服')

    def gerenxinxi(self):
        return self.find_by_accessibility('个人信息')

    def zlunbotu(self):
        xpath='//android.view.View[contains(@content-desc,"99元小米商城支付券")]'
        return self.find_by_xpath(xpath)

    def middle_title(self):
        xpath='//android.view.View[contains(@content-desc,"优选持牌机构为您服务")]'
        return self.find_by_xpath(xpath)

    def last_text(self):
        xpath='//android.view.View[contains(@content-desc,"200,000") and contains(@content-desc,"日利率0.02%")]'
        return self.find_by_xpath(xpath)

    def btn_lingquedu(self):
        return self.find_by_accessibility('领取额度')
    # 导航栏
    def nav_tianxing(self):
        return self.find_by_accessibility("天星借钱")

    def nav_discover(self):
        return self.find_by_accessibility("发现")

    def nav_mine(self):
        return self.find_by_accessibility("我的")

    # ========== 页面操作方法 ==========

    def click_kefu(self):
        """点击智能客服"""
        self.kefu().click()
        time.sleep(1)
        print("[OK] 点击【智能客服】")

    def click_youhuiquan(self):
        """点击优惠券"""
        self.youhuiquan().click()
        time.sleep(1)
        print("[OK] 点击【优惠券】")

    def click_gengduo(self):
        """点击发现页更多入口"""
        self.gengduo().click()
        time.sleep(1)
        print("[OK] 点击【更多】")

    def get_jiedaiedu_text(self):
        """获取借贷额度模块文本（容错：元素不在当前页返回空串）"""
        desc = self.safe_desc(AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"最高200000")]')
        print(f"[OK] 借贷额度: {desc}")
        return desc

    def get_zongzichan_text(self):
        """获取我的总资产文本（容错：元素不在当前页返回空串）"""
        desc = self.safe_desc(AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"我的总资产")]')
        print(f"[OK] 我的总资产: {desc}")
        return desc

    def click_wodebaozhang(self):
        """点击我的保障"""
        self.wodebaozhang().click()
        time.sleep(1)
        print("[OK] 点击【我的保障】")

    def get_fulihongbao_text(self):
        """获取福利红包文本（容错：元素不在当前页返回空串）"""
        desc = self.safe_desc(AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"福利红包")]')
        print(f"[OK] 福利红包: {desc}")
        return desc

    def click_tianxingjieqian(self):
        """点击天星借钱入口"""
        self.tianxingjieqian().click()
        time.sleep(1)
        print("[OK] 点击【天星借钱】")

    def click_huankuanguanjia(self):
        """点击还款管家"""
        self.huankuanguanjia().click()
        time.sleep(1)
        print("[OK] 点击【还款管家】")

    def click_xinyongka(self):
        """点击信用卡"""
        self.xinyongka().click()
        time.sleep(1)
        print("[OK] 点击【信用卡】")

    def click_meiriqiandao(self):
        """点击每日签到"""
        self.meiriqiandao().click()
        time.sleep(1)
        print("[OK] 点击【每日签到】")

    def click_daezhouzhuan(self):
        """点击100万大额周转"""
        self.daezhouzhuan().click()
        time.sleep(1)
        print("[OK] 点击【100万大额周转】")

    def click_huafeichongzhi(self):
        """点击话费充值"""
        self.huafeichongzhi().click()
        time.sleep(1)
        print("[OK] 点击【话费充值】")

    def click_wodekefu(self):
        """点击我的客服"""
        self.wodekefu().click()
        time.sleep(1)
        print("[OK] 点击【我的客服】")

    def click_gerenxinxi(self):
        """点击个人信息"""
        self.gerenxinxi().click()
        time.sleep(1)
        print("[OK] 点击【个人信息】")

    def get_middle_title_text(self):
        """获取中部标题文本（容错：元素不在当前页返回空串）"""
        desc = self.safe_desc(AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"优选持牌机构为您服务")]')
        print(f"[OK] 中部标题: {desc}")
        return desc

    def get_last_text(self):
        """获取底部额度文本（容错：元素不在当前页返回空串）"""
        desc = self.safe_desc(AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"200,000") and contains(@content-desc,"日利率0.02%")]')
        print(f"[OK] 底部额度: {desc}")
        return desc

    def click_btn_lingquedu(self):
        """点击领取额度按钮"""
        self.btn_lingquedu().click()
        time.sleep(1)
        print("[OK] 点击【领取额度】")

    # 导航栏操作
    def click_nav_tianxing(self):
        """点击底部【天星借钱】Tab"""
        self.open_tab("天星借钱")
        print("[OK] 切换到【天星借钱】")

    def click_nav_discover(self):
        """点击底部【发现】Tab"""
        self.open_tab("发现")
        print("[OK] 切换到【发现】")

    def click_nav_mine(self):
        """点击底部【我的】Tab"""
        self.open_tab("我的")
        print("[OK] 切换到【我的】")