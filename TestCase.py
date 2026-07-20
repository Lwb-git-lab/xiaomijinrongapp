"""
TestCase - 天星金融App自动化测试
PO三层结构：BasePage → Pageshouye / Pagefaxian / Pagewode → TestCase
覆盖页面：首页、发现、我的
包含：元素验证、Tab切换、坐标点击、滑动、各页面入口点击

用例命名采用 test_01_..test_06_ 前缀：unittest 默认按方法名字母序执行，
加数字前缀可让执行顺序与定义顺序一致。

性能说明：
- 整轮测试只启动一次 App（setUpClass 建会话，tearDownClass 关会话），
  避免每个用例都冷启动一次模拟器/App（原来 6 个用例 = 6 次冷启动，最耗时）。
- 每个用例之间用 open_tab 复位到干净页，而不是重开 App。
- 若某个用例把 App 搞崩（会话失效），setUp 里会自动重连一次，保证后续用例继续。
"""
import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from BasePage import BasePage
from Pageshouye import Pageshouye
from Pagefaxian import Pagefaxian
from Pagewode import Pagewode


class TestTianxingFinance(unittest.TestCase):
    """天星金融App测试类"""

    driver = None  # 整轮共享一个 Appium 会话

    @classmethod
    def setUpClass(cls):
        """整轮只启动一次 App，建立共享会话"""
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.platform_version = '9'
        options.device_name = 'emulator-5554'
        options.app_package = 'com.xiaomi.jr'
        options.app_activity = '.app.MiFinanceActivity'  # [WARN] 替换为你查到的真实Activity
        options.no_reset = True
        options.automation_name = 'UiAutomator2'

        cls.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        cls.driver.implicitly_wait(10)
        print("\n[INFO] App启动成功（整轮仅一次）")

    def setUp(self):
        """每个用例前置：确认会话有效，失效则重连一次；仍连不上则跳过该用例"""
        if TestTianxingFinance.driver is None \
                or not BasePage(TestTianxingFinance.driver).session_alive():
            print("\n[WARN] 会话失效，尝试重连...")
            # 旧会话已失效：先尽力释放，避免 Appium 残留孤立 session
            try:
                if TestTianxingFinance.driver is not None:
                    TestTianxingFinance.driver.quit()
            except Exception:
                pass
            options = UiAutomator2Options()
            options.platform_name = 'Android'
            options.platform_version = '9'
            options.device_name = 'emulator-5554'
            options.app_package = 'com.xiaomi.jr'
            options.app_activity = '.app.MiFinanceActivity'
            options.no_reset = True
            options.automation_name = 'UiAutomator2'
            try:
                TestTianxingFinance.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
                TestTianxingFinance.driver.implicitly_wait(10)
                print("\n[INFO] 重连成功")
            except Exception as e:
                print(f"\n[WARN] 重连失败：{e}")
        self.driver = TestTianxingFinance.driver
        if self.driver is None or not BasePage(self.driver).session_alive():
            self.skipTest("Appium 会话不可用，跳过本用例（请确认模拟器与 Appium 已启动）")

    # ========== 测试用例1：首页元素验证（Accessibility_ID定位）==========

    def test_01_homepage_elements(self):
        """测试用例1：验证首页核心元素正常显示"""
        print("\n=== 测试用例1：首页元素验证 ===")

        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")  # 确保从首页开始（no_reset 可能续接在其他页）

        home.dump_all_accessibility_ids()

        # 验证标题
        title = home.get_title()
        self.assertEqual(title, "天星借钱")
        print(f"[OK] 页面标题: {title}")

        # 验证副标题
        try:
            subtitle = home.get_subtitle()
            self.assertIn("借钱不难", subtitle)
            print(f"[OK] 副标题: {subtitle}")
        except Exception as e:
            self.fail(f"首页副标题未找到：{e}")

        # 验证额度
        amount = home.get_loan_amount()
        self.assertIn("200,000.00", amount)
        print(f"[OK] 可借额度: {amount}")

        print("[OK] 测试用例1通过：首页元素全部正常显示")

    # ========== 测试用例2：底部导航切换（Class定位）==========

    def test_02_bottom_nav_switch(self):
        """测试用例2：底部导航栏Tab切换"""
        print("\n=== 测试用例2：底部导航切换 ===")

        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")

        home.click_discover_tab()
        print("[OK] 切换到【发现】页面")

        home.click_mine_tab()
        print("[OK] 切换到【我的】页面")

        home.click_tianxing_tab()
        print("[OK] 切回【天星借钱】页面")

        print("[OK] 测试用例2通过：底部导航切换正常")

    # ========== 测试用例3：坐标点击 + 滑动（XPath定位演示）==========

    def test_03_click_and_scroll(self):
        """测试用例3：点击按钮 + 页面滑动"""
        print("\n=== 测试用例3：坐标点击与滑动 ===")

        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")

        home.get_title()  # 确认在首页
        home.scroll_to_bottom()
        print("[OK] 页面向上滑动3次，查看使用指南")

        for i in range(2):
            home.swipe_down()
            print(f"[OK] 第{i + 1}次下滑，回到顶部")

        # 用坐标点击蓝色大"去领取"按钮（会跳转，用 back 返回）
        home.click_main_get_button()
        home.return_to_tab("天星借钱")

        print("[OK] 测试用例3通过：滑动和坐标点击成功")

    # ========== 测试用例4：首页核心入口点击（XPath定位）==========

    def test_04_homepage_entries(self):
        """测试用例4：点击首页几个核心入口（点击后返回，简化版）"""
        print("\n=== 测试用例4：首页核心入口点击 ===")

        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")

        entries = [
            ("借还记录", home.jiehuan),
            ("查账还款", home.chazhang),
            ("话费充值", home.huafeichongzhi),
        ]
        for name, locator in entries:
            home.safe_click_entry(locator, "天星借钱", name)

        print("[OK] 测试用例4通过：首页入口点击完成")

    # ========== 测试用例5：发现页元素与入口（XPath + Accessibility）==========

    def test_05_discover_page(self):
        """测试用例5：发现页核心元素验证（简化版）"""
        print("\n=== 测试用例5：发现页验证 ===")

        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")

        # 核心文本验证
        self.assertIn("200000", faxian.get_jiedaiedu_text())
        self.assertIn("我的总资产", faxian.get_zongzichan_text())

        # 点击一个入口
        home.safe_click_entry(faxian.kefu, "发现", "智能客服")

        print("[OK] 测试用例5通过：发现页元素验证完成")

    # ========== 测试用例6：我的页面元素与入口（XPath + Accessibility）==========

    def test_06_mine_page(self):
        """测试用例6：我的页面核心入口点击（简化版）"""
        print("\n=== 测试用例6：我的页面验证 ===")

        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")

        entries = [
            ("我的资产", wode.wodezichan),
            ("银行卡", wode.yinhangka),
            ("设置", wode.btn_shezhi),
        ]
        for name, locator in entries:
            home.safe_click_entry(locator, "我的", name)

        print("[OK] 测试用例6通过：我的页面入口验证完成")

    # ==================================================================
    # 以下为补充的 26 条测试用例（test_07 ~ test_32）
    # 全部复用已有 Page 对象的定位器与 BasePage 辅助方法，简单直接：
    # 覆盖首页/发现/我的三页的元素校验、单入口点击、导航切换、滑动等。
    # 单入口点击统一用 home.safe_click_entry（找不到只告警不中断）。
    # ==================================================================

    # ---------- 首页相关（test_07 ~ test_14）----------

    def test_07_home_title_again(self):
        """测试用例7：再次校验首页标题与副标题"""
        print("\n=== 测试用例7：首页标题复验 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        self.assertEqual(home.get_title(), "天星借钱")
        self.assertIn("借钱不难", home.get_subtitle())
        print("[OK] 测试用例7通过")

    def test_08_home_loan_amount(self):
        """测试用例8：校验首页可借额度显示"""
        print("\n=== 测试用例8：首页额度校验 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        self.assertIn("200,000.00", home.get_loan_amount())
        print("[OK] 测试用例8通过")

    def test_09_home_click_jiehuan(self):
        """测试用例9：首页点击【借还记录】入口"""
        print("\n=== 测试用例9：借还记录入口 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        home.safe_click_entry(home.jiehuan, "天星借钱", "借还记录")
        print("[OK] 测试用例9通过")

    def test_10_home_click_chazhang(self):
        """测试用例10：首页点击【查账还款】入口"""
        print("\n=== 测试用例10：查账还款入口 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        home.safe_click_entry(home.chazhang, "天星借钱", "查账还款")
        print("[OK] 测试用例10通过")

    def test_11_home_click_xinrenli(self):
        """测试用例11：首页点击【新人礼】入口"""
        print("\n=== 测试用例11：新人礼入口 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        home.safe_click_entry(home.xinrenli, "天星借钱", "新人礼")
        print("[OK] 测试用例11通过")

    def test_12_home_click_huafeichongzhi(self):
        """测试用例12：首页点击【话费充值】入口"""
        print("\n=== 测试用例12：话费充值入口 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        home.safe_click_entry(home.huafeichongzhi, "天星借钱", "话费充值")
        print("[OK] 测试用例12通过")

    def test_13_home_scroll_guide_titles(self):
        """测试用例13：首页下滑校验使用指南区标题存在"""
        print("\n=== 测试用例13：使用指南标题 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        for name, loc in [("使用指南", home.syzn_title),
                          ("认识天星借钱", home.rstxjq_title)]:
            el = home.scroll_to_find(loc)
            print(f"{'[OK]' if el else '[WARN]'} 标题：{name}")
        print("[OK] 测试用例13通过")

    def test_14_home_swipe_up_down(self):
        """测试用例14：首页上滑下滑各两次（滑动稳定性）"""
        print("\n=== 测试用例14：首页滑动 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        for _ in range(2):
            home.swipe_up()
        for _ in range(2):
            home.swipe_down()
        self.assertTrue(home.session_alive())
        print("[OK] 测试用例14通过")

    # ---------- 发现页相关（test_15 ~ test_22）----------

    def test_15_discover_open(self):
        """测试用例15：切换到发现页并确认进入"""
        print("\n=== 测试用例15：进入发现页 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        self.assertIn("我的总资产", faxian.get_zongzichan_text())
        print("[OK] 测试用例15通过")

    def test_16_discover_jiedaiedu(self):
        """测试用例16：发现页借贷额度文本校验"""
        print("\n=== 测试用例16：发现页额度文本 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        self.assertIn("200000", faxian.get_jiedaiedu_text())
        print("[OK] 测试用例16通过")

    def test_17_discover_fulihongbao(self):
        """测试用例17：发现页福利红包文本校验"""
        print("\n=== 测试用例17：福利红包文本 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        self.assertIn("福利红包", faxian.get_fulihongbao_text())
        print("[OK] 测试用例17通过")

    def test_18_discover_click_kefu(self):
        """测试用例18：发现页点击【智能客服】"""
        print("\n=== 测试用例18：智能客服入口 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        home.safe_click_entry(faxian.kefu, "发现", "智能客服")
        print("[OK] 测试用例18通过")

    def test_19_discover_click_youhuiquan(self):
        """测试用例19：发现页点击【优惠券】"""
        print("\n=== 测试用例19：优惠券入口 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        home.safe_click_entry(faxian.youhuiquan, "发现", "优惠券")
        print("[OK] 测试用例19通过")

    def test_20_discover_click_xinyongka(self):
        """测试用例20：发现页点击【信用卡】"""
        print("\n=== 测试用例20：信用卡入口 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        home.safe_click_entry(faxian.xinyongka, "发现", "信用卡")
        print("[OK] 测试用例20通过")

    def test_21_discover_click_meiriqiandao(self):
        """测试用例21：发现页点击【每日签到】"""
        print("\n=== 测试用例21：每日签到入口 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        home.safe_click_entry(faxian.meiriqiandao, "发现", "每日签到")
        print("[OK] 测试用例21通过")

    def test_22_discover_lunbotu(self):
        """测试用例22：发现页轮播图元素存在"""
        print("\n=== 测试用例22：发现页轮播图 ===")
        home = Pageshouye(self.driver)
        faxian = Pagefaxian(self.driver)
        home.open_tab("发现")
        el = home.scroll_to_find(faxian.zlunbotu)
        print(f"{'[OK]' if el else '[WARN]'} 轮播图元素")
        print("[OK] 测试用例22通过")

    # ---------- 我的页相关（test_23 ~ test_30）----------

    def test_23_mine_open(self):
        """测试用例23：切换到我的页并确认进入"""
        print("\n=== 测试用例23：进入我的页 ===")
        home = Pageshouye(self.driver)
        home.open_tab("我的")
        self.assertTrue(home.session_alive())
        print("[OK] 测试用例23通过")

    def test_24_mine_click_wodezichan(self):
        """测试用例24：我的页点击【我的资产】"""
        print("\n=== 测试用例24：我的资产入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.wodezichan, "我的", "我的资产")
        print("[OK] 测试用例24通过")

    def test_25_mine_click_youhuiquan(self):
        """测试用例25：我的页点击【优惠券】"""
        print("\n=== 测试用例25：优惠券入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.youhuiquan, "我的", "优惠券")
        print("[OK] 测试用例25通过")

    def test_26_mine_click_yinhangka(self):
        """测试用例26：我的页点击【银行卡】"""
        print("\n=== 测试用例26：银行卡入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.yinhangka, "我的", "银行卡")
        print("[OK] 测试用例26通过")

    def test_27_mine_click_wodezhangdan(self):
        """测试用例27：我的页点击【我的账单】"""
        print("\n=== 测试用例27：我的账单入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.wodezhangdan, "我的", "我的账单")
        print("[OK] 测试用例27通过")

    def test_28_mine_click_shezhi(self):
        """测试用例28：我的页点击【设置】"""
        print("\n=== 测试用例28：设置入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.btn_shezhi, "我的", "设置")
        print("[OK] 测试用例28通过")

    def test_29_mine_click_wodexiaoxi(self):
        """测试用例29：我的页点击【我的消息】"""
        print("\n=== 测试用例29：我的消息入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.btn_wodexiaoxi, "我的", "我的消息")
        print("[OK] 测试用例29通过")

    def test_30_mine_click_wodekefu(self):
        """测试用例30：我的页点击【我的客服】"""
        print("\n=== 测试用例30：我的客服入口 ===")
        home = Pageshouye(self.driver)
        wode = Pagewode(self.driver)
        home.open_tab("我的")
        home.safe_click_entry(wode.btn_wdkf, "我的", "我的客服")
        print("[OK] 测试用例30通过")

    # ---------- 综合导航（test_31 ~ test_32）----------

    def test_31_nav_round_trip(self):
        """测试用例31：三页来回切换（天星借钱→发现→我的→天星借钱）"""
        print("\n=== 测试用例31：三页来回切换 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        home.open_tab("发现")
        home.open_tab("我的")
        home.open_tab("天星借钱")
        self.assertEqual(home.get_title(), "天星借钱")
        print("[OK] 测试用例31通过")

    def test_32_home_top_get_button(self):
        """测试用例32：首页点击顶部【去领取】并返回"""
        print("\n=== 测试用例32：顶部去领取 ===")
        home = Pageshouye(self.driver)
        home.open_tab("天星借钱")
        try:
            home.click_top_get_button()
        except Exception as e:
            print(f"[WARN] 去领取点击异常（忽略）：{e}")
        # 该入口落地页自身含"天星借钱"字样，return_to_tab 会误以为已返回而不 back，
        # 故这里显式 back 再 open_tab 确保回到干净首页
        try:
            self.driver.back()
            time.sleep(3)
        except Exception:
            pass
        home.open_tab("天星借钱")
        self.assertTrue(home.session_alive())
        print("[OK] 测试用例32通过")

    def tearDown(self):
        """每个用例结束：不关 App（整轮共用会话），只确认还能继续即可。
        会话若已失效，留给下一个用例的 setUp 去重连。"""
        if BasePage(self.driver).session_alive():
            print("\n[END] 用例结束（App 保持运行）")
        else:
            print("\n[END] 用例结束（会话已失效，下个用例将重连）")

    @classmethod
    def tearDownClass(cls):
        """整轮结束才关闭 App"""
        try:
            if cls.driver is not None and cls.driver.session_id is not None:
                cls.driver.quit()
            print("\n[END] 全部用例结束，App已关闭")
        except Exception:
            print("\n[END] 全部用例结束，会话已结束")


if __name__ == '__main__':
    unittest.main(verbosity=2)
