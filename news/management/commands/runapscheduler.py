import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

from ...models import PostCategory
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    today = datetime.today()
    last_week = today - timedelta(days=7)
    week_posts = PostCategory.objects.filter(post__createDate__date__range=(last_week.date(), today.date()))
    category_set = {i.category.categoryName for i in week_posts}
    for category in category_set:
        choice_posts = week_posts.filter(category__categoryName=category)
        subscribers_emails = choice_posts[0].category.get_subscribers_email_list()
        message = f'''Вас приветствует Ваш любимый новостной портал!
Вот {"список статей, опубликованных" if choice_posts.count() > 0 else "статья, опубликованная"} за прошедшую неделю:\n'''
        for post in choice_posts:
            message = message + 'http://127.0.0.1:8000' + post.post.get_absolute_url() + '\n'
            # отправляем письмо
        send_mail(
            subject='Новые посты',
            # имя клиента и дата записи будут в теме для удобства
            message=message,  # сообщение с кратким описанием проблемы
            from_email='aigulapai@yandex.ru',
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[subscribers_emails]  # здесь список получателей. Например, секретарь, сам врач и так далее
        )



# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")