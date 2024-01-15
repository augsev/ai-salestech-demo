import time

from openai.types.beta import Assistant, Thread
from taipy.gui import Markdown, notify, download

from biz.bo import ChatContext, BoVTrainer
from biz.vtrainer import list_all, add, update
from db.models import VTrainer
from utils.utils import openai_client

client = openai_client()

assistants_cache: dict[str: Assistant] = {}
threads_cache: dict[str: Thread] = {}
chat_ctx_cache: dict[str: ChatContext] = {}


def load() -> list[BoVTrainer]:
    bvts: list[BoVTrainer] = []
    vts: list[VTrainer] = list_all()
    for vt in vts:
        bvt = BoVTrainer(vt)
        bvts.append(bvt)
        pass
    return bvts


def reload(state):
    state.vo_bvts = load()
    pass


def get_cached_chat_context(assistant_id: str) -> ChatContext:
    chat_ctx = chat_ctx_cache.get(assistant_id)
    if chat_ctx is None:
        chat_ctx = ChatContext()
        chat_ctx_cache[assistant_id] = chat_ctx
        pass
    return chat_ctx


def renew_cached_chat_context(assistant_id: str) -> ChatContext:
    chat_ctx = ChatContext()
    chat_ctx_cache[assistant_id] = chat_ctx
    return chat_ctx


def get_cached_thread(assistant_id: str) -> Thread:
    thread = threads_cache.get(assistant_id)
    if thread is None:
        thread = client.beta.threads.create()
        threads_cache[assistant_id] = thread
        pass
    return thread


def renew_cached_thread(assistant_id: str) -> Thread:
    thread = client.beta.threads.create()
    threads_cache[assistant_id] = thread
    return thread


def create_or_update_cached_assistant(name: str, instructions: str = '', assistant_id: str = '') -> Assistant:
    assistant = client.beta.assistants.create(
        name="AIT-%s" % name,
        instructions=instructions,
        tools=[],
        model="gpt-3.5-turbo-1106"
    ) if (assistant_id is None or assistant_id == '') else client.beta.assistants.update(
        assistant_id=assistant_id,
        name="AIT-%s" % name,
        instructions=instructions
    )
    assistants_cache[assistant.id] = assistant
    return assistant


def get_cached_assistant(assistant_id: str) -> Assistant:
    assistant = assistants_cache.get(assistant_id)

    if assistant is None:
        assistant = client.beta.assistants.retrieve(assistant_id)
        assistants_cache[assistant.id] = assistant
        pass

    return assistant


# for vtrainer selector
vo_bvt = BoVTrainer()
vo_bvts = load()

# for create dialog
vo_create_show = False
vo_tname = ''
vo_notes = ''


def action_open_create_dialog(state):
    state.vo_create_show = True
    pass


def action_create(state, id, payload):
    idx = payload["args"][0]

    if idx == 1:
        bvt = BoVTrainer(VTrainer(tname=state.vo_tname, notes=state.vo_notes))
        assistant = create_or_update_cached_assistant(bvt.tname)
        bvt.config.assistant_id = assistant.id
        add(bvt.to_dao())

        reload(state)
        pass

    state.vo_create_show = False
    state.vo_tname = ''
    state.vo_notes = ''
    pass


# for vtrainer details pane
vo_detail_show = False
vo_instructions = ''


def action_select(state, var_name, value):
    state.vo_bvt = value
    state.vo_detail_show = True

    bvt: BoVTrainer = state.vo_bvt
    assistant_id = bvt.config.assistant_id

    if assistant_id == '' or assistant_id is None:
        state.vo_instructions = ''
        state.vo_current_message_active = False
        pass
    else:
        assistant = get_cached_assistant(assistant_id)
        state.vo_instructions = assistant.instructions

        get_cached_thread(assistant_id)
        state.vo_current_message_active = True
        pass

    # initial environment for chat
    switch_chat_context(state)
    pass


def action_update(state):
    bvt: BoVTrainer = state.vo_bvt
    assistant = create_or_update_cached_assistant(bvt.tname, state.vo_instructions, bvt.config.assistant_id)
    bvt.config.assistant_id = assistant.id

    update(bvt.to_dao())

    state.vo_detail_show = False
    reload(state)
    pass


# for chat part
vo_confirm_show = False
vo_current_message_active = True
vo_conversation = {"Conversation": []}
vo_current_message = ''
vo_selected_row = [0]


def switch_chat_context(state):
    bvt: BoVTrainer = state.vo_bvt
    assistant_id = bvt.config.assistant_id
    ctx = get_cached_chat_context(assistant_id)
    state.vo_conversation = ctx.conversation
    state.vo_current_message = ctx.current_message
    state.vo_selected_row = ctx.selected_row
    pass


def action_open_confirm_dialog(state):
    state.vo_confirm_show = True
    pass


def action_renew_chat(state, id, payload):
    idx = payload["args"][0]
    detail_show = True
    try:
        if idx == 1:
            bvt: BoVTrainer = state.vo_bvt
            assistant_id = bvt.config.assistant_id

            if assistant_id == '' or assistant_id is None:
                notify(state, "error", "此AI培训师未填写说明，如想对话请先填写说明并保存！")
                return

            renew_cached_thread(assistant_id)
            ctx = renew_cached_chat_context(assistant_id)
            state.vo_conversation = ctx.conversation
            state.vo_current_message = ctx.current_message
            state.vo_selected_row = ctx.selected_row
            detail_show = False
            pass
    finally:
        state.vo_confirm_show = False
        state.vo_detail_show = detail_show
        pass
    pass


def message_changed(state):
    bvt: BoVTrainer = state.vo_bvt
    assistant_id = bvt.config.assistant_id
    if assistant_id == '':
        return

    chat_ctx = get_cached_chat_context(assistant_id)
    chat_ctx.current_message = '' if state.vo_current_message is None else state.vo_current_message
    pass


def action_send_message(state):
    current_message = state.vo_current_message
    if current_message == '':
        notify(state, "error", "请输入对话内容！")
        return

    if current_message is None:
        notify(state, "error", "您输入太快，请慢一点！")
        return

    bvt: BoVTrainer = state.vo_bvt
    assistant_id = bvt.config.assistant_id

    if assistant_id == '' or assistant_id is None:
        notify(state, "error", "此AI培训师未填写说明，如想对话请先填写说明并保存！")
        return

    thread = get_cached_thread(assistant_id)
    thread_id = thread.id

    chat_ctx = get_cached_chat_context(assistant_id)
    try:
        state.vo_conversation = {"Conversation": chat_ctx.conversation["Conversation"].copy()}
        state.vo_conversation["Conversation"] += ["学员： %s" % current_message]
        state.vo_current_message = ''
        state.vo_selected_row = [len(state.vo_conversation["Conversation"]) - 1]
        state.vo_current_message_active = False
        notify(state, "info", "已发出，等待AI培训师回复。")

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=current_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            new_run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if new_run.status == "completed":
                break
            time.sleep(1)
            run = new_run
            pass

        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        response_message = messages.data[0].content[0].text.value

        chat_ctx.conversation["Conversation"] += ["学员： %s" % current_message, "培训师： %s" % response_message]
        chat_ctx.current_message = ''
        chat_ctx.selected_row = [len(chat_ctx.conversation["Conversation"]) - 1]
        state.vo_conversation = chat_ctx.conversation
        state.vo_current_message = chat_ctx.current_message
        state.vo_selected_row = chat_ctx.selected_row

        notify(state, "success", "AI培训师已回复")
    except Exception as ex:
        state.vo_conversation = chat_ctx.conversation
        state.vo_current_message = current_message
        state.vo_selected_row = [len(chat_ctx.conversation["Conversation"]) - 1]
        notify(state, "error", f"发生错误: {ex}")
        print(ex)
    finally:
        state.vo_current_message_active = True
        pass
    pass


def action_download_history(state):
    bvt: BoVTrainer = state.vo_bvt
    assistant_id = bvt.config.assistant_id
    chat_ctx = get_cached_chat_context(assistant_id)

    history = "\n\n".join(chat_ctx.conversation["Conversation"])
    download(state, content=bytes(history, "UTF-8"), name="%s.txt" % bvt.tname)
    pass


def style_conv(state, idx: int, row: int):
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"


vtrainers_md = Markdown("pages/vtrainers/vtrainers.md")
