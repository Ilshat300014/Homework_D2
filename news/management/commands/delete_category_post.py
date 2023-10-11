from django.core.management.base import BaseCommand, CommandError
from ...models import PostCategory, Post


class Command(BaseCommand):
    help = 'Удаляет все посты в выбранной категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        category_values = PostCategory.category.get_queryset().values()
        name_list = [name['categoryName'] for name in category_values]
        self.stdout.write(
            f'Введите название категории из {name_list}, посты которых Вы хотите удалить:')  # спрашиваем пользователя, посты какой категории он хочет удалить
        category_name = input()
        if category_name in name_list:
            posts_count = Post.objects.filter(category__categoryName=category_name).count()
            self.stdout.write(
                f'Do you really want to delete {posts_count} posts? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
            answer = input()  # считываем подтверждение
            if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
                Post.objects.filter(category__categoryName=category_name).delete()
                self.stdout.write(self.style.SUCCESS('Succesfully delete posts!'))
                return
            self.stdout.write(
                self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано
            return
        self.stdout.write(f'Не правильный ввод названия категории')
        return