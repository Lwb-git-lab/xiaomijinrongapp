"""
HomePage - 天星金融首页
根据Appium Inspector截图提取的元素：
- 标题：天星借钱
- 副标题：借钱不难
- 顶部"去领取"按钮
- 额度：200,000.00
- 底部蓝色"去领取"大按钮
- 底部导航：天星借钱、发现、我的
"""
from BasePage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
import time


class Pageshouye(BasePage):

    # ========== 页面元素定位 ==========

    def title_element(self):
        """页面标题：天星借钱"""
        return self.find_by_accessibility("天星借钱")

    def subtitle_element(self):
        """副标题：借钱不难，全面解决您的借款难题"""
        return self.find_by_accessibility("借钱不难，全面解决您的借款难题")

    def top_get_button(self):
        """顶部"去领取"小按钮"""
        return self.find_by_accessibility("去领取")

    def loan_amount_element(self):
        """额度显示容器：content-desc 为"最高可借额度（元）\n200,000.00\n利率..."整块文本"""
        xpath = '//*[contains(@content-desc, "200,000.00")]'
        return self.find_by_xpath(xpath)

    def main_get_button(self):
        """底部蓝色大"去领取"按钮（长文案块：｜最高得50元现金红包…去领取）。
        注意：顶部小按钮的 accessibility_id 也是"去领取"，用 find_by_accessibility
        只会命中第一个（顶部那个）。这里用 contains 命中大按钮独有的长文案，
        避免和 top_get_button 抢同一个元素。"""
        xpath = '//*[contains(@content-desc,"最高得50元现金红包")]'
        return self.find_by_xpath(xpath)

    def jiehuan(self):
        # 借还记录按钮
        xpath='//android.view.View[@content-desc="借还记录"]'
        return self.find_by_xpath(xpath)

    def chazhang(self):
        # 查账还款按钮
        xpath='//android.view.View[@content-desc="查账还款"]'
        return self.find_by_xpath(xpath)

    def xinrenli(self):
        # 新人礼按钮
        xpath='//android.view.View[@content-desc="新人礼"]'
        return self.find_by_xpath(xpath)

    def youhunquan(self):
        # 优惠券按钮
        xpath='//android.view.View[@content-desc="优惠券"]'
        return self.find_by_xpath(xpath)

    def chezhudai_s(self):
        # 100万车主贷入口：原来写死"100万 车主贷"（中间带空格）常常匹配不到，
        # 真实 content-desc 的空格/换行可能不同。改为同时包含"100万"和"车主贷"，
        # 对空格/顺序都容错。
        xpath='//android.view.View[contains(@content-desc,"100万") and contains(@content-desc,"车主贷")]'
        return self.find_by_xpath(xpath)

    def jieqingzhengming(self):
        xpath='//android.view.View[@content-desc="结清证明"]'
        return self.find_by_xpath(xpath)

    def huafeichongzhi(self):
        xpath='//android.view.View[@content-desc="话费充值"]'
        return self.find_by_xpath(xpath)

    def lunbotudaohanglan(self):
        xpath='//android.view.View[@content-desc="立即查看"]'
        return self.find_by_xpath(xpath)

    def dejpzq_title(self):
        return self.find_by_accessibility("大额精品专区")

    def chezhudai_x(self):
        xpath='//android.view.View[contains(@content-desc,"车主贷") and contains(@content-desc,"最高100万")]'
        return self.find_by_xpath(xpath)

    def fangzhudai(self):
        xpath='//android.view.View[contains(@content-desc,"房主贷") and contains(@content-desc,"最高6000万")]'
        return self.find_by_xpath(xpath)

    def syzn_title(self):
        return self.find_by_accessibility("使用指南")

    def fangpianshouce(self):
        return self.find_by_accessibility("防诈骗指南")

    def huankuanzhinan(self):
        return self.find_by_accessibility("关于还款")

    def rstxjq_title(self):
        return self.find_by_accessibility("认识天星借钱")

    def juheduojiajigou(self):
        xpath='//android.view.View[@content-desc=" 聚合多家机构 简单便捷"]'
        return self.find_by_xpath(xpath)

    def youxuanhezuocahnpin(self):
        xpath='//android.view.View[@content-desc=" 优选合作产品 放心选择"]'
        return self.find_by_xpath(xpath)

    def bumanyisuishihuan(self):
        xpath='//android.view.View[@content-desc=" 不满意随时换 借钱不难"]'
        return self.find_by_xpath(xpath)

    # 底部导航栏
    def nav_tianxing(self):
        return self.find_by_accessibility("天星借钱")

    def nav_discover(self):
        return self.find_by_accessibility("发现")

    def nav_mine(self):
        return self.find_by_accessibility("我的")

    # ========== 页面操作方法 ==========

    def get_title(self):
        """获取页面标题（Flutter 的 accessibility_id 即文本）。
        返回真实元素文本，找不到抛 TimeoutException 让用例失败。"""
        return self.title_element().get_attribute('content-desc') or ''

    def get_subtitle(self):
        """获取副标题，返回真实元素文本"""
        return self.subtitle_element().get_attribute('content-desc') or ''

    def get_loan_amount(self):
        """获取可借额度（容器 content-desc 含 "200,000.00"），返回真实文本"""
        element = self.loan_amount_element()
        desc = element.get_attribute('content-desc') or ''
        if "200,000.00" not in desc:
            raise AssertionError(f"额度容器内未找到200,000.00，实际: {desc}")
        return desc

    def click_top_get_button(self):
        """点击顶部"去领取"按钮"""
        self.click_accessibility("去领取")
        print("[OK] 点击顶部'去领取'按钮")

    def click_main_get_button(self):
        """点击中间蓝色大"去领取"按钮"""
        # 如果顶部按钮点了，用坐标点中间的大按钮
        size = self.driver.get_window_size()
        x = int(size['width'] * 0.50)
        y = int(size['height'] * 0.72)
        self.tap_by_coordinates(x, y)
        print(f"[OK] 点击蓝色大'去领取'按钮 (坐标:{x},{y})")

    def click_discover_tab(self):
        """点击底部"发现"Tab"""
        self.open_tab("发现")
        print("[OK] 切换到底部【发现】Tab")

    def click_mine_tab(self):
        """点击底部"我的"Tab"""
        self.open_tab("我的")
        print("[OK] 切换到底部【我的】Tab")

    def click_tianxing_tab(self):
        """点击底部"天星借钱"Tab"""
        self.open_tab("天星借钱")
        print("[OK] 切换到底部【天星借钱】Tab")

    def scroll_to_bottom(self):
        """滚动到底部查看使用指南"""
        for i in range(3):
            self.swipe_up()
            print(f"[OK] 第{i+1}次上滑")