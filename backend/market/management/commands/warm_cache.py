from django.core.management.base import BaseCommand
from market.cache_utils import CacheManager, schedule_cache_warming
from django.utils import timezone

class Command(BaseCommand):
    help = 'Warm up application cache with frequently accessed data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--schedule',
            action='store_true',
            help='Schedule periodic cache warming in background',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show cache statistics',
        )

    def handle(self, *args, **options):
        if options['stats']:
            self.show_cache_stats()
        elif options['schedule']:
            self.schedule_cache_warming()
        else:
            self.warm_cache()

    def warm_cache(self):
        """Warm up the cache with frequently accessed data"""
        self.stdout.write('Starting cache warming...')
        start_time = timezone.now()

        try:
            success = CacheManager.warm_up_cache()
            
            if success:
                end_time = timezone.now()
                duration = (end_time - start_time).total_seconds()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Cache warming completed successfully in {duration:.2f} seconds'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Cache warming failed')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Cache warming error: {str(e)}')
            )

    def schedule_cache_warming(self):
        """Schedule periodic cache warming"""
        self.stdout.write('Scheduling periodic cache warming...')
        
        try:
            success = schedule_cache_warming()
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('Cache warming scheduled successfully')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed to schedule cache warming')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Scheduling error: {str(e)}')
            )

    def show_cache_stats(self):
        """Display cache statistics"""
        self.stdout.write('Cache Statistics:')
        
        try:
            stats = CacheManager.get_cache_stats()
            
            for key, value in stats.items():
                self.stdout.write(f'  {key.replace("_", " ").title()}: {value}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting cache stats: {str(e)}')
            )
