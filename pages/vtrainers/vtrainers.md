<|{vo_create_show}|dialog|title=�½�AI��ѵʦ|width=30%|labels=ȡ��;�½�|on_action=action_create

<|{vo_tname}|input|label=����|class_name=fullwidth|>

<|{vo_notes}|input|label=����|class_name=fullwidth|>
|>

<|{vo_confirm_show}|dialog|title=ȷ��������ϰ|width=30%|labels=ȡ��;ȷ��|on_action=action_renew_chat
#### **��ȷ��������������¼�����¿�ʼ��ϰ��**{: .h6}
|>

<|2 9|layout|
<sidebar|sidebar|
<|{vo_bvt}|selector|lov={vo_bvts}|type=BoVTrainer|adapter={lambda v: (str(v.id), v.tname)}|on_change=action_select|>
<|�½� +|button|on_action=action_open_create_dialog|class_name=fullwidth plain|>
|sidebar>

<|part|render=True|class_name=align-item-bottom table|
<|{vo_conversation}|table|style=style_conv|show_all|width=100%|selected={vo_selected_row}|rebuild|>
<|part|class_name=card mt1|
<|9 1|layout|
<|{vo_current_message}|input|active={vo_current_message_active}|label=��������|multiline=True|lines_shown=2|on_action=action_send_message|on_change=message_changed|class_name=fullwidth message_input|>

<|{vo_icon_history}|button|hover_text=���������¼|on_action=action_copy_conversation|>
|>
|>
|>
|>

<|{vo_detail_show}|pane|anchor=right|width=800px|
<|container container-bg|

#### **���Ա༭**{: .color-primary .h5}

<|1 1|layout|gap=1rem|class_name=m-half|
<|{vo_bvt.tname}|input|label=����|class_name=fullwidth|>

<|{vo_bvt.notes}|input|label=����||class_name=fullwidth|>
|>

#### **���ñ༭**{: .color-primary .h5}

<|1|layout|class_name=m-half|
<|{vo_bvt.config.assistant_id}|input|label=AssistantID|active=False|class_name=fullwidth|>
|>

<|1|layout|class_name=m-half|
<|{vo_instructions}|input|label=˵��|multiline=True|lines_shown=10|class_name=fullwidth|>
|>

<|����|button|on_action=action_update|class_name=plain|>
<|������ϰ|button|on_action=action_open_confirm_dialog|>
|>
|>
