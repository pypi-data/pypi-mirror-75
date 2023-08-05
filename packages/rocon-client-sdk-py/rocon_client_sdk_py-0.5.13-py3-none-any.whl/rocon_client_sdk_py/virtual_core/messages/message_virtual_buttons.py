from rocon_client_sdk_py.core_logic.message import Message
from rocon_client_sdk_py.virtual_core.components.button_requests import ButtonRequests


class VirtualButtons(Message):
    def __init__(self):
        super().__init__()
        self.name = 'virtualButtons'

    async def on_handle(self, message_body):
        self.rocon_logger.debug('have got virtualButtons message: {}'.format(message_body))
        button_requests = ButtonRequests(self.context)

        if button_requests.process_request_by_button(message_body, self.context.worker.uuid, message_body) is None:
            if message_body == 'O':
                self.rocon_logger.debug('"O" button called!!')
                request = button_requests.find_request_by_button_id('human_input', self.context.worker.uuid)
                if request and request['button'] == message_body:
                    # 등록된 buttonRequest의 waiting을 푼다.(Rx의해
                    button_requests.process(request, 'success')
                else:
                    self.rocon_logger.debug('"O" button request not found')

            elif message_body == 'X':
                self.rocon_logger.debug('"X" button called!!')
                request = button_requests.find_request_by_button_id('human_input', self.context.worker.uuid)
                if request and request['button'] == message_body:
                    # 등록된 buttonRequest의 waiting을 푼다.(Rx의해
                    button_requests.process(request, 'success')
                else:
                    self.rocon_logger.debug('"X" button request not found')

            elif message_body == 'E_PUSH':
                self.rocon_logger.debug('emergency called!!')
                request = button_requests.find_request_by_button_id('human_input', self.context.worker.uuid)
                if request and request['button'] == message_body:
                    # 등록된 buttonRequest의 waiting을 푼다.(Rx의해
                    button_requests.process(request, 'success')
                else:
                    self.rocon_logger.debug('"E_PUSH" button request not found')
            else:
                self.rocon_logger.debug('not defined button called!! it is not implemented yet.')

        return True