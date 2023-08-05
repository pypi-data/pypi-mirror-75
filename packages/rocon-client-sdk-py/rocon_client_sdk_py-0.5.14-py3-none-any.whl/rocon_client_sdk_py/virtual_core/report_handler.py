import pydash


def get_args(inst):
    return pydash.get(inst, 'action.args')


def get_target_arg(args, target_key):
    return pydash.find(args, lambda arg: pydash.get(arg, 'key') == target_key)


def get_target_inst_by_func(instructions, func_name):
    return pydash.filter_(instructions, lambda inst: inst['action']['func_name'] == func_name)


def get_next_inst(instructions, base_inst):
    return pydash.find(instructions, {'id': base_inst['next']})


def get_instruction_by_resource_id(instructions, resource_id):
    def cb(inst):
        args = get_args(inst)
        resource_id_arg = get_target_arg(args, 'resource_id')
        return resource_id_arg['value'] == resource_id

    return pydash.find(instructions, cb)


def get_success_result(results):
    return pydash.filter_(results, lambda result: result['status'] == 'DONE_SUCCESS')


def get_use_resource_inst(report, target_resource):
    target_resource_id = pydash.get(target_resource, 'id')
    use_resource_instructions = get_target_inst_by_func(pydash.get(report, 'instructions'), 'use_resource')
    use_resource_ids = []
    for instruction in use_resource_instructions:
        use_resource_ids.append(instruction['id'])

    success_results = get_success_result(pydash.get(report, ['result', 'returns']))
    success_ids = []
    for result in success_results:
        success_ids.append(result['id'])

    target_ids = pydash.difference(use_resource_ids, success_ids)
    target_instructions = []
    for target_id in target_ids:
        target_instructions.append(pydash.find(use_resource_instructions, {'id': target_id}))

    return get_instruction_by_resource_id(target_instructions, target_resource_id)


def get_enter_exit_aligns(report, target_resource):
    use_resource_inst = get_use_resource_inst(report, target_resource)
    args = pydash.get(use_resource_inst, 'action.args')
    resource_inst = pydash.find(args, lambda arg: arg['key'] == 'resource_id')

    aligns = pydash.find(pydash.get(resource_inst, 'properties'), lambda property: property['key'] == 'align')

    enter = pydash.get(aligns['value'], 'enter')
    exit = pydash.get(aligns['value'], 'exit')
    return {'enter': enter, 'exit': exit}


def get_next_move_inst(report, target_inst):
    current_inst = target_inst
    move_inst = None
    while current_inst['next']:
        next_inst = get_next_inst(pydash.get(report, 'instructions'), target_inst)
        if next_inst['action']['func_name'] == 'move':
            move_inst = next_inst
            break

        current_inst = next_inst

    return move_inst