from lib.django_cron import cronScheduler, Job

class TestCron(Job):
    run_every = 10 #seconds
    def job(self):
        #f = open('/home/erem/beatwrit/CRON_TESTING.test', 'w')
        """
        f = open('CRON_TESTING', 'w')
        print "WHAT!"
        f.write('BOOOOOM')
        f.close()
        """

cronScheduler.register(TestCron)
"""
class CheckMail(Job):
        run_every = 300
                
        def job(self):
                # This will be executed every 5 minutes
                check_feedback_mailbox()
"""
#cronScheduler.register(CheckMail)
