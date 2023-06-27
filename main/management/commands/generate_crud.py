import os
import inspect
import importlib
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from django.template import Template, Context
from django.template.loader import get_template

# Define a helper function to create a new file with given content
def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

class Command(BaseCommand):
    help = 'Generates views, urls, and templates for a models.py file using FBV and htmx'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='App name to generate CRUD for')
        parser.add_argument('model_name', type=str, help='Model name to generate CRUD for')

    def handle(self, *args, **options):
        app_name = options['app_name']
        model_name = options['model_name']
        model_name_lower = model_name.lower()

        # Import the app and model dynamically
        models_module = importlib.import_module(f'{app_name}.models')
        model = getattr(models_module, model_name)

        # Render views and urls templates
        views_template = get_template('views_template.txt')
        urls_template = get_template('urls_template.txt')

        context = {
            'app_name': app_name,
            'model_name': model_name,
            'model_name_lower': model_name_lower,
            'model_name_plural': self.model_name_plural(model),
            'model_fields': self.get_field_names_for_model(model),
        }

        views_content = views_template.render(context)
        urls_content = urls_template.render(context)

        # Write views content to the views.py file
        with open(f'{app_name}/views.py', 'a') as views_file:
            views_file.write(views_content)

        # Write URLs content to the urls.py file
        with open(f'{app_name}/urls.py', 'a') as urls_file:
            urls_file.write(urls_content)

        # Generate templates for list, create, and update
        templates_dir = f'{app_name}/templates/{model_name_lower}'
        os.makedirs(templates_dir, exist_ok=True)

        template_files = [
            'list.html.txt', 
            'create.html.txt', 
            'detail.html.txt',
            'update.html.txt',
            'base.html.txt',
        ]

        for template_file in template_files:
            content=template_file.render(context)
            name=template_file.split(".txt")[0]
            create_file(f'{templates_dir}/{name}', content)
    
    def model_name_plural(self, model):
        if isinstance(model._meta.verbose_name_plural, str):
            return model._meta.verbose_name_plural
        return f"{model.__name__}s"

    def create_file_from_template(self, file_path, template_path, context_variables):
        with open(file_path, 'w') as new_file:
            new_file.write(get_template(template_path).render(context_variables))

    def get_field_names_for_model(self, model):
        """
            Returns fields other than id and uneditable fields (DateTimeField where auto_now or auto_now_add is True)
        """
        return [field.name for field in model._meta.get_fields() if field.name != "id" and not
                (field.get_internal_type() == "DateTimeField" and
                 (field.auto_now is True or field.auto_now_add is True)) and
                field.concrete and (not field.is_relation or field.one_to_one or
                                    (field.many_to_one and field.related_model))]