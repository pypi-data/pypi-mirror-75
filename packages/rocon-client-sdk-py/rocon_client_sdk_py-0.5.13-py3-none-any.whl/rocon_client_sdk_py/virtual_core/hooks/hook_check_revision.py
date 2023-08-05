import pydash
from rocon_client_sdk_py.virtual_core.components.button_requests import ButtonRequests
from rocon_client_sdk_py.core_logic.hook_origin_check_revision import HookOriginCheckRevision
from rocon_client_sdk_py.core_logic.context import Context


class HookCheckRevision(HookOriginCheckRevision):

    async def on_handle(self, report):

        br = ButtonRequests(self.context)
        proposed_instructions = pydash.get(report, 'revision.propositions.instructions')
        if proposed_instructions is None:
            return True

        diff_insts = pydash.difference_with(proposed_instructions, report['instructions'], pydash.is_equal)
        self.context.rocon_logger.debug('calculate diff of instructions : update:{}, origin:{}, diff:{}'.format(proposed_instructions, report['instructions'], diff_insts))

        for inst in diff_insts:
            def cb(result, value):
                result[value['key']] = value
                return result

            args = pydash.reduce_(inst['action']['args'], cb)
            if inst['action']['func_name'] == 'wait':
                if args['param']['value'] == 'success':
                    # wait가 정상적으로 해제 될때,

                    request = br.find_request_by_button_id('signal', self.context.worker.uuid)
                    if request:
                        await self.context.api_report.approve_revision(report)

                        # 등록된 buttonRequest의 waiting을 푼다.(Rx의해
                        br.process(request, 'success')
                    else:
                        self.rocon_logger.debug('found revision to finish wait(signal) but there is no button request for it')
                else:
                    self.rocon_logger.debug('condition is not match on wait')
            else:
                self.rocon_logger.debug('cannot handle revision of instruction : {}'.format(inst))

        return True