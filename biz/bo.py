from pydantic import BaseModel

from db.models import VCustomer, VTrainer


class ChatContext:

    def __init__(self):
        self.conversation = {"Conversation": []}
        self.current_message = ""
        self.selected_row = [0]

    pass


class BoVcConfig(BaseModel):
    assistant_id: str = ''
    pass


class BoVCustomer:

    def __init__(self, vc: VCustomer = None):
        self.id = vc.id if vc is not None else -1
        self.cname = vc.cname if vc is not None else ''
        self.notes = vc.notes if vc is not None else ''
        self.config = self._deserialize(vc.config) if vc is not None else BoVcConfig()
        self.prompt = vc.prompt if vc is not None else ''
        self.putime = vc.putime if vc is not None else ''
        self.ctime = vc.ctime if vc is not None else ''
        self.active = vc.active if vc is not None else ''
        pass

    def to_dao(self) -> VCustomer:
        config = self._serialize(self.config)
        return VCustomer(id=self.id, cname=self.cname, notes=self.notes, config=config, prompt=self.prompt,
                         putime=self.putime, ctime=self.ctime, active=self.active)

    @staticmethod
    def _deserialize(config: str | None) -> BoVcConfig:
        if config is None or config == '':
            return BoVcConfig()

        bo_vc_config = None
        try:
            bo_vc_config = BoVcConfig.model_validate_json(config)
        finally:
            if bo_vc_config is None:
                bo_vc_config = BoVcConfig()
        return bo_vc_config

    @staticmethod
    def _serialize(config: BoVcConfig) -> str:
        return config.model_dump_json(indent=4)

    pass


class BoVtConfig(BaseModel):
    assistant_id: str = ''
    pass


class BoVTrainer:

    def __init__(self, vt: VTrainer = None):
        self.id = vt.id if vt is not None else -1
        self.tname = vt.tname if vt is not None else ''
        self.notes = vt.notes if vt is not None else ''
        self.config = self._deserialize(vt.config) if vt is not None else BoVcConfig()
        self.prompt = vt.prompt if vt is not None else ''
        self.putime = vt.putime if vt is not None else ''
        self.ctime = vt.ctime if vt is not None else ''
        self.active = vt.active if vt is not None else ''
        pass

    def to_dao(self) -> VTrainer:
        config = self._serialize(self.config)
        return VTrainer(id=self.id, tname=self.tname, notes=self.notes, config=config, prompt=self.prompt,
                        putime=self.putime, ctime=self.ctime, active=self.active)

    @staticmethod
    def _deserialize(config: str | None) -> BoVtConfig:
        if config is None or config == '':
            return BoVtConfig()

        bo_vt_config = None
        try:
            bo_vt_config = BoVcConfig.model_validate_json(config)
        finally:
            if bo_vt_config is None:
                bo_vt_config = BoVtConfig()
        return bo_vt_config

    @staticmethod
    def _serialize(config: BoVtConfig) -> str:
        return config.model_dump_json(indent=4)

    pass
