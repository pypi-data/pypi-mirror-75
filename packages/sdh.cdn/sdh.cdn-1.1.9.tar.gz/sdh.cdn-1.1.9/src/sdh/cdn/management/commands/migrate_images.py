import importlib
from types import ModuleType
from django.core.management.base import BaseCommand, CommandError
from django.db.models.fields.files import ImageFileDescriptor

def get_class(path):
    class_path = path.split('.')
    if len(class_path) == 1:
        raise CommandError('Please set the dot separated path to Model Class (e.g. app.module.Class)')
    module = '.'.join(class_path[:-1])
    class_name = class_path[-1]
    try:
        _class = getattr(importlib.import_module(module), class_name)
    except ModuleNotFoundError as e:
        raise CommandError('ModuleNotFoundError: %s' % e)
    except AttributeError as e:
        raise CommandError(e)
    if isinstance(_class, ModuleType):
        raise CommandError('%s is module, not a class' % path)
    return _class


class Command(BaseCommand):
    help = 'Migrates DB stored images to another storage'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', help='Model class')
        parser.add_argument('-f', '--field', help='Image field')
        parser.add_argument('-o', '--old', help='Old storage class')

    def handle(self, *args, **options):
        if not options['model']:
            raise CommandError('Please set the Model Class Path (-m, --model option)')
        if not options['old']:
            raise CommandError('Please set the Old Storage Class (-o, --old option)')
        if not options['field']:
            raise CommandError('Please set the Image Field (-f, --field option)')

        model = get_class(options['model'])
        old = get_class(options['old'])()

        try:
            image_field = getattr(model, options['field'])
        except AttributeError:
            raise CommandError('%s is not a %s class field' % (options['field'], options['model']))
        if image_field.__class__ != ImageFileDescriptor:
            raise CommandError('Field %s.%s is not a image field' % (options['model'], options['field']))

        for record in model.objects.all():
            self.stdout.write(str(record))
            image = getattr(record, image_field.field.name)
            name = image.name
            extension = name.split('.')[-1]
            if not extension in ['jpg', 'png']:
                extension = old.url(image.name).split('.')[-1]
                name = '{}.{}'.format(name, extension)
            if old.exists(image.name):
                file = old.open(image.name)
            else:
                self.stdout.write('  {}  not exist in storage {}'.format(image.name, options['old']))
                continue
            if image.field.storage.exists(name):
                new_name = 'Already saved'
            else:
                new_name = image.field.storage.save(name, file)
                image.name = new_name
            self.stdout.write('  {}  >>>  {}'.format(name, new_name))
            record.save()

        self.stdout.write(self.style.SUCCESS('Success'))
