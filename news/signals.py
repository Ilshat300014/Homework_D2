from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    title = instance.postTitle
    if not created:
        for value in instance.category.values():
            category_name = value['categoryName']
            category_subscribers = instance.category.get(categoryName=category_name).subscribers
            for subscriber in category_subscribers:
                send_mail(
                    subject = title, # тема
                    message = f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе {category_name}!',  # сообщение с кратким описанием проблемы
                    from_email = 'aigulapai@yandex.ru', # отправитель
                    recipient_list = [subscriber.email] # получатель
                )