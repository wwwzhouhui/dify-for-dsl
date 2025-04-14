class LLMResponseValidationError(Exception):
    """LLM 响应验证错误"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
