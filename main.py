from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as comp
from astrbot.api import logger
from random import randint, choice, random, sample, shuffle, seed
from datetime import datetime
import math
import os

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PLUGIN_DIR, "assets")

seed(datetime.now().timestamp())
frys = ["香菇","菠菜","蒜苗","胡萝卜","空心菜","地瓜叶","花菜","茄子","南瓜","鸡蛋(韭菜炒鸡蛋，西红柿炒鸡蛋)", "土豆丝", "四季豆"]
example_foods = ["早饭", "中饭", "晚饭"]
# 西式快餐
meals_western_fastfood = ["KFC", "麦当劳", "披萨"]

# 中式快餐/简餐
meals_chinese_fastfood = [
    "沙县小吃",
    "自选菜（比如老乡鸡）",
    "一饭一菜套餐",
    "卤肉饭",
    "猪脚饭",
    "牛肉饭",
    "咖喱饭",
    "鸡公煲",
    "酸菜鱼",
    "盖浇饭"
]

# 粉面/主食类
meals_main = [
    "兰州拉面",
    "乌冬面",
    "炒面",
    "炒米粉",
    "米粉",
    "土豆粉",
    "拌粉",
    "江西小炒",
    "炒饭",
    "炒饼"
]

# 小吃/点心类
meals_snacks = ["生煎包", "饺子", "烧麦", "肠粉", "馍馍", "杨枝甘露"]

# 汤锅/麻辣类
meals_spicy = ["火锅", "麻辣烫", "冒菜", "钵钵鸡", "干锅", "烤肉", ""]

# 即食/速食
meals_instant = ["泡面(还是吃点健康的吧)"]

mkkr = ["真九"]

meals = meals_western_fastfood + meals_chinese_fastfood + meals_main + meals_snacks + meals_spicy + meals_instant
meals_41 = meals + mkkr

human_templates = [
    # 今天尝尝 + 后缀
    "今天尝尝{}吧", "今天尝尝{}怎么样？", "今天尝尝{}？", "今天尝尝{}！",

    # 这一顿试试 + 后缀
    "这一顿试试{}吧", "这一顿试试{}怎么样？",  "这一顿试试{}？", "这一顿试试{}！",

    # 试试 + 后缀
    "试试{}吧","试试{}怎么样？","试试{}？","试试{}！",

    # 了解一下 + 后缀
    "了解一下{}吧","了解一下{}怎么样？","了解一下{}？","了解一下{}！",

    # 吃点 + 后缀
    "吃点{}吧","吃点{}怎么样？","吃点{}？","吃点{}！",

    # 来点 + 后缀
    "来点{}吧","来点{}怎么样？","来点{}？","来点{}！",

    # 吃吃 + 后缀
    "吃吃{}吧","吃吃{}怎么样？","吃吃{}？","吃吃{}！",

    # 空前缀 + 所有后缀
    "{}吧","{}怎么样？","{}？","{}尝尝","{}吃吃！","{}！",

    # 额外添加的常用表达
    "不妨试试{}吧","不妨试试{}怎么样？","推荐你{}尝尝","一定要试{}！",
]
kfc_not_human = ["友情提醒，今天是星期四", "KFC Crazy Thursday", ":(\n\n在调用插件的处理函数 meal 时出现异常：KFC Crazy Thursday need ￥50", "前面忘了，后面忘了，最后今天疯狂星期四"]
human_length = len(human_templates)
kfc_length = len(kfc_not_human)
total_length = human_length + kfc_length
img_path = ["开始炒.jpg", "炒好了.jpg"]
start_time = datetime.now()
# mkkr_img = [
#     "20250614_010412",
#     "20250614_225500",
#     "20250616_232242",
#     "20250618_182053",
#     "20250618_182719",
#     "20250619_213036",
#     "20250619_213405",
#     "20250623_160533",
#     "20250624_112213",
#     "20250624_112229",
#     "20250627_014120",
#     "20250627_211407",
#     "20250627_211657",
#     "20250628_014721",
#     "20250628_014810",
#     "20250628_201234",
#     "20250629_002845",
#     "20250629_204200",
#     "20250629_204413",
#     "20250629_211111",
#     "20250629_212853",
#     "20250701_165130",
#     "20250908_175743",
#     "20250930_022013",
#     "20251004_111454",
#     "20251018_200818",
#     "20251111_091547",
#     "20251122_180745",
#     "20251122_180756",
#     "20251128_231826",
#     "20251128_231856",
#     "20251202_143057",
#     "20251218_154002",
#     "20251221_005740",
#     "20251225_041339",
#     "20251226_011300",
#     "20251231_033937",
# ]
qq_id = {}

def RandomAnything(options: list):
    """从选项列表中随机选择一个选项"""
    if not options:
        return None
    return choice(options)

@register("meal", "spica", "一个简单的 是啊，吃什么 插件", "0.5.0")
class RandMeal(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # async def initialize(self):
    #     """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 meal。注册成功后，发送 `/meal` 就会触发这个指令，并回复一个随机的吃什么建议。alias 参数可以设置指令的别名，用户发送别名也会触发这个指令。
    @filter.command("meal", alias={'吃什么', '吃什麽'})
    async def random_meal(self, event: AstrMessageEvent, msg_arg: str=""):
        """这是一个 是啊，吃什么 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        # user_name = event.get_sender_name()
        # message_str = event.message_str # 用户发的纯文本消息字符串
        session_id = event.message_obj.session_id
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        nowtime = datetime.now()

        if msg_arg == "菜单":
            yield event.plain_result("菜单功能开发中！")
        elif msg_arg == "":
            if nowtime.weekday() == 3 and random() < 0.4: # 疯狂星期四 kfc概率0.4
                if random() <= 0.5:
                    meal = meals_41[0]
                    sentense = choice(human_templates).format(meal)
                else:
                    sentense = choice(kfc_not_human)
                logger.info(f"随机菜[疯狂星期四] -> {sentense}")
            # elif nowtime.month == 4 and nowtime.day == 1 and random() < 0.5 and session_id in {"1061360382", "877173610"}: # 愚人节，随机返回一个菜或mkkr
            #     meal = "真九"
            #     sentense = choice(human_templates).format(meal)
            #     chain = [
            #         comp.Plain(sentense),           # 真九 \n [图片]
            #         comp.Image.fromFileSystem(os.path.join(ASSETS_DIR, f"{mkkr_img[randint(0, len(mkkr_img)-1)]}.jpg"))
            #     ]
            #     yield event.chain_result(chain)
            #     return

            else:
                meal = meals_41[randint(0,len(meals_41)-1)]
                sentense = choice(human_templates).format(meal)
                logger.info(f"随机菜 -> {meal}：{sentense}")
            yield event.plain_result(sentense) # 发送一条纯文本消息
            # yield event.plain_result(str(msg_arg=="")) # 发送一条纯文本消息
        elif msg_arg == "帮助" or msg_arg == "help":
            yield event.plain_result("功能一览\n输入 /吃什么 触发主功能\n输入 /吃什么 菜单 还没开发好的菜单\n输入 /吃什么 帮助 查看帮助文档")
        else:
            yield event.plain_result("没有这个参数哦\n输入参数help可以查看帮助")

    @filter.command("fry", alias={'炒什么'})
    async def fry(self, event: AstrMessageEvent, n="1"):
        """这是一个 是啊，炒什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        try:
            n = int(n)
        except ValueError:
            yield event.plain_result("请输入一个整数哦")
            return
        if int(n) > 10:
            yield event.plain_result("菜炒的太多会吃不完哦~\n建议炒10份以下的菜")
            return
        elif int(n) <= 0:
            yield event.plain_result("你到底炒不炒😠")
            return
        wait_for_fry = sample(frys, k=int(n))
        str = f"炒{wait_for_fry[0]}"
        for fryed in wait_for_fry[1:]:
            str += f"，炒{fryed}"
        chain = [
            comp.Plain(str),           # 炒xx \n [图片]
            comp.Image.fromFileSystem(os.path.join(ASSETS_DIR, img_path[randint(0, len(img_path)-1)]))
        ]
        yield event.chain_result(chain)

    @filter.command("choice", alias={'选什么'})
    async def choice(self, event: AstrMessageEvent, option1: str, option2: str, n: int=1000):
        """这是一个 是啊，选什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        options = [option1, option2]
        if n > 10000000:
            yield event.plain_result("根据大数定理，再往上增加次数会很大概率会出现50\\% 50\\%")
            return
        n1 = 0
        n2 = 0

        for i in range(n): 
            choice_result = choice(options)
            if choice_result == option1:
                n1 += 1
            elif choice_result == option2:
                n2 += 1
            else:
                n3 += 1
        result = f"{option1}\n{int((math.ceil(n1/n*100)-30)*1.34) * '·'}\n{n1/n*100:.4f}%\n\n{option2}\n{int((math.ceil(n2/n*100)-30)*1.34) * '·'}\n{n2/n*100:.4f}%\n\n共进行了{n}次选择"
        
        yield event.plain_result(f"{result}")

    @filter.command("mkkr", alias={'我要看pa饭二期'})
    async def mkkr(self, event: AstrMessageEvent):
        """这是一个 pa饭二期 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        chain = [
            comp.Plain("这是一个自动生成pa饭二期的工具"),
            comp.Image.fromFileSystem(os.path.join(ASSETS_DIR, "诈骗.png"))
        ]
        yield event.chain_result(chain)
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("test")
    async def test(self, event: AstrMessageEvent, options: str=""):
        """这是一个测试函数。"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        sender = event.message_obj.sender.user_id
        group_id = event.message_obj.group_id
        self_id = event.message_obj.self_id
        session_id = event.message_obj.session_id
        message_id = event.message_obj.message_id
        message_str = event.message_str # 用户发的纯文本消息字符串
        nowtime = datetime.now()
        if options == "all":
            yield event.plain_result(f"以下是启动后所有QQID与交互次数的列表：\n{qq_id}")
        elif options == "echo":
            if session_id == "1061360382":
                yield event.plain_result("对了？")
            else:
                yield event.plain_result("有点奇怪")
        else:
            if sender in qq_id:
                qq_id[sender] += 1
                index = qq_id[sender] - 1
                if index >= len(meals_41):
                    yield event.plain_result("还决定不下来？出门右手边能吃的第二家饭店请")
                    return
                random_seed = sender + nowtime.strftime("%Y%m%d") + nowtime.strftime("%H") # 同一个人在同一天同一小时调用测试函数，随机数相同，保证每个人每小时的结果不变
                seed(random_seed) # 同一个人在同一天调用测试函数，随机数相同，保证每个人每天的结果不变
                shuffle(meals_41) # 打乱列表顺序，保证每次调用结果不同
                # yield event.plain_result(f"发送人:{sender}\n席德:{random_seed}\n当前序列:{index}/{len(meals)}\n{meals[index]}") # 发送一条纯文本消息
                # yield event.plain_result(f"{meals[qq_id[sender]-1]}")
                yield event.plain_result(f"sender: {sender}\n你已经调用过这个测试函数了哦\n调用次数：{qq_id[sender]}\n\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")
            else:
                qq_id.update({sender: 1})
                random_seed = sender + nowtime.strftime("%Y%m%d") + nowtime.strftime("%H") # 同一个人在同一天同一小时调用测试函数，随机数相同，保证每个人每小时的结果不变
                seed(random_seed) # 同一个人在同一天调用测试函数，随机数相同，保证每个人每天的结果不变
                shuffle(meals_41) # 打乱列表顺序，保证每次调用结果不同
                # yield event.plain_result(f"{meals[0]}")
                # yield event.plain_result(f"发送人:{sender}\n席德:{random_seed}\n当前序列:0/{len(meals)}\n{meals[0]}") # 发送一条纯文本消息
                yield event.plain_result(f"sender: {sender}\n这是你今天第一次调用这个测试函数哦\n调用次数：1\n\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")
            # yield event.plain_result(f"sender: {sender}\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")

    @filter.command("testo")
    async def testo(self, event: AstrMessageEvent, *options: str):
        """测试可变参数数量的函数。"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.chain_result([comp.Plain(opt) for opt in options])

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        nowtime = datetime.now()
        with open(os.path.join(PLUGIN_DIR, "qq_id.txt"), "a", encoding="utf-8") as f:
            f.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} ~ {nowtime.strftime('%Y-%m-%d %H:%M:%S')} {str(qq_id)}\n")
