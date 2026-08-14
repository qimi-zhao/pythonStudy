("""findMyHouse.py

用法:
- 在文件头部编辑 `HOUSES` 列表，填写每个团地的 `name` 与 `url`。
- 编辑 `CHECK_TIMES`（24小时制字符串数组），如 ["09:00","18:00"]。
- 配置 Twilio 环境变量以发送短信：`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `TARGET_PHONE`。

脚本会在指定时间访问每个 URL，查找表格 tbody.rep_room 中的房源行（示例 HTML 结构见项目说明），
如果找到房源则解析并提取: 部屋名, 家賃(共益費), 間取り, 床面積, 階数，并发送短信通知（仅对新发现的房源去重）。
""")

import os
import time
from datetime import datetime
import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

try:
	from twilio.rest import Client
	_HAS_TWILIO = True
except Exception:
	_HAS_TWILIO = False

try:
	import schedule
except Exception:
	schedule = None

try:
	from playwright.sync_api import sync_playwright
	_HAS_PLAYWRIGHT = True
except Exception:
	_HAS_PLAYWRIGHT = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# --------------------
# User configuration (在这里填写)
# --------------------
# 每个条目: {"name": "显示名", "url": "https://..."}
HOUSES: List[Dict[str, str]] = [
	# 示例:
	# {"name": "UR 例子1", "url": "https://chintai.r6.ur-net.go.jp/chintai/..."},
	{"name": "サンヴァリエ日吉", "url": "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_3290.html"},
	{"name": "小杉御殿", "url": "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2660.html"},
	{"name": "シティコート元住吉", "url": "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_3410.html"},
	{"name": "大井六丁目", "url": "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1830.html"},
	{"name": "南六郷一丁目", "url": "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_2910.html"},
	{"name": "南六郷二丁目", "url": "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1960.html"},
	{"name": "シャレール新蒲田", "url": "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_5480.html"},
	{"name": "鶴見町第二", "url": "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1770.html"},
	{"name": "川崎日進", "url": "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1830.html"},
]

# 查询时间数组（24小时制），脚本会每天在这些时间点运行
CHECK_TIMES: List[str] = ["09:30", "10:30", "11:30", "13:30", "14:30", "15:30"]

# --------------------
# Twilio / 通知设置（使用环境变量更安全）
# --------------------
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')
TARGET_PHONE = os.getenv('TARGET_PHONE')

# --------------------
# Telegram 设置（Bot 推送）
# 在环境变量中设置: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
# --------------------
TELEGRAM_BOT_TOKEN = rf"***"
TELEGRAM_CHAT_ID = rf"***"
TELEGRAM_USERNAME = rf"***"

# HTTP headers
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; findMyHouse/1.0)"}

# Playwright render timing defaults (milliseconds)
RENDER_PAGE_TIMEOUT = 15000  # page.goto timeout
RENDER_WAIT_SELECTOR_TIMEOUT = 3000  # wait_for_selector timeout

# Internal state for de-dup
# seen_rooms[name] = set(of unique room ids or room names)
seen_rooms = {}


def fetch_html(url: str, timeout: int = 15) -> str:
	try:
		r = requests.get(url, timeout=timeout, headers=HEADERS)
		r.raise_for_status()
		return r.text
	except Exception as e:
		logging.warning(f"fetch failed {url}: {e}")
		return ""


def fetch_rendered_html(url: str, wait_selector: str = None, timeout: int = 30000) -> str:
	"""Use Playwright to render the page and return the HTML content. Returns empty string if Playwright unavailable or fails."""
	if not _HAS_PLAYWRIGHT:
		logging.info('Playwright not installed; skipping rendered fetch')
		return ""
	try:
		with sync_playwright() as pw:
			browser = pw.chromium.launch(headless=True)
			page = browser.new_page()
			# use networkidle to avoid waiting unnecessary long on resources
			try:
				page.goto(url, timeout=RENDER_PAGE_TIMEOUT, wait_until='networkidle')
			except Exception:
				# fallback to normal goto with same timeout
				try:
					page.goto(url, timeout=RENDER_PAGE_TIMEOUT)
				except Exception as e:
					logging.error(f'Playwright goto failed for {url}: {e}')
					browser.close()
					return ""

			if wait_selector:
				try:
					page.wait_for_selector(wait_selector, timeout=RENDER_WAIT_SELECTOR_TIMEOUT)
				except Exception:
					# selector didn't appear quickly; don't block too long
					logging.info(f"wait_for_selector('{wait_selector}') timed out after {RENDER_WAIT_SELECTOR_TIMEOUT}ms")
			else:
				# small pause to allow scripts to run briefly
				page.wait_for_timeout(800)

			html = page.content()
			browser.close()
			return html
	except Exception as e:
		logging.error(f'Playwright fetch failed for {url}: {e}')
		return ""


def parse_rooms(html: str) -> List[Dict[str, str]]:
	"""解析页面中房源表格，返回房源列表。如果没有房源返回空列表。

	解析规则基于用户提供的 HTML 示例：tbody.rep_room 中每个 .js-log-item tr（非 dn）为一条房源。
	提取字段: 部屋名(rep_room-name), 家賃(rep_room-price 与 rep_room-commonfee), 間取り(rep_room-type),
	床面積(rep_room-floor), 階数(rep_room-kai)。
	"""
	if not html:
		return []
	soup = BeautifulSoup(html, 'html.parser')
	tbody = soup.select_one('tbody.rep_room')

	# Build candidate row elements with fallbacks:
	candidates = []
	if tbody:
		candidates = list(tbody.select('tr.js-log-item'))
	else:
		# 1) global tr.js-log-item
		candidates = list(soup.select('tr.js-log-item'))
		# 2) if still empty, find elements with room-name and take their ancestor tr
		if not candidates:
			name_els = soup.select('.rep_room-name, .rep_room-name *')
			for el in name_els:
				tr = el.find_parent('tr')
				if tr is not None:
					candidates.append(tr)

	rows = []
	seen_trs = set()
	for tr in candidates:
		# avoid duplicates
		try:
			tr_id = id(tr)
		except Exception:
			tr_id = str(tr)
		if tr_id in seen_trs:
			continue
		seen_trs.add(tr_id)
		cls = tr.get('class') or []
		# 跳过带 dn 的行（示例中的图片/详情行）
		if 'dn' in cls:
			continue

		# 尝试获取唯一标识: data-log-key
		log_key = tr.get('data-log-key') or ''

		name_el = tr.select_one('.rep_room-name')
		room_name = name_el.get_text(strip=True) if name_el else ''

		# price selectors: try a few variants
		rent_el = tr.select_one('.rep_room-price') or tr.select_one('.item_price.rep_room-price') or tr.select_one('.item_price')
		rent = rent_el.get_text(strip=True) if rent_el else ''

		common_el = tr.select_one('.rep_room-commonfee') or tr.select_one('.item_commonfee')
		common = common_el.get_text(strip=True) if common_el else ''

		layout_el = tr.select_one('.rep_room-type')
		layout = layout_el.get_text(strip=True) if layout_el else ''

		area_el = tr.select_one('.rep_room-floor')
		area = area_el.get_text(strip=True) if area_el else ''

		floor_el = tr.select_one('.rep_room-kai')
		floor = floor_el.get_text(strip=True) if floor_el else ''

		rows.append({
			'id': log_key or room_name,
			'name': room_name,
			'rent': rent,
			'common': common,
			'layout': layout,
			'area': area,
			'floor': floor,
		})

	return rows


def send_sms(message: str) -> bool:
	if _HAS_TWILIO and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM and TARGET_PHONE:
		try:
			client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
			client.messages.create(body=message, from_=TWILIO_FROM, to=TARGET_PHONE)
			logging.info('SMS sent')
			return True
		except Exception as e:
			logging.error(f'Twilio send failed: {e}')
			print(message)
			return False
	else:
		logging.info('Twilio not configured or library missing, fallback to printing message')
		print(message)
		return False


def send_telegram(message: str) -> bool:
	global TELEGRAM_CHAT_ID
	if not TELEGRAM_BOT_TOKEN:
		logging.info('Telegram not configured (TELEGRAM_BOT_TOKEN missing)')
		return False
	# If chat id missing, try to auto-discover via getUpdates (user must have started the bot)
	if not TELEGRAM_CHAT_ID:
		logging.info('TELEGRAM_CHAT_ID not set — attempting to discover via getUpdates. Ensure you started the bot (press Start in the bot chat).')
		discovered = discover_chat_id_from_updates(TELEGRAM_BOT_TOKEN, TELEGRAM_USERNAME)
		if discovered:
			TELEGRAM_CHAT_ID = str(discovered)
			logging.info(f'Discovered TELEGRAM_CHAT_ID = {TELEGRAM_CHAT_ID}')
		else:
			logging.info('Unable to discover chat id via getUpdates')
			return False
	try:
		api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
		resp = requests.post(api, json={
			'chat_id': TELEGRAM_CHAT_ID,
			'text': message,
			'disable_notification': False,
		}, timeout=10)
		if resp.status_code == 200:
			logging.info('Telegram message sent')
			return True
		else:
			logging.error(f'Telegram send failed: {resp.status_code} {resp.text}')
			return False
	except Exception as e:
		logging.error(f'Failed to send Telegram message: {e}')
		return False


def discover_chat_id_from_updates(bot_token: str, username: str = None):
	"""Call getUpdates and try to find a chat id. If `username` provided, prefer that user's chat id."""
	try:
		api = f"https://api.telegram.org/bot{bot_token}/getUpdates"
		resp = requests.get(api, timeout=10)
		if resp.status_code != 200:
			logging.error(f'getUpdates failed: {resp.status_code} {resp.text}')
			return None
		data = resp.json()
		results = data.get('result', [])
		if not results:
			return None
		# search for matching username if provided
		for item in results:
			# messages
			msg = item.get('message') or item.get('edited_message') or item.get('channel_post')
			if not msg:
				continue
			chat = msg.get('chat')
			if not chat:
				continue
			# if username provided, match it
			if username:
				from_user = msg.get('from')
				if from_user and from_user.get('username') == username:
					return chat.get('id')
			else:
				return chat.get('id')
		# fallback: take first chat id found
		for item in results:
			msg = item.get('message') or item.get('edited_message') or item.get('channel_post')
			if msg and msg.get('chat'):
				return msg.get('chat').get('id')
	except Exception as e:
		logging.error(f'discover_chat_id_from_updates error: {e}')
	return None


def notify(message: str) -> bool:
	"""统一通知入口：优先 Telegram，其次 Twilio，其次打印到控制台。"""
	# Try Telegram first
	if send_telegram(message):
		return True
	# Fallback to SMS
	if send_sms(message):
		return True
	# Last resort: print
	logging.info('All notification methods failed or not configured — printed message')
	print(message)
	return False


def check_house(house: Dict[str, str]):
	name = house.get('name') or house.get('url')
	url = house.get('url')
	if not url:
		logging.warning(f"skip house without url: {house}")
		return name, []

	html = fetch_html(url)
	rooms = parse_rooms(html)

	# If no rooms found in static HTML, try rendering the page (Playwright) and parse again
	if not rooms:
		logging.info(f"{name}: no rooms found in initial HTML — attempting rendered fetch")
		rendered = fetch_rendered_html(url, wait_selector='tbody.rep_room')
		if rendered:
			rooms = parse_rooms(rendered)
			if rooms:
				logging.info(f"{name}: found {len(rooms)} rooms after rendering")
				html = rendered

	return name, rooms


def run_checks_all():
	logging.info('开始逐个检查 HOUSES')
	results = []
	for h in HOUSES:
		try:
			name, rooms = check_house(h)
			results.append((name, rooms))
		except Exception as e:
			logging.error(f"检查 {h.get('name')} 时报错: {e}")
			results.append((h.get('name') or h.get('url'), []))

	# Build a single aggregated message
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	lines = [f"{timestamp} 房源检测结果"]
	for name, rooms in results:
		lines.append(f"{name}")
		if rooms:
			for r in rooms:
				lines.append(f"部屋名: {r['name']} | 家賃: {r['rent']} {r['common']} | 間取り: {r['layout']} | 床面積: {r['area']} | 階数: {r['floor']}")
		else:
			lines.append("房屋信息:")

	message = '\n'.join(lines)
	notify(message)

	# Update seen_rooms state for de-dup tracking
	for name, rooms in results:
		seen = seen_rooms.setdefault(name, set())
		for r in rooms:
			seen.add(r.get('id') or r.get('name'))


def schedule_checks():
	if schedule is None:
		logging.error('schedule 库未安装，无法使用定时任务，请直接调用 run_checks_all 或安装 schedule')
		return
	schedule.clear()
	for t in CHECK_TIMES:
		try:
			schedule.every().day.at(t).do(run_checks_all)
			logging.info(f'scheduled daily check at {t}')
		except Exception as e:
			logging.error(f'invalid schedule time {t}: {e}')


if __name__ == '__main__':
	if not HOUSES:
		logging.error('请在脚本头部填写 HOUSES 列表，然后运行本脚本')
		exit(1)

	# 运行一次完整检查后退出 — 方便用系统计划任务（Task Scheduler）调用
	run_checks_all()
	logging.info('一次性检查完成，脚本退出（适用于由系统计划任务调用）')
	exit(0)

