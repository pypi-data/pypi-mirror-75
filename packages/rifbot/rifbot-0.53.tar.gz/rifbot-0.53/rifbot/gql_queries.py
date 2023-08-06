JOB_FIELDS = '''
    id
    type
    status
    createdTs
    startedTs
    endedTs
    args
    executor {
        id
        name
        host
        hostName
        port
        processName
        localIp
        publicIp
        features {
          name
          data
        }
        summary
    }  
'''

QUERIES = {
    'PING': '''
        query {
            ping
        }
        ''',

    'FIND_ONE_STRATEGY_RESULT':
        '''
        query ($runId: String!){
            findOneStrategyResult(runId: $runId) {
                strategyStats
                monteCarlo
            }
        }
        '''
}

MUTATIONS = {
    'ENQUEUE_STRATEGY_RUN':
        '''
        mutation($rootOptions: RootOptionsInput!, $runId: String) {
            enqueueStrategyRun(rootOptions: $rootOptions, runId: $runId) {
                ''' + JOB_FIELDS + '''
            }
        }
    '''
}

SUBSCRIPTIONS = {
    'PING':
        '''
            subscription {
                ping
            }
        ''',
    'ON_JOB_STARTED':
        '''
        subscription ($jobId: String){
             onJobStarted (jobId: $jobId) {
              ''' + JOB_FIELDS + '''
             }
        }
        ''',
    'ON_JOB_FINISHED':
        '''
        subscription ($jobId: String){
             onJobFinished (jobId: $jobId) {
                ''' + JOB_FIELDS + '''
             }
        }
        ''',
}
