from nonebot import get_plugin_config, logger, get_driver
from nonebot.plugin import PluginMetadata, on_message, on
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_ddbotatall",
    description="为DDBOT-WS适配的简易@全体插件，在@全体次数不够的情况下@SUPERUSER",
    usage="None",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)

atall = on_message(rule=lambda event: event.user_id ==
                   event.self_id, priority=1)
on_message_sent = on("message_sent", block=False)

config = get_driver().config
superusers = list(config.superusers)

atall_segment = MessageSegment.at('all')
atadmin_segment = MessageSegment.at(superusers[0])

live_text = "正在直播"
tmp = str(live_text)


@atall.handle()
@on_message_sent.handle()
async def atall_handler(bot: Bot, matcher: Matcher, event: Event):
    group_id = event.group_id
    text = str(event.raw_message)
    if tmp in text:
        try:
            logger.success(f"在群聊{group_id}中 尝试@全体")
            await bot.send(event, message=atall_segment)
        except Exception as e:
            await bot.send(event, message="@全体次数不足 "+atadmin_segment)
