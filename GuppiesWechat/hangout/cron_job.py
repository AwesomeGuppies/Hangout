from datetime import timedelta

from django_cron import CronJobBase, Schedule as CronSchedule
from django.utils import timezone

from hangout import logic as hangout_logic
from hangout.models import Schedule, ScheduleUser


class HangoutCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = CronSchedule(run_every_mins=RUN_EVERY_MINS)
    code = 'HangoutCronJob'  # a unique code

    def do(self):
        print('start HangoutCronJob')
        cursor_date = timezone.now() + timedelta(hours=1)   # 取一小时内的数据
        schedules = Schedule.objects.filter(started_date__lt=cursor_date, is_notified=False).all()
        print('schedules: ', len(schedules))
        for schedule in schedules:
            notify_at = schedule.started_date - timedelta(minutes=schedule.notify_other)
            is_notify = notify_at < timezone.now()

            print('current schedule is: %s' % schedule)
            if not is_notify:
                print('will be notify at: %s' % notify_at)
                continue

            hangout_logic.template_notify(schedule, schedule.wechatauth, title="别忘了今天的预约哦!")

            for su in ScheduleUser.objects.filter(schedule=schedule).all():
                hangout_logic.template_notify(schedule, su.wechatauth, title="别忘了今天的预约哦!")

            schedule.is_notified = True
            schedule.save()
        print('end HangoutCronJob')
