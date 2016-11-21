from datetime import timedelta

from django.conf import settings
from django_cron import CronJobBase, Schedule as CronSchedule
from django.utils import timezone
from wechat_sdk import WechatBasic

from hangout import logic as hangout_logic
from hangout.models import Schedule, ScheduleUser, HangoutConfig


class HangoutCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = CronSchedule(run_every_mins=RUN_EVERY_MINS)
    code = 'HangoutCronJob'  # a unique code

    def do(self):
        print('start HangoutCronJob')
        cursor_date = timezone.now() + timedelta(hours=1)   # 取一小时内的数据
        schedules = Schedule.objects.filter(started_date__lt=cursor_date, is_notified=False).all()
        print('schedules: ', len(schedules))

        wechat_config = settings.WECHAT_CONF
        wechat_base = WechatBasic(conf=wechat_config, **HangoutConfig.get_access_token())

        for schedule in schedules:
            notify_at = schedule.started_date - timedelta(minutes=schedule.notify_other)
            is_notify = notify_at < timezone.now()

            print('current schedule is: %s' % schedule)
            if not is_notify:
                print('will be notify at: %s' % notify_at)
                continue

            natural_time = hangout_logic.natural_time(schedule.started_date)
            print('natural_time is: %s' % natural_time)

            text = "别忘了%s的预约哦!" % natural_time
            hangout_logic.template_notify(wechat_base,
                                          schedule.wechatauth, schedule, title=text)

            print('template send to owner ok')

            text = "别忘了与%s%s的预约哦!" % (schedule.user.userinfo.nickname, natural_time)

            for su in ScheduleUser.objects.filter(schedule=schedule).all():
                hangout_logic.template_notify(wechat_base,
                                              su.wechatauth, schedule, title=text)

            print('template send to other ok')
            schedule.is_notified = True
            schedule.save()
            print('save')
        print('end HangoutCronJob')
