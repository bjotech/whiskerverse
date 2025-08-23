from ..repositories.timer_repository import TimerRepository
import datetime

class TimerService:
    def __init__(self):
        self.timer_repo = TimerRepository()
    
    def is_available(self, player_id: int, action: str) -> bool:
        """Check if an action is available for a player"""
        timer = self.timer_repo.get_timer(player_id, action)
        if not timer:
            return True
        
        now = datetime.datetime.utcnow()
        return now >= timer['next_available']
    
    def get_seconds_remaining(self, player_id: int, action: str) -> int:
        """Get the number of seconds remaining until the action is available again"""
        timer = self.timer_repo.get_timer(player_id, action)
        if not timer:
            return 0
        
        now = datetime.datetime.utcnow()
        if now >= timer['next_available']:
            return 0
        
        time_diff = timer['next_available'] - now
        return int(time_diff.total_seconds())
    
    def set_cooldown(self, player_id: int, action: str, seconds: int):
        """Set a cooldown for a player action"""
        next_available = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        self.timer_repo.set_timer(player_id, action, next_available)
        return next_available
    
    def clear_timer(self, player_id: int, action: str):
        """Clear a timer for a player action"""
        return self.timer_repo.delete_timer(player_id, action)
    
    def get_all_timers(self, player_id: int):
        """Get all active timers for a player"""
        timers = self.timer_repo.get_all_timers(player_id)
        now = datetime.datetime.utcnow()
        
        active_timers = []
        for timer in timers:
            if timer['next_available'] > now:
                seconds_remaining = int((timer['next_available'] - now).total_seconds())
                active_timers.append({
                    'action': timer['action'],
                    'seconds_remaining': seconds_remaining,
                    'next_available': timer['next_available']
                })
        
        return active_timers
    
    def reset_all_timers(self):
        """Reset all timers for all players (admin function)"""
        return self.timer_repo.reset_all_timers()