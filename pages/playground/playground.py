from taipy.gui import Markdown, notify, download

from biz.bot import list_all, add, update
from db.models import Bot
from utils.utils import zhipuai_client

client = zhipuai_client()


class ChatContext:

    def __init__(self):
        self.history = []
        self.conversation = {"Conversation": []}
        self.current_message = ""
        self.selected_row = [0]

    pass


chat_ctx_cache: dict[str: ChatContext] = {}


def get_cached_chat_context(id: str) -> ChatContext:
    chat_ctx = chat_ctx_cache.get(id)
    if chat_ctx is None:
        chat_ctx = ChatContext()
        chat_ctx_cache[id] = chat_ctx
        pass
    return chat_ctx


def load() -> list[Bot]:
    return list_all()


def reload(state):
    state.vo_bots = load()
    pass


# for bot selector
vo_bots = load()

# for create dialog
vo_create_show = False
vo_name = ''
vo_prompts = ''
vo_notes = ''


def action_open_create_dialog(state):
    state.vo_create_show = True
    pass


def action_create(state, id, payload):
    idx = payload["args"][0]

    if idx == 1:
        bot = Bot(name=state.vo_name, prompts="", notes=state.vo_notes)
        add(bot)

        reload(state)
        pass

    state.vo_create_show = False
    state.vo_cname = ''
    state.vo_notes = ''
    pass


def action_reload_selection(state):
    reload(state)
    state.vo_current_message_active = False
    pass


# for bot details pane


vo_detail_show = False
vo_bot = Bot()


def action_select(state, var_name, value):
    new_bot = Bot()
    new_bot.id = value.id
    new_bot.name = value.name
    new_bot.prompts = value.prompts
    new_bot.notes = value.notes
    state.vo_bot = new_bot

    chat_ctx = get_cached_chat_context(str(state.vo_bot.id))
    state.history = chat_ctx.history
    state.vo_conversation = chat_ctx.conversation
    state.vo_current_message = chat_ctx.current_message
    state.vo_selected_row = chat_ctx.selected_row

    state.vo_current_message_active = True
    state.vo_detail_show = True
    pass


def action_update(state):
    update(state.vo_bot)

    state.vo_detail_show = False
    reload(state)
    pass


# for chat part
vo_confirm_show = False
vo_current_message_active = False
history = []
vo_conversation = {"Conversation": []}
vo_current_message = ''
vo_selected_row = [0]


def action_open_confirm_dialog(state):
    state.vo_confirm_show = True
    pass


def action_renew_chat(state, id, payload):
    idx = payload["args"][0]
    detail_show = True
    try:
        if idx == 1:
            new_chat_ctx = ChatContext()
            chat_ctx_cache[str(state.vo_bot.id)] = new_chat_ctx
            state.history = new_chat_ctx.history
            state.vo_conversation = new_chat_ctx.conversation
            state.vo_current_message = new_chat_ctx.current_message
            state.vo_selected_row = new_chat_ctx.selected_row

            detail_show = False
            pass
    finally:
        state.vo_confirm_show = False
        state.vo_detail_show = detail_show
        pass
    pass


def action_send_message(state):
    current_message = state.vo_current_message
    if current_message == '':
        notify(state, "error", "请输入对话内容！")
        return

    if current_message is None:
        notify(state, "error", "您输入太快，请慢一点！")
        return

    conversation_copy = state.vo_conversation["Conversation"].copy()
    try:
        state.vo_conversation["Conversation"] += ["你： %s" % current_message]
        state.vo_current_message = ''
        state.vo_selected_row = [len(state.vo_conversation["Conversation"]) - 1]
        state.vo_current_message_active = False
        notify(state, "info", "已发出，等待AI机器人回复。")

        bot: Bot = state.vo_bot

        messages = [{"role": "system", "content": bot.prompts}]
        for history_msg in state.history:
            messages.append({"role": history_msg["role"], "content": history_msg["content"]})
            pass
        messages.append({"role": "user", "content": current_message})

        response = client.chat.completions.create(
            model="glm-3-turbo",
            messages=messages
        )
        response_message = response.choices[0].message.content

        state.history.append({"role": "user", "content": current_message})
        state.history.append({"role": "assistant", "content": response_message})
        state.vo_conversation["Conversation"] += ["机器人： %s" % response_message]
        state.vo_current_message = ""
        state.vo_selected_row = [len(state.vo_conversation["Conversation"]) - 1]

        notify(state, "success", "AI机器人已回复")
    except Exception as ex:
        state.vo_conversation = {"Conversation": conversation_copy}
        state.vo_current_message = current_message
        state.vo_selected_row = [len(state.vo_conversation["Conversation"]) - 1]
        notify(state, "error", f"发生错误: {ex}")
        print(ex)
    finally:
        state.vo_current_message_active = True
        pass
    pass


def action_download_history(state):
    conversations = "\n\n".join(state.vo_conversation["Conversation"])
    download(state, content=bytes(conversations, "UTF-8"), name="%s.txt" % state.vo_bot.name)
    pass


def style_conv(state, idx: int, row: int):
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"


playground_md = Markdown("pages/playground/playground.md")
