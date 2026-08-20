import csv
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from movie.models import Movie
from news.models import News

class Command(BaseCommand):
    help = 'Poblar la base de datos leyendo un archivo JSON (para películas) o CSV (para noticias)'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Ruta al archivo (ej. movies_initial.json o Fake.csv)')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'No se encontró el archivo: {file_path}'))
            return

        # --- PROCESAR ARCHIVO JSON (Películas) ---
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                movies = json.load(file)
                count = 0
                for movie in movies:
                    exist = Movie.objects.filter(title=movie['title']).first()
                    if not exist:
                        Movie.objects.create(
                            title=movie['title'],
                            image=movie.get('image', 'movie/images/default.jpg'),
                            description=movie.get('description', ''),
                            url=movie.get('url', ''),
                            genre=movie.get('genre', ''),
                            year=movie.get('year')
                        )
                        count += 1
            self.stdout.write(self.style.SUCCESS(f'Se agregaron {count} películas correctamente desde {file_path}.'))

        # --- PROCESAR ARCHIVO CSV (Noticias) ---
        elif file_path.endswith('.csv'):
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    if count >= 5:
                        break

                    headline = row.get('title', '').strip()
                    body = row.get('text', '').strip()
                    date_str = row.get('date', '').strip()

                    try:
                        formatted_date = datetime.strptime(date_str, '%B %d, %Y').date()
                    except ValueError:
                        try:
                            formatted_date = datetime.strptime(date_str, '%d-%b-%y').date()
                        except ValueError:
                            formatted_date = datetime.now().date()

                    News.objects.create(
                        headline=headline[:200],
                        body=body,
                        date=formatted_date
                    )
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Se agregaron {count} noticias correctamente desde {file_path}.'))

        else:
            self.stderr.write(self.style.ERROR('Formato no soportado. Usa un archivo .json o .csv'))