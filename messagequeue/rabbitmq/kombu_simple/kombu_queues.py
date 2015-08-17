from kombu import Exchange, Queue

task_exchange = Exchange('task_exchange', type='direct')
task_json_queue = Queue('task_json_queue', task_exchange,
                        routing_key='json_queue')
task_pickle_queue = Queue('task_pickle_queue', task_exchange,
                          routing_key='pickle_queue')
