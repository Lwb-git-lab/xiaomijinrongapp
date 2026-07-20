from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from contextlib import contextmanager


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._implicit_wait = 10  # 与主 suite 保持一致

    @contextmanager
    def _fast_find(self, timeout=1.5):
        """临时降低隐式等待，用于「轮询查找」场景（滑动逐步查找元素）。

        默认隐式等待是 10s，find_element 找不到时会阻塞整段等待；
        在 scroll_to_find / safe_click_entry 的循环里每轮都阻塞 10s 会显得像卡死。
        这里把等待压到 ~1.5s，找到找不到都快速返回，由外层重试决定下一步。"""
        original = self._implicit_wait
        self.driver.implicitly_wait(timeout)
        self._implicit_wait = timeout
        try:
            yield
        finally:
            self.driver.implicitly_wait(original)
            self._implicit_wait = original

    @contextmanager
    def _fast_wait(self):
        """把隐式等待临时设为 0，用于配合 WebDriverWait 的显式等待场景。

        坑：Appium/Selenium 里隐式等待和显式等待会「叠加」——
        当隐式等待=10s 时，WebDriverWait(d, 3) 实际最坏要等 3×(10+ε) 秒才判失败。
        进入本上下文后隐式等待=0，WebDriverWait 就忠于自己的 timeout。"""
        original = self._implicit_wait
        self.driver.implicitly_wait(0)
        self._implicit_wait = 0
        try:
            yield
        finally:
            self.driver.implicitly_wait(original)
            self._implicit_wait = original

    # ========== 等待机制 ==========

    def wait_element(self, by, value, timeout=10):
        """显式等待元素出现（直接 find_element 形式）"""
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(by, value)
        )

    def wait_clickable(self, by, value, timeout=10):
        """显式等待元素可点击"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    # ========== 定位方式（AppiumBy 直接形式）==========

    def find_by_id(self, id_value):
        """ID 定位：driver.find_element(AppiumBy.ID, id_value)"""
        return self.driver.find_element(AppiumBy.ID, id_value)

    def find_by_accessibility(self, text):
        """Accessibility ID 定位（Flutter 的 content-desc）"""
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, text)

    def find_by_class(self, class_name):
        """Class 名称定位"""
        return self.driver.find_element(AppiumBy.CLASS_NAME, class_name)

    def find_by_xpath(self, xpath):
        """XPath 定位"""
        return self.driver.find_element(AppiumBy.XPATH, xpath)

    # ========== 通用操作 ==========

    def click_accessibility(self, text):
        """点击Accessibility元素"""
        element = self.find_by_accessibility(text)
        element.click()
        time.sleep(0.6)

    def tap_by_coordinates(self, x, y):
        """坐标点击（Flutter备用方案）"""
        self.driver.tap([(x, y)])
        time.sleep(0.6)

    def get_text(self, by, value):
        """获取元素文本"""
        element = self.wait_element(by, value)
        return element.text

    def safe_desc(self, by, value, timeout=3):
        """容错取元素 content-desc：找不到返回空串而非抛异常。
        给「当前页可能不含该元素」的文本校验用——让用例用 assertIn 收场，
        而不是在 get 阶段就抛 WebDriverException 让整个用例变 ERROR。"""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(by, value))
            return el.get_attribute('content-desc') or ''
        except Exception:
            return ''

    def get_attribute(self, by, value, attr):
        """获取元素属性"""
        element = self.wait_element(by, value)
        return element.get_attribute(attr)

    def swipe_up(self):
        """向上滑动（对 W3C 临时异常做重试，避免 app 未稳定时滑动失败）"""
        self._safe_swipe(0.75, 0.25)

    def swipe_down(self):
        """向下滑动（对 W3C 临时异常做重试）"""
        self._safe_swipe(0.25, 0.75)

    def _safe_swipe(self, ratio_start, ratio_end):
        """滑动：app 未稳定 / UI 无响应时会抛 InvalidElementStateException，
        这种情况滑动本就是尽力而为，绝不能抛异常把用例搞崩；
        连续失败说明 UI 已假死，直接放弃本次滑动。"""
        for attempt in range(3):
            try:
                size = self.driver.get_window_size()
                x = size['width'] // 2
                y_start = int(size['height'] * ratio_start)
                y_end = int(size['height'] * ratio_end)
                self.driver.swipe(x, y_start, x, y_end, 800)
                time.sleep(0.5)
                return
            except Exception:
                if attempt < 2:
                    time.sleep(1.0)  # app 未稳定，稍后重试
                else:
                    return  # 最后一次仍失败：放弃本次滑动，不抛异常

    def dump_all_accessibility_ids(self):
        """打印当前页面所有元素的content-desc，用于调试定位"""
        import re
        source = self.driver.page_source
        descs = re.findall(r'content-desc="([^"]*)"', source)
        descs = [d for d in descs if d]
        print(f"\n=== 页面所有 content-desc 元素（共{len(descs)}个）===")
        for d in sorted(set(descs)):
            print(f"  - {d}")

    # ========== 导航与返回 ==========

    def is_present(self, by, value, timeout=3):
        """元素是否存在（不抛异常，用于判断当前所在页面）"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(by, value))
            return True
        except Exception:
            return False

    def session_alive(self):
        """会话是否仍有效（app 崩溃/H5 卡死会导致 InvalidSessionId）"""
        try:
            self.driver.get_window_size()
            return True
        except Exception:
            return False

    def _click_tab(self, tab_name, timeout=2):
        """点击底部导航栏的 Tab。

        坑：首页标题的 content-desc 也是"天星借钱"，与底部导航同名。
        find_element 按 DOM 顺序返回，会先命中标题（标题在导航之前渲染），
        点到标题是无效操作，导航从未真正切换，后续返回/复位全乱。
        这里取所有同名元素里 y 坐标最靠下的那个 = 真正的底部导航栏，
        并用 find_elements + 短等待，导航不可见时快速返回 False 不阻塞。

        Flutter 重渲染极快，find_elements 拿到的元素引用隔一次 HTTP 调用
        （读 location / 点 click）就可能 stale。所以「查找→取坐标→点击」
        整体重试：任一步抛 StaleElementReference 就重新 find_elements 拿
        新鲜引用，最多 3 次，避免 stale 冒泡成用例 ERROR。"""
        original = self._implicit_wait
        self.driver.implicitly_wait(timeout)
        self._implicit_wait = timeout
        try:
            for _ in range(3):
                try:
                    els = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, tab_name)
                    if not els:
                        return False
                    # 取 y 坐标最靠下的元素（= 真实底部导航，而非同名标题）
                    target = max(els, key=lambda e: e.location.get('y', 0))
                    target.click()
                    return True
                except Exception:
                    time.sleep(0.3)
                    continue
            return False
        finally:
            self.driver.implicitly_wait(original)
            self._implicit_wait = original

    def open_tab(self, tab_name):
        """切到指定底部 Tab：点击底部导航（取同名最靠下的元素 = 真实导航）。"""
        if not self.session_alive():
            print(f"[WARN] 会话已失效，无法切换 Tab: {tab_name}")
            return
        if self._click_tab(tab_name):
            time.sleep(0.8)
        else:
            print(f"[WARN] 点击 Tab '{tab_name}' 失败（导航未找到）")

    def return_to_tab(self, tab_name):
        """从子页面返回目标 Tab：先尝试点底部 Tab（能点到说明已在 Tab 页），
        点不到则 back 一次再点（说明在子页面/无导航栏），back 无效则放弃。
        统一走 _click_tab：只命中真实底部导航，且导航不可见时快速返回不阻塞。"""
        if not self.session_alive():
            return
        # 尝试直接点 Tab（已在 Tab 页时最安全，不会误退出 App）
        if self._click_tab(tab_name):
            time.sleep(0.8)
            return
        # 在子页面，底部导航不可见：back 一次退出
        try:
            self.driver.back()
            time.sleep(0.5)
        except Exception:
            pass
        if not self.session_alive():
            return
        # 再点一次 Tab
        if self._click_tab(tab_name):
            time.sleep(0.8)

    def _reset_to_top(self, times=2):
        """连续下滑回到页面顶部，消除上一次操作遗留的滚动位置"""
        for _ in range(times):
            self.swipe_down()

    def safe_click_entry(self, locator_fn, tab_name, entry_label=""):
        """点击某入口：确保在目标页 → 双向滑动查找并点击 → 可靠返回目标页。
        找不到只告警跳过，不中断用例；会话已失效则直接跳过。
        双向：前 4 次 swipe_up（看底部），后 4 次 swipe_down（看顶部）。"""
        if not self.session_alive():
            print(f"[WARN] 会话已失效，跳过：{entry_label}")
            return
        self.open_tab(tab_name)
        self._reset_to_top()
        clicked = False
        with self._fast_find(1.5):
            for i in range(8):
                if not self.session_alive():
                    break
                try:
                    locator_fn().click()
                    time.sleep(0.6)
                    clicked = True
                    break
                except Exception:
                    if i < 4:
                        self.swipe_up()
                    else:
                        self.swipe_down()
        if clicked:
            print(f"[OK] 点击入口：{entry_label}")
        else:
            print(f"[WARN] 入口未找到，跳过：{entry_label}")
        self.return_to_tab(tab_name)

    def scroll_to_find(self, locator_fn, max_swipes=6):
        """双向查找元素：前一半 swipe_up（看底部），后一半 swipe_down（看顶部）。
        找到返回元素，找不到返回 None。"""
        with self._fast_find(1.5):
            for i in range(max_swipes):
                if not self.session_alive():
                    return None
                try:
                    return locator_fn()
                except Exception:
                    if i < max_swipes // 2:
                        self.swipe_up()
                    else:
                        self.swipe_down()
            for _ in range(3):
                self.swipe_down()
        return None