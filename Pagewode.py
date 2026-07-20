import time
from appium.webdriver.common.appiumby import AppiumBy
from BasePage import BasePage

class Pagewode(BasePage):

    def btn_wodexiaoxi(self):
        return self.find_by_accessibility('我的消息')

    def btn_shezhi(self):
        return self.find_by_accessibility('设置')

    def bianjigerenxinxi(self):
        xpath='//android.view.View[@content-desc="编辑"]/android.widget.ImageView[1]'
        return self.find_by_xpath(xpath)

    def btn_qushiming(self):
        return self.find_by_accessibility('去实名')

    def youhuiquan(self):
        # 优惠券：原来只匹配 View[@content-desc]，“我的”页可能用 TextView/text 属性呈现，
        # 容器类型不同就匹配不到。改为：任意元素，content-desc 或 text 含“优惠券”。
        xpath='//*[contains(@content-desc,"优惠券") or contains(@text,"优惠券")]'
        return self.find_by_xpath(xpath)

    def yue(self):
        xpath='//android.view.View[contains(@content-desc,"余额")]'
        return self.find_by_xpath(xpath)

    def yinhangka(self):
        xpath='//android.view.View[contains(@content-desc,"银行卡")]'
        return self.find_by_xpath(xpath)

    def wodezichan(self):
        xpath='//android.view.View[contains(@content-desc,"我的资产")]'
        return self.find_by_xpath(xpath)

    def zongkejieedu(self):
        xpath='//android.view.View[contains(@content-desc,"总可借额度")]'
        return self.find_by_xpath(xpath)

    def wodebaodan(self):
        xpath='//android.view.View[contains(@content-desc,"我的保单")]'
        return self.find_by_xpath(xpath)

    def wodezhangdan(self):
        xpath='//android.view.View[contains(@content-desc,"我的账单")]'
        return self.find_by_xpath(xpath)

    def btn_txjq(self):
        xpath='//android.view.View[contains(@content-desc,"天星借钱")]'
        return self.find_by_xpath(xpath)

    def btn_sjcz(self):
        return self.find_by_accessibility('手机充值')

    def btn_hkgj(self):
        xpath='//android.view.View[contains(@content-desc,"还款管家")]'
        return self.find_by_xpath(xpath)

    def btn_lqk(self):
        return self.find_by_accessibility(' 零钱卡')

    def btn_xyk(self):
        xpath='//android.view.View[contains(@content-desc,"信用卡")]'
        return self.find_by_xpath(xpath)

    def btn_flzx(self):
        return self.find_by_accessibility('福利中心')

    def btn_jqzm(self):
        return self.find_by_accessibility('结清证明')

    def btn_wdzd(self):
        xpath='//android.view.View[contains(@content-desc,"我的账单")]'
        return self.find_by_xpath(xpath)

    def last_lbt(self):
        xpath='//android.view.View[contains(@content-desc,"小米联名卡探索版专享")]'
        return self.find_by_xpath(xpath)

    def btn_wdkf(self):
        return self.find_by_accessibility('我的客服')
    # 导航栏
    def nav_tianxing(self):
        return self.find_by_accessibility("天星借钱")

    def nav_discover(self):
        return self.find_by_accessibility("发现")

    def nav_mine(self):
        return self.find_by_accessibility("我的")

    # ========== 页面操作方法 ==========

    def click_wodexiaoxi(self):
        """点击我的消息"""
        self.btn_wodexiaoxi().click()
        time.sleep(1)
        print("[OK] 点击【我的消息】")

    def click_shezhi(self):
        """点击设置"""
        self.btn_shezhi().click()
        time.sleep(1)
        print("[OK] 点击【设置】")

    def click_bianjigerenxinxi(self):
        """点击编辑个人信息"""
        self.bianjigerenxinxi().click()
        time.sleep(1)
        print("[OK] 点击【编辑个人信息】")

    def click_qushiming(self):
        """点击去实名"""
        self.btn_qushiming().click()
        time.sleep(1)
        print("[OK] 点击【去实名】")

    def click_youhuiquan(self):
        """点击优惠券"""
        self.youhuiquan().click()
        time.sleep(1)
        print("[OK] 点击【优惠券】")

    def click_yue(self):
        """点击余额"""
        self.yue().click()
        time.sleep(1)
        print("[OK] 点击【余额】")

    def click_yinhangka(self):
        """点击银行卡"""
        self.yinhangka().click()
        time.sleep(1)
        print("[OK] 点击【银行卡】")

    def click_wodezichan(self):
        """点击我的资产"""
        self.wodezichan().click()
        time.sleep(1)
        print("[OK] 点击【我的资产】")

    def click_zongkejieedu(self):
        """点击总可借额度"""
        self.zongkejieedu().click()
        time.sleep(1)
        print("[OK] 点击【总可借额度】")

    def click_wodebaodan(self):
        """点击我的保单"""
        self.wodebaodan().click()
        time.sleep(1)
        print("[OK] 点击【我的保单】")

    def click_wodezhangdan(self):
        """点击我的账单"""
        self.wodezhangdan().click()
        time.sleep(1)
        print("[OK] 点击【我的账单】")

    def click_txjq(self):
        """点击天星借钱（最高20万）"""
        self.btn_txjq().click()
        time.sleep(1)
        print("[OK] 点击【天星借钱】")

    def click_sjcz(self):
        """点击手机充值"""
        self.btn_sjcz().click()
        time.sleep(1)
        print("[OK] 点击【手机充值】")

    def click_hkgj(self):
        """点击还款管家"""
        self.btn_hkgj().click()
        time.sleep(1)
        print("[OK] 点击【还款管家】")

    def click_lqk(self):
        """点击零钱卡"""
        self.btn_lqk().click()
        time.sleep(1)
        print("[OK] 点击【零钱卡】")

    def click_xyk(self):
        """点击信用卡"""
        self.btn_xyk().click()
        time.sleep(1)
        print("[OK] 点击【信用卡】")

    def click_flzx(self):
        """点击福利中心"""
        self.btn_flzx().click()
        time.sleep(1)
        print("[OK] 点击【福利中心】")

    def click_jqzm(self):
        """点击结清证明"""
        self.btn_jqzm().click()
        time.sleep(1)
        print("[OK] 点击【结清证明】")

    def click_wdzd(self):
        """点击我的账单（导航区域）"""
        self.btn_wdzd().click()
        time.sleep(1)
        print("[OK] 点击【我的账单】")

    def click_last_lbt(self):
        """点击底部轮播图"""
        self.last_lbt().click()
        time.sleep(1)
        print("[OK] 点击【底部轮播图】")

    def click_wdkf(self):
        """点击我的客服"""
        self.btn_wdkf().click()
        time.sleep(1)
        print("[OK] 点击【我的客服】")

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