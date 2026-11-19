from django.db import models

class Team(models.Model):
    class Category(models.TextChoices):
        # Categorías iniciales; pueden ajustarse a las de la liga.
        INFANTIL = 'infantil', 'Infantil'
        JUVENIL = 'juvenil', 'Juvenil'

    name = models.CharField('nombre', max_length=100)
    city = models.CharField('ciudad', max_length=100)
    category = models.CharField('categoría', max_length=20, choices=Category.choices)

    class Meta:
        verbose_name = 'equipo'
        verbose_name_plural = 'equipos'
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField('nombre', max_length=100)
    number = models.PositiveIntegerField('número')
    position = models.CharField('posición', max_length=50)
    birth_date = models.DateField('fecha de nacimiento')
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='players', verbose_name='equipo'
    )

    class Meta:
        verbose_name = 'jugador'
        verbose_name_plural = 'jugadores'
        ordering = ['team', 'number', 'name']

    def __str__(self):
        return f'{self.name} (#{self.number})'
