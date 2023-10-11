from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post, Category


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_post(action, instance, **kwargs):
    if action == 'post_add':
        category_name = instance.category.values()[0]['categoryName']
        category_values = Category.objects.get(categoryName=category_name)
        print(category_name)
        print(category_values.get_subscribers_email_list())
        # for subscriber in post.category.subscribers.values():
        # send_mail(
        #     subject = 'Signals', # тема
        #     message = f'Здравствуйте. Новая статья в Вашем любимом разделе {category_name}!',  # сообщение с кратким описанием проблемы
        #     from_email = 'aigulapai@yandex.ru', # отправитель
        #     recipient_list = category_values.get_subscribers_email_list() # получатель
        # )
