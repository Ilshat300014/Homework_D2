from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post, PostCategory


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_managers_post(**kwargs):
    post = PostCategory.objects.all().last()
    for subscriber in post.category.subscribers.values():
        print(f"In {post.category.categoryName} added new post. Mail sent to {subscriber['username']} {subscriber['email']}")
        # send_mail(
        #     subject = 'Signals', # тема
        #     message = f'Здравствуй, {subscriber["username"]}. Новая статья в твоём любимом разделе {category.categoryName}!',  # сообщение с кратким описанием проблемы
        #     from_email = 'aigulapai@yandex.ru', # отправитель
        #     recipient_list = [subscriber["email"]] # получатель
        # )
